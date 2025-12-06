from typing import List, Dict, Any, Optional
from ..services.openai_service import OpenAIService
from ..services.qdrant_service import QdrantService
from ..config.settings import settings
import logging
import asyncio
from functools import lru_cache
import hashlib

class RAGService:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.qdrant_service = QdrantService()
        self.logger = logging.getLogger(__name__)
        # Add in-memory cache for query responses
        self._query_cache = {}
        # Add cache timeout (in seconds)
        self._cache_timeout = 300  # 5 minutes

    def _get_cache_key(self, query: str, content_slug: Optional[str] = None) -> str:
        """Generate a cache key for the query."""
        cache_input = f"{query}:{content_slug or 'all'}"
        return hashlib.md5(cache_input.encode()).hexdigest()

    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cached entry is still valid."""
        import time
        return (time.time() - timestamp) < self._cache_timeout

    async def _batch_index_content(self, content_list: List[Dict[str, Any]]):
        """Index multiple content items in batch for better performance."""
        try:
            vector_data_list = []
            for content_item in content_list:
                content_id = content_item["id"]
                content = content_item["content"]
                metadata = content_item.get("metadata", {})

                # Generate embeddings for the content
                embeddings = await self.openai_service.generate_embeddings(content)

                # Prepare vector data
                vector_data = {
                    "id": content_id,
                    "vector": embeddings,
                    "payload": {
                        "content_id": content_id,
                        "content": content,
                        "metadata": metadata
                    }
                }
                vector_data_list.append(vector_data)

            # Batch upsert to Qdrant
            await self.qdrant_service.upsert_vectors(vector_data_list)
            self.logger.info(f"Batch indexed {len(content_list)} content items successfully")
        except Exception as e:
            self.logger.error(f"Error in batch indexing: {str(e)}")
            raise

    async def initialize_rag_system(self):
        """Initialize the RAG system by creating necessary collections."""
        try:
            await self.qdrant_service.create_collection()
            self.logger.info("RAG system initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing RAG system: {str(e)}")
            raise

    async def index_content(self, content_id: str, content: str, metadata: Dict = None):
        """Index content for RAG retrieval."""
        try:
            # Generate embeddings for the content
            embeddings = await self.openai_service.generate_embeddings(content)

            # Prepare vector data
            vector_data = {
                "id": content_id,
                "vector": embeddings,
                "payload": {
                    "content_id": content_id,
                    "content": content,
                    "metadata": metadata or {}
                }
            }

            # Upsert to Qdrant
            await self.qdrant_service.upsert_vectors([vector_data])
            self.logger.info(f"Content indexed successfully: {content_id}")
        except Exception as e:
            self.logger.error(f"Error indexing content {content_id}: {str(e)}")
            raise

    async def query_rag(self, query: str, content_slug: Optional[str] = None, top_k: int = 5) -> Dict[str, Any]:
        """Query the RAG system for relevant information with performance optimizations."""
        import time

        # Generate cache key
        cache_key = self._get_cache_key(query, content_slug)

        # Check if result is in cache
        if cache_key in self._query_cache:
            cached_result, timestamp = self._query_cache[cache_key]
            if self._is_cache_valid(timestamp):
                self.logger.info(f"Cache hit for query: {query[:50]}...")
                return cached_result
            else:
                # Remove expired cache entry
                del self._query_cache[cache_key]

        try:
            # Generate embeddings for the query
            query_embeddings = await self.openai_service.generate_embeddings(query)

            # Search in Qdrant for similar content
            search_results = await self.qdrant_service.search_vectors(
                query_vector=query_embeddings,
                limit=top_k
            )

            if not search_results:
                result = {
                    "response": "I couldn't find relevant information in the textbook content to answer your question.",
                    "sources": [],
                    "confidence": 0.0
                }

                # Cache the result
                self._query_cache[cache_key] = (result, time.time())
                return result

            # Prepare context from search results
            context_parts = []
            sources = []

            for result in search_results:
                content = result["payload"]["content"]
                content_id = result["payload"]["content_id"]

                context_parts.append(content)
                sources.append(content_id)

            # Combine context (limit to avoid exceeding token limits)
            context = "\n\n".join(context_parts)
            # Truncate context if too long (OpenAI has token limits)
            if len(context) > 3000:  # Approximate token limit
                context = context[:3000]
                self.logger.warning("Context truncated to stay within token limits")

            # Generate response using OpenAI
            prompt = f"""
            You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
            Use the following context to answer the user's question.
            If the context doesn't contain enough information, say so.

            Context: {context}

            Question: {query}

            Answer:
            """

            response = await self.openai_service.generate_completion(
                prompt=prompt,
                max_tokens=500,
                temperature=0.3
            )

            # Calculate a simple confidence score based on search result scores
            avg_score = sum(r["score"] for r in search_results) / len(search_results)
            confidence = min(avg_score, 1.0)  # Normalize to 0-1 range

            result = {
                "response": response.strip(),
                "sources": sources,
                "confidence": confidence
            }

            # Cache the result
            self._query_cache[cache_key] = (result, time.time())

            return result

        except Exception as e:
            self.logger.error(f"Error querying RAG system: {str(e)}")
            raise

    async def validate_question_relevance(self, question: str, content_slug: Optional[str] = None) -> bool:
        """Validate if a question is relevant to the textbook content with caching."""
        import time

        # Generate cache key for validation
        cache_key = f"validate:{hashlib.md5(f'{question}:{content_slug or \"all\"}'.encode()).hexdigest()}"

        # Check if result is in cache
        if cache_key in self._query_cache:
            cached_result, timestamp = self._query_cache[cache_key]
            # Use shorter timeout for validation (2 minutes)
            if (time.time() - timestamp) < 120:
                self.logger.info(f"Validation cache hit for question: {question[:50]}...")
                return cached_result
            else:
                # Remove expired cache entry
                del self._query_cache[cache_key]

        try:
            # Generate embeddings for the question
            question_embeddings = await self.openai_service.generate_embeddings(question)

            # Search in Qdrant to see if there are any related documents
            search_results = await self.qdrant_service.search_vectors(
                query_vector=question_embeddings,
                limit=1  # Just check if there's any match
            )

            # If we found matches, the question is likely relevant
            result = len(search_results) > 0

            # Cache the result
            self._query_cache[cache_key] = (result, time.time())

            return result

        except Exception as e:
            self.logger.error(f"Error validating question relevance: {str(e)}")
            # Default to True to not block valid questions
            return True

    async def get_content_context(self, content_slug: str) -> str:
        """Get context for a specific content slug."""
        # This would typically fetch from a content management system
        # For now, we'll return a placeholder
        return f"Content context for {content_slug}"
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from ..config.settings import settings

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=False  # Set to True in production if gRPC is available
        )
        self.collection_name = "textbook_content"

    async def create_collection(self, vector_size: int = 1536):
        """Create a collection for storing textbook content embeddings."""
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            if self.collection_name not in [col.name for col in collections.collections]:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE
                    )
                )
        except Exception as e:
            raise Exception(f"Error creating Qdrant collection: {str(e)}")

    async def upsert_vectors(self, vectors: List[Dict], vector_size: int = 1536):
        """Upsert vectors into the collection."""
        try:
            points = []
            for vector_data in vectors:
                points.append(
                    models.PointStruct(
                        id=vector_data["id"],
                        vector=vector_data["vector"],
                        payload=vector_data.get("payload", {})
                    )
                )

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
        except Exception as e:
            raise Exception(f"Error upserting vectors: {str(e)}")

    async def search_vectors(self, query_vector: List[float], limit: int = 10) -> List[Dict]:
        """Search for similar vectors in the collection."""
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )

            return [
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                }
                for result in results
            ]
        except Exception as e:
            raise Exception(f"Error searching vectors: {str(e)}")

    async def delete_vectors(self, ids: List[str]):
        """Delete vectors by IDs."""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=ids
                )
            )
        except Exception as e:
            raise Exception(f"Error deleting vectors: {str(e)}")

    async def get_vector_count(self) -> int:
        """Get the total count of vectors in the collection."""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.points_count
        except Exception as e:
            raise Exception(f"Error getting vector count: {str(e)}")
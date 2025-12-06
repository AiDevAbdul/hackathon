from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
import json
import re
from uuid import UUID

from ..models.user import User
from ..models.translation import TranslationCache
from ..services.openai_service import OpenAIService
from ..utils.cache import cache_manager

class TranslationService:
    def __init__(self):
        self.openai_service = OpenAIService()

    @staticmethod
    async def get_cached_translation(db: AsyncSession, content_id: str, target_language: str) -> Optional[TranslationCache]:
        """Get cached translation if it exists and is not expired."""
        # First check the in-memory cache
        cache_key = f"translation:{content_id}:{target_language}"
        cached_result = await cache_manager.get(cache_key)
        if cached_result is not None:
            return cached_result

        # If not in memory cache, check database
        result = await db.execute(
            select(TranslationCache)
            .filter(TranslationCache.content_id == content_id)
            .filter(TranslationCache.target_language == target_language)
            .filter(TranslationCache.expires_at > datetime.utcnow())
        )
        translation = result.scalar_one_or_none()

        # Cache the result in memory for faster subsequent access (short TTL)
        if translation:
            await cache_manager.set(cache_key, translation, ttl=60)  # 1 minute in-memory cache

        return translation

    @staticmethod
    async def cache_translation(
        db: AsyncSession,
        content_id: str,
        target_language: str,
        translated_content: str,
        confidence_score: float = 1.0
    ) -> TranslationCache:
        """Cache a translation with a default expiration of 24 hours."""
        # Check if a cached version already exists and update it, or create a new one
        existing = await TranslationService.get_cached_translation(db, content_id, target_language)

        if existing:
            existing.translated_content = translated_content
            existing.confidence_score = confidence_score
            existing.updated_at = datetime.utcnow()
            existing.expires_at = datetime.utcnow() + timedelta(hours=24)
        else:
            from ..models.translation import TranslationCache as TranslationCacheModel
            existing = TranslationCacheModel(
                content_id=content_id,
                target_language=target_language,
                translated_content=translated_content,
                confidence_score=confidence_score,
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            db.add(existing)

        await db.commit()
        await db.refresh(existing)

        # Clear the in-memory cache for this translation
        cache_key = f"translation:{content_id}:{target_language}"
        await cache_manager.delete(cache_key)

        return existing

    async def translate_content(self, content: str, target_language: str = "ur") -> tuple[str, float]:
        """Translate content using OpenAI API."""
        try:
            # Create a prompt for translation
            prompt = f"""
            Translate the following text to {target_language}.
            Preserve technical terminology and meaning as much as possible.
            If it's Urdu, use proper Urdu script and grammar.

            Text to translate: {content}

            Translation:
            """

            translated_text = await self.openai_service.generate_completion(
                prompt=prompt,
                max_tokens=len(content) * 2,  # Allow more tokens for translation
                temperature=0.3
            )

            # For now, return a confidence score of 0.8 (would be calculated more accurately in a real implementation)
            confidence = 0.8
            return translated_text.strip(), confidence

        except Exception as e:
            raise Exception(f"Error translating content: {str(e)}")

    def validate_translation_quality(self, original_content: str, translated_content: str, target_language: str = "ur") -> dict:
        """
        Validate the quality of a translation and return a quality report.

        Args:
            original_content: The original content before translation
            translated_content: The translated content to validate
            target_language: The target language code (default: "ur" for Urdu)

        Returns:
            dict: Quality report containing various metrics and validation results
        """
        quality_report = {
            "is_valid": True,
            "confidence_score": 0.0,
            "issues": [],
            "metrics": {}
        }

        # Check for empty translation
        if not translated_content or not translated_content.strip():
            quality_report["is_valid"] = False
            quality_report["issues"].append("Translation is empty or contains only whitespace")
            quality_report["confidence_score"] = 0.0
            return quality_report

        # Calculate basic metrics
        original_length = len(original_content)
        translated_length = len(translated_content)

        # Length ratio check (should be reasonable, not too short or too long)
        if original_length > 0:
            length_ratio = translated_length / original_length
            quality_report["metrics"]["length_ratio"] = round(length_ratio, 2)

            if length_ratio < 0.3:  # Translation is less than 30% of original
                quality_report["issues"].append(f"Translation is significantly shorter than original ({length_ratio:.2f} ratio)")
            elif length_ratio > 3.0:  # Translation is more than 3x longer than original
                quality_report["issues"].append(f"Translation is significantly longer than original ({length_ratio:.2f} ratio)")
        else:
            quality_report["metrics"]["length_ratio"] = 0.0

        # Character validation based on target language
        if target_language.lower() == "ur":
            # For Urdu, check if it contains Arabic/Persian script characters
            urdu_pattern = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
            has_urdu_chars = bool(re.search(urdu_pattern, translated_content))

            if not has_urdu_chars:
                quality_report["issues"].append("Translation does not contain Urdu/Arabic script characters")
                quality_report["is_valid"] = False

        # Check for excessive repetition (potential AI hallucination)
        words = translated_content.split()
        if len(words) > 5:  # Only check if there are enough words
            unique_words = set(words)
            repetition_ratio = len(unique_words) / len(words)
            quality_report["metrics"]["repetition_ratio"] = round(repetition_ratio, 2)

            if repetition_ratio < 0.3:  # More than 70% repetition
                quality_report["issues"].append(f"High repetition detected in translation ({repetition_ratio:.2f} unique ratio)")

        # Check for placeholder or template-like content
        placeholder_patterns = [
            r'\[.*?\]',  # [TEXT] style placeholders
            r'\{\{.*?\}\}',  # {{TEXT}} style placeholders
            r'UNTRANSLATED.*?TEXT',  # Untranslated text markers
        ]

        for pattern in placeholder_patterns:
            if re.search(pattern, translated_content, re.IGNORECASE):
                quality_report["issues"].append(f"Potential placeholder pattern detected: {pattern}")
                quality_report["is_valid"] = False

        # Calculate confidence score based on issues found
        issue_count = len(quality_report["issues"])
        if issue_count == 0:
            quality_score = 0.9  # High quality if no issues
        elif issue_count == 1:
            quality_score = 0.7  # Medium quality if one issue
        elif issue_count == 2:
            quality_score = 0.5  # Lower quality if two issues
        else:
            quality_score = 0.2  # Very low quality if multiple issues

        # Adjust score based on severity of issues
        for issue in quality_report["issues"]:
            if "empty" in issue.lower() or "does not contain" in issue.lower():
                quality_score = min(quality_score, 0.1)  # Very serious issues

        quality_report["confidence_score"] = round(quality_score, 2)

        # If we found serious issues, mark as invalid
        if any("empty" in issue.lower() or "does not contain" in issue.lower() for issue in quality_report["issues"]):
            quality_report["is_valid"] = False

        return quality_report

    async def get_or_create_translation(
        self,
        db: AsyncSession,
        content_id: str,
        content: str,
        target_language: str = "ur",
        min_quality_score: float = 0.5
    ) -> tuple[str, float]:
        """Get cached translation or create a new one with quality validation."""
        # Try to get cached translation
        cached = await TranslationService.get_cached_translation(db, content_id, target_language)

        if cached:
            # Validate cached translation quality if it's below minimum threshold
            if cached.confidence_score < min_quality_score:
                quality_report = self.validate_translation_quality(content, cached.translated_content, target_language)
                if not quality_report["is_valid"] or quality_report["confidence_score"] < min_quality_score:
                    # Invalidate the low-quality cached translation
                    await TranslationService.invalidate_translation_cache(db, content_id, target_language)
                else:
                    # Update the cached confidence score if validation gives a different score
                    if abs(quality_report["confidence_score"] - cached.confidence_score) > 0.01:
                        cached.confidence_score = quality_report["confidence_score"]
                        await db.commit()
                    return cached.translated_content, cached.confidence_score

        # If not cached or cached version is invalid, translate and validate
        translated_content, initial_confidence = await self.translate_content(content, target_language)

        # Validate the quality of the new translation
        quality_report = self.validate_translation_quality(content, translated_content, target_language)

        # If translation quality is below minimum threshold, raise an exception
        if not quality_report["is_valid"] or quality_report["confidence_score"] < min_quality_score:
            raise Exception(f"Translation quality is too low (score: {quality_report['confidence_score']}). Issues: {', '.join(quality_report['issues'])}")

        # Use the validated confidence score instead of the initial one
        final_confidence = quality_report["confidence_score"]

        await TranslationService.cache_translation(
            db, content_id, target_language, translated_content, final_confidence
        )

        return translated_content, final_confidence

    @staticmethod
    async def invalidate_translation_cache(db: AsyncSession, content_id: str, target_language: str = None):
        """Invalidate cached translation(s)."""
        query = select(TranslationCache).filter(TranslationCache.content_id == content_id)

        if target_language:
            query = query.filter(TranslationCache.target_language == target_language)

        result = await db.execute(query)
        translations = result.scalars().all()

        for translation in translations:
            await db.delete(translation)

        await db.commit()
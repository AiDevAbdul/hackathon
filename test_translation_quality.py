"""
Test script for translation quality validation functionality
"""
import sys
import re


def validate_translation_quality(original_content: str, translated_content: str, target_language: str = "ur") -> dict:
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


def test_translation_quality_validation():
    """Test the translation quality validation functionality."""

    print("Testing Translation Quality Validation...")

    # Test 1: Valid translation
    print("\n1. Testing valid translation:")
    original = "Artificial intelligence is a wonderful field of computer science."
    translated = "مصنوعی ذہانت کمپیوٹر سائنس کا ایک شاندار میدان ہے۔"

    result = validate_translation_quality(original, translated, "ur")
    print(f"   Original: {original}")
    print(f"   Translated: [URDU TEXT - {len(translated)} chars]")
    print(f"   Is Valid: {result['is_valid']}")
    print(f"   Confidence Score: {result['confidence_score']}")
    print(f"   Issues: {result['issues']}")
    print(f"   Metrics: {result['metrics']}")

    # Test 2: Empty translation
    print("\n2. Testing empty translation:")
    result = validate_translation_quality(original, "", "ur")
    print(f"   Original: {original}")
    print(f"   Translated: ''")
    print(f"   Is Valid: {result['is_valid']}")
    print(f"   Confidence Score: {result['confidence_score']}")
    print(f"   Issues: {result['issues']}")

    # Test 3: Translation without Urdu characters
    print("\n3. Testing translation without Urdu characters:")
    translated_bad = "This is not in Urdu script"
    result = validate_translation_quality(original, translated_bad, "ur")
    print(f"   Original: {original}")
    print(f"   Translated: {translated_bad}")
    print(f"   Is Valid: {result['is_valid']}")
    print(f"   Confidence Score: {result['confidence_score']}")
    print(f"   Issues: {result['issues']}")

    # Test 4: Translation that is too short
    print("\n4. Testing translation that is too short:")
    translated_short = "AI"
    result = validate_translation_quality(original, translated_short, "ur")
    print(f"   Original: {original}")
    print(f"   Translated: {translated_short}")
    print(f"   Is Valid: {result['is_valid']}")
    print(f"   Confidence Score: {result['confidence_score']}")
    print(f"   Issues: {result['issues']}")

    # Test 5: Translation with high repetition
    print("\n5. Testing translation with high repetition:")
    translated_repeat = "ذہانت ذہانت ذہانت کمپیوٹر کمپیوٹر کمپیوٹر سائنس سائنس سائنس"
    result = validate_translation_quality(original, translated_repeat, "ur")
    print(f"   Original: {original}")
    print(f"   Translated: [REPEATED URDU TEXT - {len(translated_repeat)} chars]")
    print(f"   Is Valid: {result['is_valid']}")
    print(f"   Confidence Score: {result['confidence_score']}")
    print(f"   Issues: {result['issues']}")

    print("\nTranslation quality validation tests completed!")


if __name__ == "__main__":
    test_translation_quality_validation()
import React, { useState } from 'react';
import TranslationService from '../../services/translationService';

const TranslationToggle = ({ contentSlug, onTranslationChange }) => {
  const [isTranslating, setIsTranslating] = useState(false);
  const [translationError, setTranslationError] = useState(null);

  const handleTranslateToUrdu = async () => {
    if (!contentSlug) {
      setTranslationError('Content slug is required for translation');
      return;
    }

    setIsTranslating(true);
    setTranslationError(null);

    try {
      const translationData = await TranslationService.getUrduTranslation(contentSlug);
      if (onTranslationChange) {
        onTranslationChange(translationData.translated_content);
      }
    } catch (error) {
      console.error('Translation error:', error);
      setTranslationError('Failed to translate content. Please try again.');
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <div className="translation-toggle">
      <button
        onClick={handleTranslateToUrdu}
        disabled={isTranslating}
        className="translation-button"
      >
        {isTranslating ? 'Translating...' : '.Translate to Urdu'}
      </button>
      {translationError && (
        <div className="translation-error">
          {translationError}
        </div>
      )}
    </div>
  );
};

export default TranslationToggle;
import React, { useState, useEffect } from 'react';

const TranslationProgress = ({
  contentId,
  targetLanguage,
  onProgressUpdate,
  initialProgress = 0
}) => {
  const [progress, setProgress] = useState(initialProgress);
  const [isTranslating, setIsTranslating] = useState(false);
  const [status, setStatus] = useState('idle'); // idle, translating, completed, error

  // Simulate translation progress for demonstration
  useEffect(() => {
    if (isTranslating && progress < 100) {
      const interval = setInterval(() => {
        setProgress(prev => {
          const newProgress = Math.min(prev + 5, 100);

          if (newProgress === 100) {
            clearInterval(interval);
            setStatus('completed');
            if (onProgressUpdate) {
              onProgressUpdate({ contentId, targetLanguage, progress: 100, status: 'completed' });
            }
            return 100;
          }

          if (onProgressUpdate) {
            onProgressUpdate({ contentId, targetLanguage, progress: newProgress, status: 'translating' });
          }

          return newProgress;
        });
      }, 200);

      return () => clearInterval(interval);
    }
  }, [isTranslating, progress, contentId, targetLanguage, onProgressUpdate]);

  const startTranslation = () => {
    if (status === 'completed') return;

    setProgress(0);
    setIsTranslating(true);
    setStatus('translating');
    if (onProgressUpdate) {
      onProgressUpdate({ contentId, targetLanguage, progress: 0, status: 'translating' });
    }
  };

  const resetProgress = () => {
    setProgress(0);
    setIsTranslating(false);
    setStatus('idle');
    if (onProgressUpdate) {
      onProgressUpdate({ contentId, targetLanguage, progress: 0, status: 'idle' });
    }
  };

  const getProgressColor = () => {
    if (status === 'error') return '#e74c3c';
    if (status === 'completed') return '#27ae60';
    if (status === 'translating') return '#3498db';
    return '#bdc3c7';
  };

  const getStatusText = () => {
    switch (status) {
      case 'translating': return `Translating to ${targetLanguage}...`;
      case 'completed': return `Translation to ${targetLanguage} completed!`;
      case 'error': return `Translation to ${targetLanguage} failed`;
      default: return `Ready to translate to ${targetLanguage}`;
    }
  };

  return (
    <div className="translation-progress">
      <div className="progress-header">
        <h4>Translation Progress</h4>
        <div className="status-indicator">
          <span className={`status-dot ${status}`}></span>
          <span className="status-text">{getStatusText()}</span>
        </div>
      </div>

      <div className="progress-bar-container">
        <div
          className="progress-bar"
          style={{
            width: `${progress}%`,
            backgroundColor: getProgressColor(),
            height: '8px',
            borderRadius: '4px',
            transition: 'width 0.3s ease, background-color 0.3s ease'
          }}
        ></div>
      </div>

      <div className="progress-info">
        <span className="progress-percent">{Math.round(progress)}%</span>
        <div className="progress-actions">
          {!isTranslating && status !== 'completed' && (
            <button
              className="start-translation-btn"
              onClick={startTranslation}
              disabled={status === 'completed'}
            >
              Start Translation
            </button>
          )}
          {status === 'completed' && (
            <button
              className="reset-translation-btn"
              onClick={resetProgress}
            >
              Reset
            </button>
          )}
        </div>
      </div>

      <style jsx>{`
        .translation-progress {
          background: var(--ifm-color-emphasis-100, #f5f6f7);
          border-radius: 8px;
          padding: 16px;
          margin: 16px 0;
          border: 1px solid var(--ifm-color-emphasis-200, #ebedf0);
        }

        .progress-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 12px;
        }

        .progress-header h4 {
          margin: 0;
          font-size: 14px;
          font-weight: 600;
          color: var(--ifm-heading-color, #252525);
        }

        .status-indicator {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 12px;
        }

        .status-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          display: inline-block;
        }

        .status-dot.idle {
          background-color: #bdc3c7;
        }

        .status-dot.translating {
          background-color: #3498db;
          animation: pulse 1.5s ease-in-out infinite;
        }

        .status-dot.completed {
          background-color: #27ae60;
        }

        .status-dot.error {
          background-color: #e74c3c;
        }

        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }

        .progress-bar-container {
          background: var(--ifm-color-emphasis-200, #ebedf0);
          border-radius: 4px;
          height: 8px;
          overflow: hidden;
          margin-bottom: 8px;
        }

        .progress-info {
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 12px;
          color: var(--ifm-color-emphasis-600, #606770);
        }

        .progress-actions {
          display: flex;
          gap: 8px;
        }

        button {
          padding: 4px 12px;
          border: 1px solid var(--ifm-color-emphasis-300, #dadde1);
          border-radius: 4px;
          background: white;
          color: var(--ifm-color-emphasis-600, #606770);
          font-size: 12px;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        button:hover {
          background: var(--ifm-color-emphasis-200, #ebedf0);
        }

        button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .start-translation-btn {
          background: #3498db;
          color: white;
          border-color: #3498db;
        }

        .start-translation-btn:hover:not(:disabled) {
          background: #2980b9;
          border-color: #2980b9;
        }

        .reset-translation-btn {
          background: #e74c3c;
          color: white;
          border-color: #e74c3c;
        }

        .reset-translation-btn:hover {
          background: #c0392b;
          border-color: #c0392b;
        }
      `}</style>
    </div>
  );
};

export default TranslationProgress;
import React from 'react';

const UrduContent = ({ content, isLoading, error }) => {
  if (error) {
    return (
      <div className="urdu-content error">
        <p>Error loading Urdu translation: {error}</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="urdu-content loading">
        <p>Translating to Urdu...</p>
      </div>
    );
  }

  if (!content) {
    return (
      <div className="urdu-content empty">
        <p>No Urdu translation available</p>
      </div>
    );
  }

  return (
    <div className="urdu-content" dir="rtl" lang="ur">
      <div className="urdu-text">
        {content}
      </div>
    </div>
  );
};

export default UrduContent;
import React from 'react';

const FunFactCard = ({ fact }) => {
  if (!fact) {
    return null;
  }

  return (
    <div className="fun-fact-card">
      <div className="fun-fact-title">
        🤓 Fun Fact: {fact.title}
      </div>
      <div className="fun-fact-description">
        {fact.description}
      </div>
      <div className="fun-fact-meta">
        <span className="fun-fact-category">
          Category: {fact.category}
        </span>
        <span className="fun-fact-level">
          Level: {fact.difficulty_level}
        </span>
      </div>
    </div>
  );
};

export default FunFactCard;
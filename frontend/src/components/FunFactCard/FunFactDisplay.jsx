import React from 'react';
import FunFactCard from './FunFactCard';

const FunFactDisplay = ({ facts, isLoading, error }) => {
  if (error) {
    return (
      <div className="fun-fact-display error">
        <p>Error loading fun facts: {error}</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="fun-fact-display loading">
        <p>Loading fun facts...</p>
      </div>
    );
  }

  if (!facts || facts.length === 0) {
    return (
      <div className="fun-fact-display empty">
        <p>No fun facts available for this section</p>
      </div>
    );
  }

  return (
    <div className="fun-fact-display">
      {facts.map((fact, index) => (
        <FunFactCard key={fact.id || index} fact={fact} />
      ))}
    </div>
  );
};

export default FunFactDisplay;
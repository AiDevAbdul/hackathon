import React from 'react';
import './FunFactStyling.module.css'; // Import the CSS module

const FunFactStyling = ({ children,styleType = 'default' }) => {
  const getStyleClasses = (type) => {
    const baseClass = 'fun-fact-styled';
    switch (type) {
      case 'highlight':
        return `${baseClass} fun-fact-highlight`;
      case 'minimal':
        return `${baseClass} fun-fact-minimal`;
      case 'accent':
        return `${baseClass} fun-fact-accent`;
      case 'boxed':
        return `${baseClass} fun-fact-boxed`;
      case 'rounded':
        return `${baseClass} fun-fact-rounded`;
      case 'card':
        return `${baseClass} fun-fact-card`;
      default:
        return `${baseClass} fun-fact-default`;
    }
  };

  return (
    <div className={getStyleClasses(styleType)}>
      {children}
    </div>
  );
};

export default FunFactStyling;
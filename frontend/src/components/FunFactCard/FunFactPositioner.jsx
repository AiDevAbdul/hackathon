import React from 'react';

const FunFactPositioner = ({ children, position = 'inline' }) => {
  const getPositionClasses = (pos) => {
    switch (pos) {
      case 'inline':
        return 'fun-fact-inline';
      case 'sidebar':
        return 'fun-fact-sidebar';
      case 'popup':
        return 'fun-fact-popup';
      case 'floating':
        return 'fun-fact-floating';
      default:
        return 'fun-fact-inline';
    }
  };

  return (
    <div className={`fun-fact-positioner ${getPositionClasses(position)}`}>
      {children}
    </div>
  );
};

export default FunFactPositioner;
import React, { createContext, useContext, useEffect, useState } from 'react';

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('system');

  useEffect(() => {
    // Load theme preference from localStorage or system preference
    const savedTheme = localStorage.getItem('theme') || 'system';
    setTheme(savedTheme);

    // Apply the theme to the document
    applyTheme(savedTheme);
  }, []);

  const applyTheme = (themeMode) => {
    // Remove existing theme classes
    document.documentElement.classList.remove('light', 'dark');

    // Determine actual theme based on system preference if needed
    let actualTheme = themeMode;
    if (themeMode === 'system') {
      actualTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    // Apply theme class
    document.documentElement.classList.add(actualTheme);
  };

  const updateTheme = (newTheme) => {
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
  };

  const value = {
    theme,
    updateTheme
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};
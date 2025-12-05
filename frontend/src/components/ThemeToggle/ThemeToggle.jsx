import React, { useState, useEffect } from 'react';
import { FaSun, FaMoon, FaLaptop } from 'react-icons/fa';
import UserPreferencesService from '../../services/userPreferencesService';

const ThemeToggle = () => {
  const [currentTheme, setCurrentTheme] = useState('system');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadThemePreference();
  }, []);

  const loadThemePreference = async () => {
    try {
      const themeData = await UserPreferencesService.getThemePreference();
      const themeMode = themeData.theme_mode || 'system';
      setCurrentTheme(themeMode);
      applyTheme(themeMode);
    } catch (error) {
      // Default to system theme if API call fails
      setCurrentTheme('system');
      applyTheme('system');
    } finally {
      setIsLoading(false);
    }
  };

  const applyTheme = (theme) => {
    // Remove existing theme classes
    document.documentElement.classList.remove('light', 'dark');

    // Determine actual theme based on system preference if needed
    let actualTheme = theme;
    if (theme === 'system') {
      actualTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    // Apply theme class
    document.documentElement.classList.add(actualTheme);

    // Store preference in localStorage for consistency
    localStorage.setItem('theme', theme);
  };

  const toggleTheme = async (newTheme) => {
    try {
      await UserPreferencesService.updateThemePreference(newTheme);
      setCurrentTheme(newTheme);
      applyTheme(newTheme);
    } catch (error) {
      console.error('Failed to update theme preference:', error);
      // Fallback to just applying the theme locally if API fails
      setCurrentTheme(newTheme);
      applyTheme(newTheme);
    }
  };

  if (isLoading) {
    return (
      <div className="theme-toggle">
        <span>Loading theme...</span>
      </div>
    );
  }

  return (
    <div className="theme-toggle">
      <button
        onClick={() => toggleTheme('light')}
        className={`theme-button ${currentTheme === 'light' ? 'active' : ''}`}
        title="Light theme"
        aria-label="Switch to light theme"
      >
        <FaSun />
      </button>
      <button
        onClick={() => toggleTheme('dark')}
        className={`theme-button ${currentTheme === 'dark' ? 'active' : ''}`}
        title="Dark theme"
        aria-label="Switch to dark theme"
      >
        <FaMoon />
      </button>
      <button
        onClick={() => toggleTheme('system')}
        className={`theme-button ${currentTheme === 'system' ? 'active' : ''}`}
        title="System theme"
        aria-label="Switch to system theme"
      >
        <FaLaptop />
      </button>
      <span className="theme-label">
        Theme: {currentTheme.charAt(0).toUpperCase() + currentTheme.slice(1)}
      </span>
    </div>
  );
};

export default ThemeToggle;
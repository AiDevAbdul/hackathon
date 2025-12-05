import { useEffect } from 'react';

// Component to handle theme persistence across browser sessions
const ThemePersistence = () => {
  useEffect(() => {
    // Load saved theme preference from localStorage
    const savedTheme = localStorage.getItem('theme') || 'system';

    // Apply the theme to the document
    applyTheme(savedTheme);

    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleSystemThemeChange = (e) => {
      if (savedTheme === 'system') {
        const newTheme = e.matches ? 'dark' : 'light';
        document.documentElement.classList.remove('light', 'dark');
        document.documentElement.classList.add(newTheme);
      }
    };

    mediaQuery.addEventListener('change', handleSystemThemeChange);

    // Clean up event listener
    return () => {
      mediaQuery.removeEventListener('change', handleSystemThemeChange);
    };
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

  // This component doesn't render anything, it just handles side effects
  return null;
};

export default ThemePersistence;
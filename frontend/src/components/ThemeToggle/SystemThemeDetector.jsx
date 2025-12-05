import { useEffect } from 'react';

// Component to detect and respond to system theme changes
const SystemThemeDetector = ({ onSystemThemeChange }) => {
  useEffect(() => {
    // Check if the user has explicitly set a theme preference
    const userThemePreference = localStorage.getItem('theme');

    // Only listen to system changes if user has selected 'system' theme
    if (userThemePreference !== 'system') {
      return;
    }

    // Get initial system theme preference
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const initialSystemTheme = mediaQuery.matches ? 'dark' : 'light';

    if (onSystemThemeChange) {
      onSystemThemeChange(initialSystemTheme);
    }

    // Function to handle system theme changes
    const handleSystemThemeChange = (e) => {
      const newSystemTheme = e.matches ? 'dark' : 'light';
      if (onSystemThemeChange) {
        onSystemThemeChange(newSystemTheme);
      }
    };

    // Add event listener for system theme changes
    mediaQuery.addEventListener('change', handleSystemThemeChange);

    // Clean up event listener on unmount
    return () => {
      mediaQuery.removeEventListener('change', handleSystemThemeChange);
    };
  }, [onSystemThemeChange]);

  // This component doesn't render anything, it just handles side effects
  return null;
};

export default SystemThemeDetector;
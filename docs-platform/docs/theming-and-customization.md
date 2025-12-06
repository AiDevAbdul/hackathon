---
sidebar_position: 10
title: "Chapter 10: Theming & Customization"
---

# Chapter 10: Theming & Customization

## Learning Objectives

By the end of this chapter, you will be able to:
- Implement light, dark, and system-default theme options
- Create a theme management system with user preference persistence
- Design accessible themes with proper contrast ratios
- Integrate theme switching with the overall platform
- Customize UI elements based on user preferences
- Implement theme-aware components

## Introduction to Theming in Educational Platforms

Theming is a critical feature for educational platforms, especially for technical subjects that require extended reading sessions. The Physical AI & Humanoid Robotics textbook platform must support multiple themes to accommodate different user preferences, lighting conditions, and accessibility needs.

:::info
**Fun Fact**: Studies show that users can increase their reading time by up to 30% when using a theme that suits their visual preferences and environmental conditions.
:::

### The Importance of Theme Flexibility

Educational platforms face unique theming challenges:

1. **Extended Reading Sessions**: Users often spend hours reading technical content
2. **Variable Lighting Conditions**: From bright daylight to dim nighttime environments
3. **Visual Accessibility**: Supporting users with various visual impairments
4. **Personal Preference**: Different users prefer different visual styles
5. **Focus Requirements**: Some content requires high contrast, others benefit from softer tones

### Theme Categories

```yaml
Theme Types:
  - Light Theme: "Default theme optimized for bright environments"
  - Dark Theme: "Low-light theme with reduced eye strain"
  - System Theme: "Automatic theme based on system preference"
  - High Contrast: "Enhanced contrast for accessibility"
  - Focus Mode: "Minimized distractions for intensive reading"
  - Comfort Mode: "Warm tones to reduce blue light exposure"
```

## Theme Architecture

### Theme Configuration System

```python
from typing import Dict, Literal, Optional
from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel

class ThemeType(str, Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"
    HIGH_CONTRAST = "high_contrast"
    FOCUS_MODE = "focus_mode"
    COMFORT_MODE = "comfort_mode"

class ColorPalette(BaseModel):
    primary: str
    primary_dark: str
    secondary: str
    background: str
    surface: str
    text_primary: str
    text_secondary: str
    text_disabled: str
    border: str
    error: str
    warning: str
    success: str
    info: str

@dataclass
class ThemeConfig:
    name: str
    type: ThemeType
    color_palette: ColorPalette
    typography_scale: float = 1.0
    contrast_level: float = 1.0
    accessibility_features: Dict[str, bool] = None
    is_default: bool = False

class ThemeService:
    def __init__(self):
        self.themes = self._initialize_themes()
        self.user_preferences = {}

    def _initialize_themes(self) -> Dict[ThemeType, ThemeConfig]:
        """Initialize all available themes with their configurations"""
        return {
            ThemeType.LIGHT: ThemeConfig(
                name="Light Theme",
                type=ThemeType.LIGHT,
                color_palette=ColorPalette(
                    primary="#2563eb",
                    primary_dark="#1d4ed8",
                    secondary="#64748b",
                    background="#ffffff",
                    surface="#f8fafc",
                    text_primary="#1e293b",
                    text_secondary="#64748b",
                    text_disabled="#cbd5e1",
                    border="#e2e8f0",
                    error="#dc2626",
                    warning="#f59e0b",
                    success="#16a34a",
                    info="#0ea5e9"
                ),
                is_default=True
            ),
            ThemeType.DARK: ThemeConfig(
                name="Dark Theme",
                type=ThemeType.DARK,
                color_palette=ColorPalette(
                    primary="#3b82f6",
                    primary_dark="#2565c0",
                    secondary="#94a3b8",
                    background="#0f172a",
                    surface="#1e293b",
                    text_primary="#f1f5f9",
                    text_secondary="#cbd5e1",
                    text_disabled="#64748b",
                    border="#334155",
                    error="#f87171",
                    warning="#fbbf24",
                    success="#4ade80",
                    info="#7dd3fc"
                )
            ),
            ThemeType.HIGH_CONTRAST: ThemeConfig(
                name="High Contrast",
                type=ThemeType.HIGH_CONTRAST,
                color_palette=ColorPalette(
                    primary="#0000ff",
                    primary_dark="#0000cc",
                    secondary="#000000",
                    background="#ffffff",
                    surface="#ffffff",
                    text_primary="#000000",
                    text_secondary="#000000",
                    text_disabled="#000000",
                    border="#000000",
                    error="#ff0000",
                    warning="#ffff00",
                    success="#008000",
                    info="#0000ff"
                ),
                contrast_level=1.5
            ),
            ThemeType.FOCUS_MODE: ThemeConfig(
                name="Focus Mode",
                type=ThemeType.FOCUS_MODE,
                color_palette=ColorPalette(
                    primary="#4f46e5",
                    primary_dark="#4338ca",
                    secondary="#d6d3d1",
                    background="#f5f5f4",
                    surface="#f5f5f4",
                    text_primary="#1c1917",
                    text_secondary="#57534e",
                    text_disabled="#a8a29e",
                    border="#e7e5e4",
                    error="#ef4444",
                    warning="#f59e0b",
                    success="#22c55e",
                    info="#0ea5e9"
                ),
                accessibility_features={"minimal_distractions": True, "reduced_animations": True}
            ),
            ThemeType.COMFORT_MODE: ThemeConfig(
                name="Comfort Mode",
                type=ThemeType.COMFORT_MODE,
                color_palette=ColorPalette(
                    primary="#d97706",
                    primary_dark="#b45309",
                    secondary="#a16207",
                    background="#fffbeb",
                    surface="#fef3c7",
                    text_primary="#78350f",
                    text_secondary="#92400e",
                    text_disabled="#f59e0b",
                    border="#fbbf24",
                    error="#dc2626",
                    warning="#d97706",
                    success="#16a34a",
                    info="#0284c7"
                ),
                accessibility_features={"warm_colors": True, "blue_light_reduction": True}
            )
        }

    async def get_user_theme(self, user_id: str) -> ThemeConfig:
        """Get theme configuration for a specific user"""
        if user_id in self.user_preferences:
            user_theme = self.user_preferences[user_id]
        else:
            # Default to system theme which respects OS preferences
            user_theme = ThemeType.SYSTEM

        if user_theme == ThemeType.SYSTEM:
            # Determine theme based on system preference (simplified)
            import platform
            system_theme = self._detect_system_theme()
            return self.themes[system_theme]
        else:
            return self.themes[user_theme]

    def _detect_system_theme(self) -> ThemeType:
        """Detect system theme preference (simplified implementation)"""
        # In a real implementation, this would check OS-level theme settings
        # For now, we'll return light as default
        return ThemeType.LIGHT

    async def set_user_theme(self, user_id: str, theme_type: ThemeType):
        """Set theme preference for a user"""
        self.user_preferences[user_id] = theme_type

        # Log theme change for analytics
        await self._log_theme_change(user_id, theme_type)

    async def _log_theme_change(self, user_id: str, theme_type: ThemeType):
        """Log theme change for analytics and optimization"""
        # Implementation would log to database or analytics system
        pass
```

:::info
**Fun Fact**: The most effective theme systems automatically adapt to ambient lighting conditions and user behavior patterns, switching between themes based on time of day and usage context.
:::

### Theme Context Management

```python
from contextlib import contextmanager
from typing import Generator, Dict
import asyncio

class ThemeContextManager:
    def __init__(self, theme_service: ThemeService):
        self.theme_service = theme_service
        self.active_contexts = {}

    @contextmanager
    def theme_context(self, user_id: str, theme_type: ThemeType) -> Generator[Dict, None, None]:
        """Context manager for temporarily applying a theme"""
        original_theme = self.active_contexts.get(user_id)

        try:
            # Apply new theme
            theme_config = self.theme_service.themes[theme_type]
            self.active_contexts[user_id] = theme_config

            yield self._build_css_variables(theme_config)
        finally:
            # Restore original theme
            if original_theme:
                self.active_contexts[user_id] = original_theme
            else:
                self.active_contexts.pop(user_id, None)

    def _build_css_variables(self, theme_config: ThemeConfig) -> Dict[str, str]:
        """Build CSS variables dictionary from theme configuration"""
        palette = theme_config.color_palette

        css_vars = {
            # Primary colors
            "--color-primary": palette.primary,
            "--color-primary-dark": palette.primary_dark,

            # Secondary colors
            "--color-secondary": palette.secondary,

            # Background colors
            "--color-background": palette.background,
            "--color-surface": palette.surface,

            # Text colors
            "--color-text-primary": palette.text_primary,
            "--color-text-secondary": palette.text_secondary,
            "--color-text-disabled": palette.text_disabled,

            # Border colors
            "--color-border": palette.border,

            # Status colors
            "--color-error": palette.error,
            "--color-warning": palette.warning,
            "--color-success": palette.success,
            "--color-info": palette.info,

            # Typography scale
            "--typography-scale": str(theme_config.typography_scale),

            # Contrast level
            "--contrast-level": str(theme_config.contrast_level)
        }

        return css_vars

    async def get_theme_css(self, user_id: str) -> str:
        """Generate CSS for user's current theme"""
        theme_config = await self.theme_service.get_user_theme(user_id)
        css_vars = self._build_css_variables(theme_config)

        css_content = ":root {\n"
        for var, value in css_vars.items():
            css_content += f"  {var}: {value};\n"
        css_content += "}\n"

        # Add theme-specific overrides
        if theme_config.type == ThemeType.HIGH_CONTRAST:
            css_content += self._get_high_contrast_overrides()
        elif theme_config.type == ThemeType.FOCUS_MODE:
            css_content += self._get_focus_mode_overrides()
        elif theme_config.type == ThemeType.COMFORT_MODE:
            css_content += self._get_comfort_mode_overrides()

        return css_content

    def _get_high_contrast_overrides(self) -> str:
        """Get CSS overrides for high contrast theme"""
        return """
.high-contrast {
  border: 2px solid var(--color-primary) !important;
  text-decoration: underline var(--color-primary) !important;
}
        """

    def _get_focus_mode_overrides(self) -> str:
        """Get CSS overrides for focus mode"""
        return """
.focus-mode {
  animation: none !important;
  transition: none !important;
}
.focus-mode * {
  outline: none !important;
}
.focus-mode .focus-element {
  outline: 2px solid var(--color-primary) !important;
}
        """

    def _get_comfort_mode_overrides(self) -> str:
        """Get CSS overrides for comfort mode"""
        return """
.comfort-mode {
  filter: sepia(20%) hue-rotate(5deg) !important;
}
.comfort-mode img {
  filter: brightness(0.9) contrast(1.1) !important;
}
        """
```

## Frontend Theme Implementation

### React Theme Context

```jsx
// ThemeContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  const [currentTheme, setCurrentTheme] = useState('system');
  const [isInitialized, setIsInitialized] = useState(false);

  // Load user preference from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('preferred-theme');
    if (savedTheme) {
      setCurrentTheme(savedTheme);
    } else {
      // Default to system theme
      setCurrentTheme('system');
    }
    setIsInitialized(true);
  }, []);

  // Apply theme to document
  useEffect(() => {
    if (!isInitialized) return;

    // Remove all theme classes
    document.documentElement.classList.remove('light-theme', 'dark-theme', 'high-contrast-theme', 'focus-mode-theme', 'comfort-mode-theme');

    // Determine actual theme based on system preference if needed
    let actualTheme = currentTheme;
    if (currentTheme === 'system') {
      actualTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    // Apply theme class
    document.documentElement.classList.add(`${actualTheme}-theme`);
    document.documentElement.setAttribute('data-theme', actualTheme);

    // Save preference
    localStorage.setItem('preferred-theme', currentTheme);
  }, [currentTheme, isInitialized]);

  // Listen for system theme changes
  useEffect(() => {
    if (currentTheme !== 'system') return;

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => {
      // Update theme class without changing user preference
      document.documentElement.classList.remove('light-theme', 'dark-theme');
      const newTheme = mediaQuery.matches ? 'dark' : 'light';
      document.documentElement.classList.add(`${newTheme}-theme`);
      document.documentElement.setAttribute('data-theme', newTheme);
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [currentTheme]);

  const setTheme = (theme) => {
    setCurrentTheme(theme);
  };

  const themeConfig = {
    current: currentTheme,
    isDark: currentTheme === 'dark' || (currentTheme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches),
    isLight: currentTheme === 'light' || (currentTheme === 'system' && window.matchMedia('(prefers-color-scheme: light)').matches),
    isHighContrast: currentTheme === 'high_contrast',
    isFocusMode: currentTheme === 'focus_mode',
    isComfortMode: currentTheme === 'comfort_mode'
  };

  const value = {
    ...themeConfig,
    setTheme,
    toggleTheme: () => {
      const themes = ['light', 'dark', 'system'];
      const currentIndex = themes.indexOf(currentTheme);
      const nextIndex = (currentIndex + 1) % themes.length;
      setTheme(themes[nextIndex]);
    }
  };

  if (!isInitialized) {
    return <div>Loading theme...</div>;
  }

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};
```

### Theme Toggle Component

```jsx
// ThemeToggle.jsx
import React from 'react';
import { useTheme } from './ThemeContext';

const ThemeToggle = () => {
  const { current, setTheme, toggleTheme } = useTheme();

  const themeOptions = [
    { value: 'light', label: 'Light', icon: '☀️' },
    { value: 'dark', label: 'Dark', icon: '🌙' },
    { value: 'system', label: 'System', icon: '💻' },
    { value: 'high_contrast', label: 'High Contrast', icon: '🎨' },
    { value: 'focus_mode', label: 'Focus Mode', icon: '🎯' },
    { value: 'comfort_mode', label: 'Comfort Mode', icon: '😌' }
  ];

  return (
    <div className="theme-toggle-container">
      <label htmlFor="theme-select" className="theme-toggle-label">
        Theme:
      </label>
      <select
        id="theme-select"
        value={current}
        onChange={(e) => setTheme(e.target.value)}
        className="theme-select"
        aria-label="Select theme"
      >
        {themeOptions.map((option) => (
          <option key={option.value} value={option.value}>
          {option.icon} {option.label}
        </option>
        ))}
      </select>

      <button
        onClick={toggleTheme}
        className="theme-toggle-button"
        aria-label={`Switch to ${current === 'light' ? 'dark' : 'light'} theme`}
      >
        {current === 'dark' ? '☀️' : '🌙'}
      </button>
    </div>
  );
};

export default ThemeToggle;
```

:::info
**Fun Fact**: Modern theme systems can automatically adjust based on ambient light sensors, time of day, and even user eye strain patterns detected through camera analysis.
:::

## CSS Theme Implementation

### CSS Variables for Theming

```css
/* globals.css - Extended with theme variables */

/* Default (Light) theme variables */
:root {
  --color-primary: #2563eb;
  --color-primary-dark: #1d4ed8;
  --color-secondary: #64748b;
  --color-background: #ffffff;
  --color-surface: #f8fafc;
  --color-text-primary: #1e293b;
  --color-text-secondary: #64748b;
  --color-text-disabled: #cbd5e1;
  --color-border: #e2e8f0;
  --color-error: #dc2626;
  --color-warning: #f59e0b;
  --color-success: #16a34a;
  --color-info: #0ea5e9;
  --typography-scale: 1;
  --contrast-level: 1;
}

/* Dark theme variables */
[data-theme="dark"] {
  --color-primary: #3b82f6;
  --color-primary-dark: #2565c0;
  --color-secondary: #94a3b8;
  --color-background: #0f172a;
  --color-surface: #1e293b;
  --color-text-primary: #f1f5f9;
  --color-text-secondary: #cbd5e1;
  --color-text-disabled: #64748b;
  --color-border: #334155;
  --color-error: #f87171;
  --color-warning: #fbbf24;
  --color-success: #4ade80;
  --color-info: #7dd3fc;
}

/* High contrast theme variables */
[data-theme="high_contrast"] {
  --color-primary: #0000ff;
  --color-primary-dark: #0000cc;
  --color-secondary: #000000;
  --color-background: #ffffff;
  --color-surface: #ffffff;
  --color-text-primary: #000000;
  --color-text-secondary: #000000;
  --color-text-disabled: #000000;
  --color-border: #000000;
  --color-error: #ff0000;
  --color-warning: #ffff00;
  --color-success: #008000;
  --color-info: #0000ff;
  --contrast-level: 1.5;
}

/* Focus mode theme variables */
[data-theme="focus_mode"] {
  --color-primary: #4f46e5;
  --color-primary-dark: #4338ca;
  --color-secondary: #d6d3d1;
  --color-background: #f5f5f4;
  --color-surface: #f5f5f4;
  --color-text-primary: #1c1917;
  --color-text-secondary: #57534e;
  --color-text-disabled: #a8a29e;
  --color-border: #e7e5e4;
  --color-error: #ef4444;
  --color-warning: #f59e0b;
  --color-success: #22c55e;
  --color-info: #0ea5c7;
}

/* Comfort mode theme variables */
[data-theme="comfort_mode"] {
  --color-primary: #d97706;
  --color-primary-dark: #b45309;
  --color-secondary: #a16207;
  --color-background: #fffbeb;
  --color-surface: #fef3c7;
  --color-text-primary: #78350f;
  --color-text-secondary: #92400e;
  --color-text-disabled: #f59e0b;
  --color-border: #fbbf24;
  --color-error: #dc2626;
  --color-warning: #d97706;
  --color-success: #16a34a;
  --color-info: #0284c7;
}

/* Theme-specific component styles */
.textbook-content {
  background-color: var(--color-background);
  color: var(--color-text-primary);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.textbook-content .fun-fact-card {
  background-color: var(--color-surface);
  border-left: 4px solid var(--color-primary);
  color: var(--color-text-primary);
}

.textbook-content .fun-fact-card h4 {
  color: var(--color-primary);
}

/* Reduced motion for focus mode */
[data-theme="focus_mode"] * {
  animation-duration: 0.01ms !important;
  animation-iteration-count: 1 !important;
  transition-duration: 0.01ms !important;
}

/* High contrast adjustments */
[data-theme="high_contrast"] {
  border: 2px solid var(--color-primary);
}

[data-theme="high_contrast"] a {
  text-decoration: underline;
}

[data-theme="high_contrast"] button,
[data-theme="high_contrast"] input,
[data-theme="high_contrast"] select {
  border: 2px solid var(--color-border);
}

/* Comfort mode adjustments */
[data-theme="comfort_mode"] {
  filter: sepia(10%) hue-rotate(5deg);
}

[data-theme="comfort_mode"] img {
  filter: brightness(0.95) contrast(1.05);
}
```

## Theme API Integration

### Backend Theme API

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

theme_router = APIRouter(prefix="/themes", tags=["themes"])

class ThemePreference(BaseModel):
    theme_type: ThemeType
    contrast_level: Optional[float] = 1.0
    typography_scale: Optional[float] = 1.0

@theme_router.get("/available")
async def get_available_themes():
    """Get list of all available themes"""
    theme_service = ThemeService()

    themes_info = []
    for theme_type, theme_config in theme_service.themes.items():
        themes_info.append({
            "type": theme_type.value,
            "name": theme_config.name,
            "is_default": theme_config.is_default,
            "has_accessibility_features": bool(theme_config.accessibility_features)
        })

    return {"themes": themes_info}

@theme_router.get("/user/{user_id}")
async def get_user_theme(
    user_id: str,
    current_user = Depends(get_current_user)
):
    """Get current user's theme preference"""
    if current_user.id != user_id and not current_user.has_role('admin'):
        raise HTTPException(status_code=403, detail="Not authorized to view this user's preferences")

    theme_service = ThemeService()
    user_theme = await theme_service.get_user_theme(user_id)

    return {
        "current_theme": user_theme.type.value,
        "theme_config": {
            "name": user_theme.name,
            "color_palette": user_theme.color_palette.dict(),
            "typography_scale": user_theme.typography_scale,
            "contrast_level": user_theme.contrast_level,
            "accessibility_features": user_theme.accessibility_features or {}
        }
    }

@theme_router.post("/user/{user_id}/preference")
async def set_user_theme_preference(
    user_id: str,
    preference: ThemePreference,
    current_user = Depends(get_current_user)
):
    """Set user's theme preference"""
    if current_user.id != user_id and not current_user.has_role('admin'):
        raise HTTPException(status_code=403, detail="Not authorized to modify this user's preferences")

    if preference.theme_type not in ThemeType.__members__.values():
        raise HTTPException(status_code=400, detail="Invalid theme type")

    theme_service = ThemeService()
    await theme_service.set_user_theme(user_id, preference.theme_type)

    # Update additional settings
    # In a real implementation, these would be stored in user preferences

    return {"message": "Theme preference updated successfully", "theme": preference.theme_type.value}

@theme_router.get("/css/{user_id}")
async def get_user_theme_css(
    user_id: str,
    current_user = Depends(get_current_user)
):
    """Get CSS for user's current theme"""
    if current_user.id != user_id and not current_user.has_role('admin'):
        raise HTTPException(status_code=403, detail="Not authorized to access this user's theme CSS")

    theme_context_manager = ThemeContextManager(ThemeService())
    css_content = await theme_context_manager.get_theme_css(user_id)

    return {"css": css_content, "content-type": "text/css"}

@theme_router.get("/system-detection")
async def detect_system_theme():
    """Detect system theme preference"""
    theme_service = ThemeService()
    system_theme = theme_service._detect_system_theme()

    return {"system_theme": system_theme.value, "is_dark": system_theme == ThemeType.DARK}
```

## Accessibility Considerations

### WCAG Compliance for Themes

```python
class AccessibilityThemeValidator:
    def __init__(self):
        self.min_contrast_ratios = {
            "large_text": 3.0,  # For text 18pt+ or 14pt+ bold
            "normal_text": 4.5, # For normal text
            "enhanced": 7.0     # For enhanced contrast
        }

    def validate_theme_accessibility(self, theme_config: ThemeConfig) -> Dict[str, any]:
        """Validate that theme meets accessibility standards"""
        palette = theme_config.color_palette
        results = {
            "is_accessible": True,
            "violations": [],
            "suggestions": [],
            "contrast_ratios": {}
        }

        # Check text-background contrast
        normal_text_ratio = self._calculate_contrast_ratio(
            palette.text_primary,
            palette.background
        )
        results["contrast_ratios"]["text_background_normal"] = normal_text_ratio

        if normal_text_ratio < self.min_contrast_ratios["normal_text"]:
            results["violations"].append(
                f"Normal text contrast ratio ({normal_text_ratio:.2f}) below minimum ({self.min_contrast_ratios['normal_text']})"
            )
            results["is_accessible"] = False

        large_text_ratio = self._calculate_contrast_ratio(
            palette.text_secondary,
            palette.background
        )
        results["contrast_ratios"]["text_background_large"] = large_text_ratio

        if large_text_ratio < self.min_contrast_ratios["large_text"]:
            results["violations"].append(
                f"Large text contrast ratio ({large_text_ratio:.2f}) below minimum ({self.min_contrast_ratios['large_text']})"
            )
            results["is_accessible"] = False

        # Check primary color contrast for interactive elements
        primary_contrast = self._calculate_contrast_ratio(
            palette.primary,
            palette.background
        )
        results["contrast_ratios"]["primary_background"] = primary_contrast

        if primary_contrast < self.min_contrast_ratios["normal_text"]:
            results["suggestions"].append(
                "Consider adjusting primary color for better contrast against background"
            )

        return results

    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB values"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _relative_luminance(self, r: int, g: int, b: int) -> float:
        """Calculate relative luminance for contrast ratio calculation"""
        def srgb_to_linear(color_component):
            color = color_component / 255.0
            if color <= 0.03928:
                return color / 12.92
            else:
                return ((color + 0.055) / 1.055) ** 2.4

        r_linear = srgb_to_linear(r)
        g_linear = srgb_to_linear(g)
        b_linear = srgb_to_linear(b)

        return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear

    def _calculate_contrast_ratio(self, color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors"""
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)

        lum1 = self._relative_luminance(r1, g1, b1)
        lum2 = self._relative_luminance(r2, g2, b2)

        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)

        contrast_ratio = (lighter + 0.05) / (darker + 0.05)
        return contrast_ratio

    def get_accessibility_features(self, theme_type: ThemeType) -> List[str]:
        """Get accessibility features enabled by specific theme"""
        features = {
            ThemeType.HIGH_CONTRAST: [
                "Enhanced contrast ratios",
                "Bold text emphasis",
                "Clear visual separation",
                "Improved readability"
            ],
            ThemeType.FOCUS_MODE: [
                "Reduced visual distractions",
                "Minimized animations",
                "Enhanced focus indicators",
                "Streamlined interface"
            ],
            ThemeType.COMFORT_MODE: [
                "Reduced blue light emission",
                "Warm color temperature",
                "Softer visual experience",
                "Eye strain reduction"
            ]
        }

        return features.get(theme_type, [])
```

:::info
**Fun Fact**: WCAG 2.1 guidelines require a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text to ensure readability for users with visual impairments.
:::

## Performance Optimization

### Theme Switching Performance

```python
import time
from functools import wraps

class ThemePerformanceOptimizer:
    def __init__(self):
        self.theme_cache = {}
        self.performance_metrics = {}

    def cache_theme_result(func):
        """Decorator to cache theme computation results"""
        @wraps(func)
        async def wrapper(self, user_id: str, *args, **kwargs):
            cache_key = f"{func.__name__}:{user_id}:{hash(str(args))}:{hash(str(sorted(kwargs.items())))}"

            if cache_key in self.theme_cache:
                result, timestamp, access_count = self.theme_cache[cache_key]

                # Update access count
                self.theme_cache[cache_key] = (result, timestamp, access_count + 1)

                # Track performance
                if func.__name__ not in self.performance_metrics:
                    self.performance_metrics[func.__name__] = {"cache_hits": 0, "cache_misses": 0}
                self.performance_metrics[func.__name__]["cache_hits"] += 1

                return result

            # Cache miss - compute result
            start_time = time.time()
            result = await func(self, user_id, *args, **kwargs)
            compute_time = time.time() - start_time

            # Cache the result
            self.theme_cache[cache_key] = (result, time.time(), 1)

            # Track performance
            if func.__name__ not in self.performance_metrics:
                self.performance_metrics[func.__name__] = {"cache_hits": 0, "cache_misses": 0}
            self.performance_metrics[func.__name__]["cache_misses"] += 1

            return result
        return wrapper

    @cache_theme_result
    async def get_optimized_user_theme(self, user_id: str) -> ThemeConfig:
        """Get user theme with caching optimization"""
        theme_service = ThemeService()
        return await theme_service.get_user_theme(user_id)

    async def get_theme_switching_performance(self) -> Dict[str, any]:
        """Get performance metrics for theme switching"""
        total_requests = 0
        total_cache_hits = 0

        for func_name, metrics in self.performance_metrics.items():
            total_requests += metrics["cache_hits"] + metrics["cache_misses"]
            total_cache_hits += metrics["cache_hits"]

        cache_hit_rate = total_cache_hits / total_requests if total_requests > 0 else 0

        return {
            "cache_hit_rate": cache_hit_rate,
            "total_requests": total_requests,
            "cache_hits": total_cache_hits,
            "cache_misses": total_requests - total_cache_hits,
            "function_metrics": self.performance_metrics
        }

    def preload_common_themes(self):
        """Preload commonly used themes to improve performance"""
        # Preload light and dark themes since they're most commonly used
        light_theme = self.themes[ThemeType.LIGHT]
        dark_theme = self.themes[ThemeType.DARK]

        # Pre-compute CSS variables for common themes
        light_css = self._build_css_variables(light_theme)
        dark_css = self._build_css_variables(dark_theme)

        # Cache the computed values
        self.theme_cache[f"css:{ThemeType.LIGHT.value}"] = (light_css, time.time(), 999999)
        self.theme_cache[f"css:{ThemeType.DARK.value}"] = (dark_css, time.time(), 999999)

class OptimizedThemeService(ThemeService):
    def __init__(self):
        super().__init__()
        self.optimizer = ThemePerformanceOptimizer()
        self.optimizer.preload_common_themes()

    async def get_user_theme(self, user_id: str) -> ThemeConfig:
        """Get user theme with performance optimization"""
        return await self.optimizer.get_optimized_user_theme(user_id)
```

## Theme Integration with Other Features

### Integration with Personalization

```python
class ThemePersonalizationIntegrator:
    def __init__(self, theme_service: ThemeService, personalization_service):
        self.theme_service = theme_service
        self.personalization_service = personalization_service

    async def get_contextual_theme(self, user_id: str, context: Dict[str, any] = None) -> ThemeConfig:
        """Get theme based on user preferences and current context"""
        user_theme = await self.theme_service.get_user_theme(user_id)

        # Adjust theme based on context
        if context:
            # Adjust for time of day
            if 'time_of_day' in context:
                if context['time_of_day'] == 'night' and user_theme.type == ThemeType.SYSTEM:
                    # Suggest dark theme for night time
                    user_theme = self.theme_service.themes[ThemeType.DARK]
                elif context['time_of_day'] == 'day' and user_theme.type == ThemeType.SYSTEM:
                    # Suggest light theme for day time
                    user_theme = self.theme_service.themes[ThemeType.LIGHT]

            # Adjust for ambient lighting (if available)
            if 'ambient_light_level' in context:
                light_level = context['ambient_light_level']
                if light_level < 50 and user_theme.type in [ThemeType.LIGHT, ThemeType.SYSTEM]:
                    # Low light - suggest dark or comfort mode
                    if await self._user_prefers_comfort_mode(user_id):
                        user_theme = self.theme_service.themes[ThemeType.COMFORT_MODE]
                    else:
                        user_theme = self.theme_service.themes[ThemeType.DARK]
                elif light_level > 200 and user_theme.type == ThemeType.DARK:
                    # Very bright - suggest light theme
                    user_theme = self.theme_service.themes[ThemeType.LIGHT]

        return user_theme

    async def _user_prefers_comfort_mode(self, user_id: str) -> bool:
        """Check if user has indicated preference for comfort mode"""
        user_profile = await self.personalization_service.get_user_profile(user_id)
        return user_profile.get('prefers_comfort_mode', False)

    async def get_adaptive_theme_recommendation(self, user_id: str) -> Dict[str, any]:
        """Provide adaptive theme recommendation based on user behavior"""
        # Analyze user's theme switching patterns
        theme_history = await self._get_user_theme_history(user_id)

        # Identify patterns (e.g., prefers dark at night, light during day)
        patterns = self._analyze_theme_patterns(theme_history)

        recommendation = {
            "recommended_theme": self._get_pattern_based_recommendation(patterns),
            "confidence": self._calculate_recommendation_confidence(patterns),
            "reasoning": self._generate_recommendation_reasoning(patterns)
        }

        return recommendation

    async def _get_user_theme_history(self, user_id: str) -> List[Dict[str, any]]:
        """Get user's theme switching history"""
        # This would query the database for theme change events
        # For now, returning empty list
        return []

    def _analyze_theme_patterns(self, theme_history: List[Dict]) -> Dict[str, any]:
        """Analyze patterns in user's theme preferences"""
        # Analyze temporal patterns, context patterns, etc.
        patterns = {
            "time_based_preferences": {},
            "context_correlations": {},
            "switching_frequency": len(theme_history)
        }

        return patterns

    def _get_pattern_based_recommendation(self, patterns: Dict) -> ThemeType:
        """Get theme recommendation based on patterns"""
        # For now, return system theme as default
        return ThemeType.SYSTEM

    def _calculate_recommendation_confidence(self, patterns: Dict) -> float:
        """Calculate confidence in recommendation"""
        # Based on amount of data and consistency of patterns
        return 0.5  # Default medium confidence

    def _generate_recommendation_reasoning(self, patterns: Dict) -> str:
        """Generate human-readable explanation for recommendation"""
        return "Based on system default and user preference patterns"
```

:::info
**Fun Fact**: The most sophisticated theme systems adapt not only to user preferences but also to ambient conditions, reading patterns, and even biometric data like eye strain indicators.
:::

## Summary

Theming and customization are essential for creating an inclusive and accessible educational platform. The Physical AI & Humanoid Robotics textbook platform implements a comprehensive theme system that supports multiple theme types, respects user preferences, and maintains accessibility standards. The system includes light, dark, high-contrast, focus, and comfort modes to accommodate various user needs and environmental conditions.

:::info
**Fun Fact**: The most effective theme systems learn from user behavior and automatically adjust settings to optimize for comfort, readability, and engagement over time.
:::

## Key Terms

- **Theme System**: Collection of visual styles that can be applied to the UI
- **CSS Variables**: Custom properties for dynamic theme management
- **WCAG Compliance**: Web Content Accessibility Guidelines standards
- **Contrast Ratio**: Measure of readability between text and background
- **System Theme**: Theme that follows the user's OS-level preferences
- **High Contrast Mode**: Enhanced visual distinction for accessibility
- **Focus Mode**: Minimized distractions for intensive reading
- **Comfort Mode**: Reduced eye strain with warm color tones
- **Theme Persistence**: Saving user theme preferences across sessions
- **Accessibility Features**: Elements that improve usability for users with disabilities
- **Color Palette**: Set of colors used in a theme
- **Typography Scale**: Relative sizing of text elements
- **Theme Context**: React context for theme state management
- **Theme Toggle**: UI element for switching between themes
- **Performance Optimization**: Techniques to improve theme switching speed
- **Contextual Theming**: Themes that adapt based on environmental factors

## Exercises

1. Implement a new theme type for the textbook platform
2. Add accessibility validation to the theme system
3. Create a theme preview feature for users
4. Implement automatic theme switching based on time of day

---
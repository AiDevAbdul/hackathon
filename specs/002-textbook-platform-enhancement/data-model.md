# Data Model: Physical AI & Humanoid Robotics Textbook Platform Enhancement

**Feature**: 002-textbook-platform-enhancement
**Date**: 2025-12-05
**Status**: Completed

## Entities

### User
Represents a student or educator with authentication credentials, background information, preferences, and learning progress.

**Fields**:
- `id` (string, primary key): Unique identifier for the user
- `email` (string, required): User's email address for authentication
- `password_hash` (string, required): Hashed password for secure authentication
- `name` (string, required): User's full name
- `role` (string, required): User role (student, educator, admin)
- `background_software` (string, optional): User's software experience level
- `background_hardware` (string, optional): User's hardware experience level
- `created_at` (datetime, required): Account creation timestamp
- `updated_at` (datetime, required): Last update timestamp
- `last_login` (datetime, optional): Last login timestamp
- `is_active` (boolean, required): Account active status

**Validation Rules**:
- Email must be valid email format
- Password must meet security requirements (min 8 chars, mixed case, numbers)
- Role must be one of: 'student', 'educator', 'admin'

### TextbookContent
Represents the Physical AI & Humanoid Robotics course material with chapters, sections, and learning modules.

**Fields**:
- `id` (string, primary key): Unique identifier for the content
- `title` (string, required): Title of the chapter/section
- `slug` (string, required, unique): URL-friendly identifier
- `content` (text, required): Main content in markdown format
- `content_ur` (text, optional): Urdu translation of content
- `chapter_number` (integer, required): Chapter sequence number
- `section_number` (integer, optional): Section sequence number within chapter
- `level` (string, required): Content difficulty level (beginner, intermediate, advanced)
- `prerequisites` (json, optional): List of prerequisite content IDs
- `learning_objectives` (json, required): List of learning objectives
- `created_at` (datetime, required): Content creation timestamp
- `updated_at` (datetime, required): Last update timestamp
- `is_published` (boolean, required): Content publication status

**Validation Rules**:
- Title must be 1-200 characters
- Slug must be unique and URL-friendly
- Content must be non-empty when published

### PersonalizationProfile
Represents user-specific settings and preferences that modify content presentation based on background.

**Fields**:
- `id` (string, primary key): Unique identifier for the profile
- `user_id` (string, required, foreign key): Reference to User
- `content_level_preference` (string, optional): Preferred content difficulty
- `example_preference` (string, optional): Preferred example types (theoretical, practical)
- `detail_preference` (string, optional): Detail level preference (concise, detailed)
- `learning_path` (json, optional): Customized learning path
- `created_at` (datetime, required): Profile creation timestamp
- `updated_at` (datetime, required): Last update timestamp

**Validation Rules**:
- User_id must reference an existing user
- Preferences must be from predefined options

### TranslationCache
Represents cached translated content for efficient language switching.

**Fields**:
- `id` (string, primary key): Unique identifier for the cache entry
- `content_id` (string, required, foreign key): Reference to TextbookContent
- `target_language` (string, required): Target language code (e.g., 'ur' for Urdu)
- `translated_content` (text, required): Translated content
- `confidence_score` (float, optional): Translation quality confidence score
- `created_at` (datetime, required): Cache creation timestamp
- `updated_at` (datetime, required): Last update timestamp
- `expires_at` (datetime, required): Cache expiration timestamp

**Validation Rules**:
- Content_id must reference an existing textbook content
- Target language must be supported language code
- Confidence score must be between 0 and 1

### ThemePreference
Represents user's selected display theme (light/dark/system-default).

**Fields**:
- `id` (string, primary key): Unique identifier for the preference
- `user_id` (string, required, foreign key): Reference to User
- `theme_mode` (string, required): Theme selection (light, dark, system)
- `created_at` (datetime, required): Preference creation timestamp
- `updated_at` (datetime, required): Last update timestamp

**Validation Rules**:
- User_id must reference an existing user
- Theme_mode must be one of: 'light', 'dark', 'system'

### FunFactCard
Represents engaging supplementary content that enhances learning in each chapter.

**Fields**:
- `id` (string, primary key): Unique identifier for the card
- `content_id` (string, required, foreign key): Reference to TextbookContent
- `title` (string, required): Title of the fun fact
- `description` (text, required): Detailed fun fact content
- `category` (string, required): Category (historical, technical, application)
- `difficulty_level` (string, required): Related difficulty level
- `created_at` (datetime, required): Card creation timestamp
- `updated_at` (datetime, required): Last update timestamp
- `is_active` (boolean, required): Card active status

**Validation Rules**:
- Content_id must reference an existing textbook content
- Category must be one of: 'historical', 'technical', 'application'
- Title must be 1-100 characters

### UserProgress
Represents user's progress through the textbook content.

**Fields**:
- `id` (string, primary key): Unique identifier for the progress record
- `user_id` (string, required, foreign key): Reference to User
- `content_id` (string, required, foreign key): Reference to TextbookContent
- `status` (string, required): Progress status (not_started, in_progress, completed)
- `completion_percentage` (float, required): Completion percentage (0-100)
- `time_spent_seconds` (integer, optional): Time spent on content in seconds
- `last_accessed` (datetime, required): Last access timestamp
- `notes` (text, optional): User notes about the content
- `created_at` (datetime, required): Record creation timestamp
- `updated_at` (datetime, required): Last update timestamp

**Validation Rules**:
- User_id must reference an existing user
- Content_id must reference an existing textbook content
- Status must be one of: 'not_started', 'in_progress', 'completed'
- Completion_percentage must be between 0 and 100

## Relationships

- User 1:M PersonalizationProfile (one user has one personalization profile)
- User 1:M ThemePreference (one user has one theme preference)
- User 1:M UserProgress (one user has many progress records)
- TextbookContent 1:M UserProgress (one content has many progress records)
- TextbookContent 1:M FunFactCard (one content has many fun fact cards)
- TextbookContent 1:M TranslationCache (one content has many cached translations)

## State Transitions

### UserProgress Status Transitions
- `not_started` → `in_progress`: User begins engaging with content
- `in_progress` → `completed`: User completes content
- `completed` → `in_progress`: User revisits content
- `in_progress` → `not_started`: User resets progress

## Indexes

- User: email (unique)
- TextbookContent: slug (unique), chapter_number, is_published
- PersonalizationProfile: user_id (unique)
- TranslationCache: content_id + target_language (unique)
- ThemePreference: user_id (unique)
- FunFactCard: content_id, is_active
- UserProgress: user_id + content_id (unique)
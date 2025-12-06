---
description: "Data model for dual-platform textbook system"
---

# Data Model: Physical AI & Humanoid Robotics Textbook Platform

**Feature**: 003-dual-platform-setup
**Date**: 2025-12-06
**Status**: Final
**Input**: Feature specification from `/specs/[003-dual-platform-setup]/spec.md`

## Entities

### User
Represents a student or educator using the Physical AI & Humanoid Robotics textbook platform.

**Attributes**:
- `id` (UUID, required): Unique identifier for the user
- `email` (string, required): User's email address for authentication
- `password_hash` (string, required): Hashed password for secure authentication
- `name` (string, required): User's full name
- `role` (enum, required): User role ('student', 'educator', 'admin')
- `background_software` (string, optional): User's software development background
- `background_hardware` (string, optional): User's hardware/robotics background
- `created_at` (datetime, required): Account creation timestamp
- `updated_at` (datetime, required): Last update timestamp
- `last_login` (datetime, optional): Last login timestamp
- `is_active` (boolean, required): Account active status

**Relationships**:
- 1 User → M UserProgress (user's progress records)
- 1 User → 1 PersonalizationProfile (user's personalization settings)
- 1 User → 1 ThemePreference (user's theme preferences)

**Validation Rules**:
- Email must be valid email format
- Password must meet security requirements (min 8 chars, mixed case, numbers)
- Role must be one of: 'student', 'educator', 'admin'
- Name must be 1-100 characters

### TextbookContent
Represents the Physical AI & Humanoid Robotics course material with chapters, sections, and learning modules.

**Attributes**:
- `id` (UUID, required): Unique identifier for the content
- `title` (string, required): Title of the chapter/section
- `slug` (string, required, unique): URL-friendly identifier
- `content` (text, required): Main content in markdown format
- `content_ur` (text, optional): Urdu translation of content
- `chapter_number` (integer, required): Chapter sequence number
- `section_number` (integer, optional): Section sequence number within chapter
- `level` (enum, required): Content difficulty level ('beginner', 'intermediate', 'advanced')
- `prerequisites` (json, optional): List of prerequisite content IDs
- `learning_objectives` (json, required): List of learning objectives
- `created_at` (datetime, required): Content creation timestamp
- `updated_at` (datetime, required): Last update timestamp
- `is_published` (boolean, required): Content publication status

**Relationships**:
- 1 TextbookContent → M UserProgress (progress records for this content)
- 1 TextbookContent → M FunFactCard (fun fact cards for this content)
- 1 TextbookContent → M TranslationCache (cached translations for this content)

**Validation Rules**:
- Title must be 1-200 characters
- Slug must be unique and URL-friendly
- Content must be non-empty when published
- Chapter number must be positive
- Level must be one of: 'beginner', 'intermediate', 'advanced'

### PersonalizationProfile
Represents user-specific settings and preferences that modify content presentation based on background.

**Attributes**:
- `id` (UUID, required): Unique identifier for the profile
- `user_id` (UUID, required, foreign key): Reference to User
- `content_level_preference` (enum, optional): Preferred content difficulty ('beginner', 'intermediate', 'advanced')
- `example_preference` (enum, optional): Preferred example types ('theoretical', 'practical', 'balanced')
- `detail_preference` (enum, optional): Detail level preference ('concise', 'detailed', 'balanced')
- `learning_path` (json, optional): Customized learning path
- `created_at` (datetime, required): Profile creation timestamp
- `updated_at` (datetime, required): Last update timestamp

**Relationships**:
- M PersonalizationProfile → 1 User (many profiles to one user - for history)
- 1 PersonalizationProfile → M UserProgress (progress records using this profile)

**Validation Rules**:
- User_id must reference an existing user
- Preferences must be from predefined options
- Learning path must follow expected structure

### TranslationCache
Represents cached translated content for efficient language switching.

**Attributes**:
- `id` (UUID, required): Unique identifier for the cache entry
- `content_id` (UUID, required, foreign key): Reference to TextbookContent
- `target_language` (string, required): Target language code (e.g., 'ur' for Urdu)
- `translated_content` (text, required): Translated content
- `confidence_score` (float, optional): Translation quality confidence score (0-1)
- `created_at` (datetime, required): Cache creation timestamp
- `updated_at` (datetime, required): Last update timestamp
- `expires_at` (datetime, required): Cache expiration timestamp

**Relationships**:
- 1 TranslationCache → 1 TextbookContent (one translation to one content)
- 1 TranslationCache → M UserProgress (progress records with this translation)

**Validation Rules**:
- Content_id must reference an existing textbook content
- Target language must be supported language code
- Confidence score must be between 0 and 1
- Expires_at must be after created_at

### ThemePreference
Represents user's selected display theme (light/dark/system-default).

**Attributes**:
- `id` (UUID, required): Unique identifier for the preference
- `user_id` (UUID, required, foreign key): Reference to User
- `theme_mode` (enum, required): Theme selection ('light', 'dark', 'system', 'high_contrast', 'focus_mode', 'comfort_mode')
- `created_at` (datetime, required): Preference creation timestamp
- `updated_at` (datetime, required): Last update timestamp

**Relationships**:
- 1 ThemePreference → 1 User (one preference per user)

**Validation Rules**:
- User_id must reference an existing user
- Theme_mode must be one of: 'light', 'dark', 'system', 'high_contrast', 'focus_mode', 'comfort_mode'

### FunFactCard
Represents engaging supplementary content that enhances learning in each chapter.

**Attributes**:
- `id` (UUID, required): Unique identifier for the card
- `content_id` (UUID, required, foreign key): Reference to TextbookContent
- `title` (string, required): Title of the fun fact
- `description` (text, required): Detailed fun fact content
- `category` (enum, required): Category ('historical', 'technical', 'application', 'comparison', 'trivia', 'milestone')
- `difficulty_level` (enum, required): Related difficulty level ('beginner', 'intermediate', 'advanced')
- `position` (enum, required): Display position ('inline', 'sidebar', 'popup', 'floating')
- `created_at` (datetime, required): Card creation timestamp
- `updated_at` (datetime, required): Last update timestamp
- `is_active` (boolean, required): Card active status

**Relationships**:
- 1 FunFactCard → 1 TextbookContent (one card to one content)
- M FunFactCard → M UserProgress (multiple cards associated with progress)

**Validation Rules**:
- Content_id must reference an existing textbook content
- Category must be one of: 'historical', 'technical', 'application', 'comparison', 'trivia', 'milestone'
- Title must be 1-100 characters
- Position must be one of: 'inline', 'sidebar', 'popup', 'floating'

### UserProgress
Represents user's progress through the textbook content.

**Attributes**:
- `id` (UUID, required): Unique identifier for the progress record
- `user_id` (UUID, required, foreign key): Reference to User
- `content_id` (UUID, required, foreign key): Reference to TextbookContent
- `status` (enum, required): Progress status ('not_started', 'in_progress', 'completed')
- `completion_percentage` (float, required): Completion percentage (0-100)
- `time_spent_seconds` (integer, optional): Time spent on content in seconds
- `last_accessed` (datetime, required): Last access timestamp
- `notes` (text, optional): User notes about the content
- `quiz_scores` (json, optional): Scores for related quizzes
- `created_at` (datetime, required): Record creation timestamp
- `updated_at` (datetime, required): Last update timestamp

**Relationships**:
- 1 UserProgress → 1 User (one progress record to one user)
- 1 UserProgress → 1 TextbookContent (one progress record to one content)
- 1 UserProgress → 1 PersonalizationProfile (using specific profile)
- 1 UserProgress → 1 TranslationCache (using specific translation)

**Validation Rules**:
- User_id must reference an existing user
- Content_id must reference an existing textbook content
- Status must be one of: 'not_started', 'in_progress', 'completed'
- Completion_percentage must be between 0 and 100

## Entity Relationships

### User Relationships
```
User (1) -- (M) UserProgress
User (1) -- (1) PersonalizationProfile
User (1) -- (1) ThemePreference
```

### Content Relationships
```
TextbookContent (1) -- (M) UserProgress
TextbookContent (1) -- (M) FunFactCard
TextbookContent (1) -- (M) TranslationCache
```

### Progress Relationships
```
UserProgress (M) -- (1) PersonalizationProfile
UserProgress (M) -- (1) TranslationCache
```

## Data Validation Rules

### Business Logic Constraints
1. **User Background Consistency**: A user's software and hardware backgrounds should be related to their role
2. **Content Ordering**: Chapters should follow sequential numbering with proper prerequisites
3. **Translation Freshness**: Cached translations should be refreshed when original content changes
4. **Progress Tracking**: A user's progress on a content item should not exceed 100% completion
5. **Quiz Dependencies**: Users should complete prerequisite content before taking advanced quizzes

### Performance Considerations
1. **Indexing**: TextbookContent.slug and User.email should be indexed for fast lookups
2. **Partitioning**: UserProgress records could be partitioned by user_id for better performance
3. **Caching**: TranslationCache entries should have appropriate TTL settings
4. **Archiving**: Old UserProgress records could be archived to maintain performance

## API Contract Implications

### Authentication & User Management
- User creation, login, and profile management endpoints
- Background information collection during registration
- Session management and JWT token handling

### Content Management
- TextbookContent CRUD operations with publishing controls
- Translation endpoints for language switching
- Content personalization based on user profile

### Progress Tracking
- UserProgress tracking for learning analytics
- Quiz scoring and completion tracking
- Achievement and milestone tracking

### Engagement Features
- FunFactCard display and interaction tracking
- Theme preference persistence across sessions
- Personalization profile management

## Database Schema

### PostgreSQL Tables
```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL,
  background_software TEXT,
  background_hardware TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_login TIMESTAMP WITH TIME ZONE,
  is_active BOOLEAN DEFAULT TRUE
);

-- Textbook content table
CREATE TABLE textbook_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  content TEXT NOT NULL,
  content_ur TEXT,
  chapter_number INTEGER NOT NULL,
  section_number INTEGER,
  level VARCHAR(20) NOT NULL,
  prerequisites JSONB,
  learning_objectives JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  is_published BOOLEAN DEFAULT FALSE
);

-- User progress table
CREATE TABLE user_progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  content_id UUID REFERENCES textbook_content(id) ON DELETE CASCADE,
  status VARCHAR(20) NOT NULL,
  completion_percentage DECIMAL(5,2) NOT NULL,
  time_spent_seconds INTEGER,
  last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  notes TEXT,
  quiz_scores JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, content_id)
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_textbook_content_slug ON textbook_content(slug);
CREATE INDEX idx_textbook_content_chapter ON textbook_content(chapter_number);
CREATE INDEX idx_user_progress_user_content ON user_progress(user_id, content_id);
CREATE INDEX idx_user_progress_status ON user_progress(status);
```

## Vector Database Schema (Qdrant)

For the RAG (Retrieval-Augmented Generation) functionality:

```python
# Collection configuration for Qdrant
collection_config = {
    "collection_name": "textbook_content_vectors",
    "vector_size": 1536,  # Size of OpenAI embeddings
    "distance": "Cosine",
    "hnsw_config": {
        "m": 16,
        "ef_construct": 100
    },
    "optimizers_config": {
        "deleted_threshold": 0.2,
        "vacuum_min_vector_number": 1000
    }
}

# Payload schema
payload_schema = {
    "content_id": "keyword",      # Reference to textbook_content.id
    "chapter_number": "integer",  # For filtering by chapter
    "section_number": "integer",  # For filtering by section
    "level": "keyword",           # Content difficulty level
    "category": "keyword"         # Content category for filtering
}
```

## Data Migration Considerations

### Initial Setup
1. **User Migration**: Create default admin user for content management
2. **Content Migration**: Import initial textbook content with proper slugs and metadata
3. **Fun Fact Cards**: Populate with engaging facts for each chapter
4. **Translation Cache**: Pre-populate with common content translations

### Future Migrations
1. **Schema Evolution**: Plan for backward-compatible changes
2. **Data Integrity**: Maintain referential integrity during migrations
3. **Performance**: Optimize queries during schema changes
4. **Rollback Strategy**: Ensure migrations can be safely rolled back
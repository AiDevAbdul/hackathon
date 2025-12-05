import React, { useState, useEffect } from 'react';
import UserPreferencesService from '../../services/userPreferencesService';

const ContentAdapter = ({ content, contentType = 'textbook' }) => {
  const [userProfile, setUserProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [adaptedContent, setAdaptedContent] = useState(content);

  useEffect(() => {
    loadUserProfile();
  }, []);

  useEffect(() => {
    if (userProfile) {
      adaptContent();
    }
  }, [userProfile, content]);

  const loadUserProfile = async () => {
    try {
      setIsLoading(true);
      const profile = await UserPreferencesService.getPersonalizationProfile();
      setUserProfile(profile);
    } catch (err) {
      console.error('Failed to load user profile:', err);
      // Continue with default content if profile loading fails
      setUserProfile(null);
    } finally {
      setIsLoading(false);
    }
  };

  const adaptContent = () => {
    if (!userProfile || !content) {
      setAdaptedContent(content);
      return;
    }

    let adapted = content;

    // Adjust content based on user's preferred level
    if (userProfile.content_level_preference) {
      switch (userProfile.content_level_preference) {
        case 'beginner':
          // Simplify content for beginners
          adapted = addBeginnerAnnotations(content);
          break;
        case 'advanced':
          // Add more depth for advanced users
          adapted = addAdvancedDetails(content);
          break;
        default:
          // Intermediate level remains as is
          adapted = content;
      }
    }

    // Adjust examples based on user's preference
    if (userProfile.example_preference) {
      switch (userProfile.example_preference) {
        case 'practical':
          adapted = addPracticalExamples(adapted);
          break;
        case 'theoretical':
          adapted = addTheoreticalExamples(adapted);
          break;
      }
    }

    // Adjust detail level based on user's preference
    if (userProfile.detail_preference) {
      switch (userProfile.detail_preference) {
        case 'concise':
          adapted = makeConcise(adapted);
          break;
        case 'detailed':
          adapted = addDetails(adapted);
          break;
      }
    }

    setAdaptedContent(adapted);
  };

  // Helper functions to adapt content
  const addBeginnerAnnotations = (content) => {
    return `📝 Beginner Level: ${content}`;
  };

  const addAdvancedDetails = (content) => {
    return `${content} 🔍 [Detailed Analysis: This concept involves advanced principles...]`;
  };

  const addPracticalExamples = (content) => {
    return `${content} 💡 Practical Example: This concept applies to real-world scenario X...`;
  };

  const addTheoreticalExamples = (content) => {
    return `${content} 🧠 Theoretical Example: This concept relates to theory Y...`;
  };

  const makeConcise = (content) => {
    // In a real implementation, this would summarize or highlight key points
    return content;
  };

  const addDetails = (content) => {
    // In a real implementation, this would expand on concepts
    return content;
  };

  if (isLoading) {
    return <div className="content-adapter">Adapting content for you...</div>;
  }

  return (
    <div className="content-adapter">
      <div className="content-display">
        {adaptedContent}
      </div>
      {userProfile && (
        <div className="personalization-info">
          <small>
            Content adapted for: {userProfile.content_level_preference || 'default'} level,
            {userProfile.example_preference || 'mixed'} examples,
            {userProfile.detail_preference || 'balanced'} detail
          </small>
        </div>
      )}
    </div>
  );
};

export default ContentAdapter;
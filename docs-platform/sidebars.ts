import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Physical AI & Humanoid Robotics Textbook',
      items: [
        'introduction-to-physical-ai',
        'ros2-the-robotic-nervous-system',
        'digital-twin-simulation',
        'nvidia-isaac-ai-brain',
        'vision-language-action-integration',
        'hardware-requirements-and-setup',
        'personalization-and-user-experience',
        'multilingual-support-and-translation',
        'fun-fact-cards-and-engagement',
        'theming-and-customization',
        'deployment-and-operations',
        'conclusion-and-future-directions'
      ],
    },
    {
      type: 'category',
      label: 'Chapter Quizzes',
      items: [
        'introduction-to-physical-ai-quiz',
        'ros2-the-robotic-nervous-system-quiz',
        'digital-twin-simulation-quiz',
        'nvidia-isaac-ai-brain-quiz',
        'vision-language-action-integration-quiz',
        'hardware-requirements-and-setup-quiz',
        'personalization-and-user-experience-quiz',
        'multilingual-support-and-translation-quiz',
        'fun-fact-cards-and-engagement-quiz',
        'theming-and-customization-quiz',
        'deployment-and-operations-quiz',
        'conclusion-and-future-directions-quiz'
      ],
    },
    {
      type: 'category',
      label: 'Additional Resources',
      items: [
        'intro',
      ],
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;

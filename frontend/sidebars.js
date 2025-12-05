// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Physical AI & Humanoid Robotics Textbook',
      items: ['textbook-content/index'],
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'textbook-content/module1',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'textbook-content/module2',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'textbook-content/module3',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'textbook-content/module4',
      ],
    },
    {
      type: 'category',
      label: 'Course Information',
      items: [
        'textbook-content/weekly_breakdown',
        'textbook-content/assessments',
        'textbook-content/hardware',
        'textbook-content/capstone',
      ],
    },
  ],
};

module.exports = sidebars;
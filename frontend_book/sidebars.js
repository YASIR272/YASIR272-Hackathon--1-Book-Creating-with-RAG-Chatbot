// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module1/index',
        'module1/chapter1-fundamentals',
        'module1/chapter2-python-agents',
        'module1/chapter3-urdf',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module2/index',
        'module2/chapter1-physics-simulation',
        'module2/chapter2-high-fidelity-rendering',
        'module2/chapter3-digital-twin-integration',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module3/index',
        'module3/chapter1-isaac-sim-basics',
        'module3/chapter2-isaac-ros-vslam',
        'module3/chapter3-path-planning-nav2',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA) for Humanoid Robotics',
      items: [
        'module4/index',
        'module4/chapter1-voice-to-action-whisper',
        'module4/chapter2-cognitive-planning-llms',
        'module4/chapter3-autonomous-humanoid-capstone',
      ],
    },
  ],
};

module.exports = sidebars;

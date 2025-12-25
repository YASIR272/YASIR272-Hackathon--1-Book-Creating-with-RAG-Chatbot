// @ts-check
import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Bridging the Digital Brain and the Physical Body',
  favicon: 'img/logo.svg',

  url: 'https://frontend-book.vercel.app',
  baseUrl: '/',

  organizationName: 'shawn-goreys-projects',
  projectName: 'frontend_book',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  onBrokenAnchors: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          routeBasePath: 'docs',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    image: 'img/social-card.png',

    metadata: [
      {
        name: 'description',
        content:
          'A complete guide to Physical AI and Humanoid Robotics using ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action systems.',
      },
      {
        name: 'keywords',
        content:
          'Physical AI, Humanoid Robotics, ROS 2, Gazebo, NVIDIA Isaac, VLA, Robotics Simulation',
      },
    ],

    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
        width: 32,
        height: 32,
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book Modules',
        },
        {
          to: '/chatbot',
          label: 'Chatbot',
          position: 'left',
        },
        {
          href: 'https://github.com',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },

    footer: {
      style: 'dark',
      links: [
        {
          title: 'Modules',
          items: [
            { label: 'ROS 2 Nervous System', to: '/docs/module1/' },
            { label: 'Digital Twin', to: '/docs/module2/' },
            { label: 'AI Robot Brain', to: '/docs/module3/' },
            { label: 'Vision-Language-Action', to: '/docs/module4/' },
          ],
        },
      ],
      copyright: `© ${new Date().getFullYear()} Physical AI & Humanoid Robotics`,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },
};

export default config;

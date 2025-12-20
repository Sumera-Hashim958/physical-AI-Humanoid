/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'index',
    {
      type: 'category',
      label: 'Chapters',
      items: [
        'chapter-01-intro-physical-ai',
        'chapter-02-sensors-perception',
        'chapter-03-kinematics-dynamics',
        'chapter-04-motion-planning',
        'chapter-05-control-systems',
        'chapter-06-learning-adaptation',
        'chapter-07-human-robot-interaction',
      ],
    },
  ],
};

module.exports = sidebars;

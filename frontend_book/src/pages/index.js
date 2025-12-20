import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Read the Book - 5 min ⏱️
          </Link>
          <Link
            className="button button--primary button--lg"
            to="/docs/module1/intro">
            Start Learning
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A comprehensive guide to Physical AI and Humanoid Robotics">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="text--center padding-horiz--md" style={{marginBottom: '3rem'}}>
              <h2>Comprehensive Learning Modules</h2>
              <p>Explore cutting-edge topics in Physical AI and Humanoid Robotics</p>
            </div>

            <div className="row">
              <div className="col col--4 padding-horiz--md">
                <div className={styles.featureCard}>
                  <div className={styles.featureImage}>
                    <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                      <rect width="100" height="100" fill="#4da6ff" opacity="0.2" rx="10"/>
                      <text x="50" y="55" textAnchor="middle" fontSize="40" fill="#2c3e50">🤖</text>
                    </svg>
                  </div>
                  <h3>Module 1: The Robotic Nervous System</h3>
                  <p>Learn about ROS 2 fundamentals, Python agents, and robot description with URDF.</p>
                  <Link to="/docs/module1/intro" className="button button--primary button--block">
                    Explore
                  </Link>
                </div>
              </div>

              <div className="col col--4 padding-horiz--md">
                <div className={styles.featureCard}>
                  <div className={styles.featureImage}>
                    <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                      <rect width="100" height="100" fill="#4da6ff" opacity="0.2" rx="10"/>
                      <text x="50" y="55" textAnchor="middle" fontSize="40" fill="#2c3e50">🔧</text>
                    </svg>
                  </div>
                  <h3>Module 2: The Digital Twin</h3>
                  <p>Explore physics simulation with Gazebo and high-fidelity rendering.</p>
                  <Link to="/docs/module2/intro" className="button button--primary button--block">
                    Explore
                  </Link>
                </div>
              </div>

              <div className="col col--4 padding-horiz--md">
                <div className={styles.featureCard}>
                  <div className={styles.featureImage}>
                    <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                      <rect width="100" height="100" fill="#4da6ff" opacity="0.2" rx="10"/>
                      <text x="50" y="55" textAnchor="middle" fontSize="40" fill="#2c3e50">🧠</text>
                    </svg>
                  </div>
                  <h3>Module 3: The AI-Robot Brain</h3>
                  <p>Master NVIDIA Isaac Sim, VSLAM, and path planning with Nav2.</p>
                  <Link to="/docs/module3/intro" className="button button--primary button--block">
                    Explore
                  </Link>
                </div>
              </div>
            </div>

            <div className="row" style={{marginTop: '2rem'}}>
              <div className="col col--6 padding-horiz--md">
                <div className={styles.featureCard}>
                  <div className={styles.featureImage}>
                    <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                      <rect width="100" height="100" fill="#4da6ff" opacity="0.2" rx="10"/>
                      <text x="50" y="55" textAnchor="middle" fontSize="40" fill="#2c3e50">💬</text>
                    </svg>
                  </div>
                  <h3>Module 4: Vision-Language-Action (VLA)</h3>
                  <p>Integrate language models with humanoid robotics for advanced AI capabilities.</p>
                  <Link to="/docs/module4/intro" className="button button--primary button--block">
                    Explore
                  </Link>
                </div>
              </div>

              <div className="col col--6 padding-horiz--md">
                <div className={styles.featureCard}>
                  <div className={styles.featureImage}>
                    <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                      <rect width="100" height="100" fill="#4da6ff" opacity="0.2" rx="10"/>
                      <text x="50" y="55" textAnchor="middle" fontSize="40" fill="#2c3e50">🌐</text>
                    </svg>
                  </div>
                  <h3>Embodied AI</h3>
                  <p>Learn about physical AI, perception, navigation, and manipulation systems.</p>
                  <Link to="/docs/intro" className="button button--primary button--block">
                    Learn More
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.testimonials}>
          <div className="container padding-vert--xl text--center">
            <div className="row">
              <div className="col col--4 col--offset-2">
                <h3>Advanced Robotics</h3>
                <p>Master cutting-edge technologies in humanoid robotics and AI.</p>
              </div>
              <div className="col col--4">
                <h3>Practical Applications</h3>
                <p>Apply your knowledge with real-world examples and projects.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
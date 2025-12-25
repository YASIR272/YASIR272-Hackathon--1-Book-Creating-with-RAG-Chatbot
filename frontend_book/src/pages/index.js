import React from 'react';
import Layout from '@theme/Layout';
import styles from './index.module.css';

export default function Home() {
  return (
    <Layout title="Physical AI & Humanoid Robotics book">
      <main className={styles.hero}>
        <div className={styles.container}>

          {/* LEFT IMAGE */}
          <div className={styles.imageWrapper}>
            <img src="/img/hero-robot.png"
              alt="Humanoid Robot and Physical AI"
              className={styles.heroImage}
            />
          </div>

          {/* RIGHT CONTENT */}
          <div className={styles.content}>
            <h1>Physical AI & Humanoid Robotics</h1>

            <p className={styles.subtitle}>
              AI Systems in the Physical World · Embodied Intelligence
            </p>

            <p>
              This book bridges the gap between the <strong>digital brain</strong> and
              the <strong>physical body</strong>, guiding students to design,
              simulate, and deploy humanoid robots in real-world environments.
            </p>

            <ul className={styles.modules}>
              <li>🧠 ROS 2 – The Robotic Nervous System</li>
              <li>🌍 Digital Twin – Gazebo & Unity</li>
              <li>🤖 AI Robot Brain – NVIDIA Isaac</li>
              <li>🗣️ Vision-Language-Action Systems</li>
            </ul>

            <div className={styles.buttons}>
              <a
                className="button button--primary button--lg"
                href="/docs/intro"
              >
                Start Reading
              </a>
              <a
                className="button button--secondary button--lg"
                href="/docs"
              >
                View Modules
              </a>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

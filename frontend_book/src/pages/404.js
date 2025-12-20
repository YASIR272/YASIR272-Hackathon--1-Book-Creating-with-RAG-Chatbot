import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function NotFound() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Page Not Found | ${siteConfig.title}`}
      description="Page not found">
      <main className="container margin-vert--xl">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <h1 className="hero__title">Page Not Found</h1>
            <p className="hero__subtitle">We could not find what you were looking for.</p>
            <div className={styles.buttons}>
              <Link
                className="button button--primary button--lg"
                to="/">
                Go to Homepage
              </Link>
              <Link
                className="button button--secondary button--lg"
                to="/docs/intro">
                Read the Book
              </Link>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

export default NotFound;
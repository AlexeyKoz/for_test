import React from 'react';
import { Link } from 'react-router-dom';
import { FiBarChart2, FiTrendingUp, FiPieChart, FiActivity } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import './Home.css';

const Home: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="home">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            Vacation Statistics Dashboard
          </h1>
          <p className="hero-subtitle">
            Comprehensive analytics and insights for vacation management system
          </p>
          <div className="hero-image">
            <FiBarChart2 className="hero-icon" />
          </div>
          <p className="hero-description">
            Monitor vacation trends, track user engagement, and analyze destination popularity 
            with our powerful statistics dashboard. Get real-time insights to make data-driven 
            decisions for your vacation platform.
          </p>
          <div className="hero-actions">
            {isAuthenticated ? (
              <Link to="/dashboard" className="cta-button primary">
                Go to Dashboard
              </Link>
            ) : (
              <Link to="/login" className="cta-button primary">
                Admin Login
              </Link>
            )}
            <Link to="/about" className="cta-button secondary">
              Learn More
            </Link>
          </div>
        </div>
      </div>

      <div className="features-section">
        <h2>Key Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <FiTrendingUp className="feature-icon" />
            <h3>Real-time Analytics</h3>
            <p>
              Track vacation statistics in real-time with automatic updates 
              and live data synchronization.
            </p>
          </div>
          <div className="feature-card">
            <FiPieChart className="feature-icon" />
            <h3>Visual Reports</h3>
            <p>
              Beautiful charts and graphs to visualize your data with 
              interactive pie charts, bar graphs, and trend lines.
            </p>
          </div>
          <div className="feature-card">
            <FiActivity className="feature-icon" />
            <h3>User Insights</h3>
            <p>
              Understand user behavior with detailed analytics on likes, 
              preferences, and engagement patterns.
            </p>
          </div>
          <div className="feature-card">
            <FiBarChart2 className="feature-icon" />
            <h3>Destination Metrics</h3>
            <p>
              Analyze destination popularity and track which locations 
              are trending among your users.
            </p>
          </div>
        </div>
      </div>

      <div className="stats-preview">
        <h2>What You Can Track</h2>
        <div className="preview-list">
          <div className="preview-item">
            <span className="preview-bullet">▸</span>
            Total number of registered users
          </div>
          <div className="preview-item">
            <span className="preview-bullet">▸</span>
            Past, ongoing, and future vacations
          </div>
          <div className="preview-item">
            <span className="preview-bullet">▸</span>
            Total likes and engagement metrics
          </div>
          <div className="preview-item">
            <span className="preview-bullet">▸</span>
            Distribution of likes by destination
          </div>
          <div className="preview-item">
            <span className="preview-bullet">▸</span>
            Top trending vacation destinations
          </div>
          <div className="preview-item">
            <span className="preview-bullet">▸</span>
            Historical trends and patterns
          </div>
        </div>
      </div>

      <div className="cta-section">
        <h2>Ready to Get Started?</h2>
        <p>Access comprehensive vacation statistics and analytics now.</p>
        {!isAuthenticated && (
          <Link to="/login" className="cta-button large">
            Login as Administrator
          </Link>
        )}
      </div>
    </div>
  );
};

export default Home;
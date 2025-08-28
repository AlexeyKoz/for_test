import React from 'react';
import { Link } from 'react-router-dom';
import { FiHome, FiArrowLeft, FiAlertTriangle } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import './NotFound.css';

const NotFound: React.FC = () => {
    const { isAuthenticated } = useAuth();

    return (
        <div className="not-found">
            <div className="not-found-container">
                <div className="not-found-icon">
                    <FiAlertTriangle />
                </div>

                <h1 className="not-found-title">404</h1>
                <h2 className="not-found-subtitle">Page Not Found</h2>

                <p className="not-found-description">
                    Oops! The page you're looking for doesn't exist.
                    It might have been moved, deleted, or you entered the wrong URL.
                </p>

                <div className="not-found-actions">
                    <Link to="/" className="not-found-button primary">
                        <FiHome />
                        Go to Home
                    </Link>

                    <button
                        onClick={() => window.history.back()}
                        className="not-found-button secondary"
                    >
                        <FiArrowLeft />
                        Go Back
                    </button>
                </div>

                {isAuthenticated && (
                    <div className="not-found-links">
                        <p>Quick Navigation:</p>
                        <div className="not-found-nav-links">
                            <Link to="/dashboard">Dashboard</Link>
                            <Link to="/about">About</Link>
                        </div>
                    </div>
                )}

                <div className="not-found-help">
                    <p>
                        If you believe this is an error, please contact support or try refreshing the page.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default NotFound;

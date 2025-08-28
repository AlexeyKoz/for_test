import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FiBarChart2, FiLogOut, FiInfo, FiHome } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

const Navbar: React.FC = () => {
    const { user, logout, isAuthenticated } = useAuth();
    const location = useLocation();

    const isActive = (path: string) => location.pathname === path;

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <div className="navbar-brand">
                    <Link to="/" className="navbar-brand-link">
                        <FiBarChart2 className="navbar-icon" />
                        <span>Vacation Stats</span>
                    </Link>
                </div>

                <div className="navbar-menu">
                    {isAuthenticated ? (
                        <>
                            <Link
                                to="/"
                                className={`navbar-link ${isActive('/') ? 'active' : ''}`}
                            >
                                <FiHome className="navbar-link-icon" />
                                Home
                            </Link>
                            <Link
                                to="/dashboard"
                                className={`navbar-link ${isActive('/dashboard') ? 'active' : ''}`}
                            >
                                <FiBarChart2 className="navbar-link-icon" />
                                Dashboard
                            </Link>
                            <Link
                                to="/about"
                                className={`navbar-link ${isActive('/about') ? 'active' : ''}`}
                            >
                                <FiInfo className="navbar-link-icon" />
                                About
                            </Link>
                        </>
                    ) : (
                        <Link
                            to="/about"
                            className={`navbar-link ${isActive('/about') ? 'active' : ''}`}
                        >
                            <FiInfo className="navbar-link-icon" />
                            About
                        </Link>
                    )}
                </div>

                {isAuthenticated && (
                    <div className="navbar-user">
                        <span className="navbar-username">
                            Hello, {user?.first_name || user?.email}
                        </span>
                        <button onClick={logout} className="navbar-logout">
                            <FiLogOut />
                            Logout
                        </button>
                    </div>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
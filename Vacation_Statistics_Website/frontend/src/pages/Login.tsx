import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiMail, FiLock, FiLogIn } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import './Login.css';

const Login: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const { login, isAuthenticated } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (isAuthenticated) {
            navigate('/dashboard');
        }
    }, [isAuthenticated, navigate]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        // Basic client-side validation
        if (!email.trim()) {
            setError('Email is required');
            setIsLoading(false);
            return;
        }

        if (!password.trim()) {
            setError('Password is required');
            setIsLoading(false);
            return;
        }

        if (password.length < 4) {
            setError('Password must be at least 4 characters');
            setIsLoading(false);
            return;
        }

        try {
            await login({ email: email.trim(), password });
        } catch (err: any) {
            let errorMessage: string;

            // Extract user-friendly error message
            if (err.message && typeof err.message === 'string') {
                errorMessage = err.message;
            } else if (err.response?.data?.error) {
                errorMessage = err.response.data.error;
            } else if (err.code === 'NETWORK_ERROR' || !err.response) {
                errorMessage = 'Cannot connect to server. Please check your connection.';
            } else {
                errorMessage = 'Login failed. Please try again.';
            }

            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <FiLogIn className="login-icon" />
                    <h1>Admin Login</h1>
                    <p>Sign in to access the statistics dashboard</p>
                </div>

                <form onSubmit={handleSubmit} className="login-form">
                    <div className="form-group">
                        <label htmlFor="email">
                            <FiMail className="input-icon" />
                            Email Address
                        </label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="admin@example.com"
                            required
                            disabled={isLoading}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">
                            <FiLock className="input-icon" />
                            Password
                        </label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                            required
                            disabled={isLoading}
                        />
                    </div>

                    {error && (
                        <div className="error-message">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        className="login-button"
                        disabled={isLoading}
                    >
                        {isLoading ? (
                            <>
                                <span className="spinner-small"></span>
                                Signing in...
                            </>
                        ) : (
                            <>
                                <FiLogIn />
                                Sign In
                            </>
                        )}
                    </button>
                </form>

                <div className="login-footer">
                    <p className="info-text">
                        Only administrators can access the statistics dashboard.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login;
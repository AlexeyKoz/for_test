import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';

import Home from './pages/Home';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import About from './pages/About';
import NotFound from './pages/NotFound';

import './App.css';

const App: React.FC = () => {
    return (
        <Router>
            <AuthProvider>
                <div className="app">
                    <Navbar />
                    <main className="app-main">
                        <Routes>
                            {/* Public Routes */}
                            <Route path="/" element={<Home />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/about" element={<About />} />

                            {/* Protected Routes */}
                            <Route
                                path="/dashboard"
                                element={
                                    <ProtectedRoute>
                                        <Dashboard />
                                    </ProtectedRoute>
                                }
                            />

                            {/* 404 Route - Catch all unmatched routes */}
                            <Route path="*" element={<NotFound />} />
                        </Routes>
                    </main>
                </div>
            </AuthProvider>
        </Router>
    );
};

export default App;
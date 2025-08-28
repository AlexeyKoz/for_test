import React from 'react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock the stats API module to avoid real HTTP calls
jest.mock('../services/Api', () => ({
    statsAPI: {
        getSummaryStats: jest.fn(),
    },
}));

// Mock AuthContext useAuth hook
jest.mock('../context/AuthContext', () => ({
    useAuth: jest.fn(),
}));

import ProtectedRoute from '../components/ProtectedRoute';
import Dashboard from '../pages/Dashboard';
import { statsAPI } from '../services/Api';
import { useAuth } from '../context/AuthContext';

describe('Dashboard Page', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        // Set up default mock response
        (statsAPI.getSummaryStats as jest.Mock).mockResolvedValue({
            vacationStats: { pastVacations: 1, ongoingVacations: 2, futureVacations: 3 },
            totalUsers: 5,
            totalLikes: 10,
            topDestinations: [
                { destination: 'Rome', likes: 4 },
                { destination: 'Paris', likes: 3 },
            ],
        });
    });

    test('positive: renders dashboard content for authenticated user', async () => {
        // Mock authenticated user
        (useAuth as jest.Mock).mockReturnValue({
            user: { email: 'admin@example.com', first_name: 'Admin', last_name: 'User' },
            token: 'token',
            login: jest.fn(),
            logout: jest.fn(),
            isAuthenticated: true,
            isLoading: false,
        });

        render(
            <MemoryRouter initialEntries={["/dashboard"]}>
                <Routes>
                    <Route
                        path="/dashboard"
                        element={
                            <ProtectedRoute>
                                <Dashboard />
                            </ProtectedRoute>
                        }
                    />
                </Routes>
            </MemoryRouter>
        );

        // Wait for the dashboard to load and check for the main heading
        expect(await screen.findByText(/statistics dashboard/i)).toBeInTheDocument();

        // Check for stats cards that should be rendered
        expect(await screen.findByText(/total users/i)).toBeInTheDocument();
        expect(await screen.findByText(/total likes/i)).toBeInTheDocument();
        expect(await screen.findByText(/total vacations/i)).toBeInTheDocument();
    });

    test('negative: redirects unauthenticated user to login', async () => {
        // Mock unauthenticated user
        (useAuth as jest.Mock).mockReturnValue({
            user: null,
            token: null,
            login: jest.fn(),
            logout: jest.fn(),
            isAuthenticated: false,
            isLoading: false,
        });

        render(
            <MemoryRouter initialEntries={["/dashboard"]}>
                <Routes>
                    <Route
                        path="/dashboard"
                        element={
                            <ProtectedRoute>
                                <Dashboard />
                            </ProtectedRoute>
                        }
                    />
                    <Route path="/login" element={<div>Login Page</div>} />
                </Routes>
            </MemoryRouter>
        );

        // Should redirect to login page
        expect(await screen.findByText(/login page/i)).toBeInTheDocument();
    });
});
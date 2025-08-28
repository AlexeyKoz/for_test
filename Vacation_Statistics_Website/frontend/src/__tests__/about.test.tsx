import React from 'react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock AuthContext useAuth hook
const mockUseAuth = jest.fn();
jest.mock('../context/AuthContext', () => ({
    useAuth: () => mockUseAuth(),
}));

import About from '../pages/About';
import Navbar from '../components/Navbar';

describe('About Page', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('positive: renders About content for public access', () => {
        // Mock unauthenticated user for public access
        mockUseAuth.mockReturnValue({
            user: null,
            token: null,
            login: jest.fn(),
            logout: jest.fn(),
            isAuthenticated: false,
            isLoading: false,
        });

        render(
            <MemoryRouter initialEntries={["/about"]}>
                <Routes>
                    <Route path="/about" element={<About />} />
                </Routes>
            </MemoryRouter>
        );

        // Check for main headings
        expect(screen.getByRole('heading', { name: /about this project/i })).toBeInTheDocument();
        expect(screen.getByRole('heading', { name: /project overview/i })).toBeInTheDocument();

        // Check for technology stack section
        expect(screen.getByRole('heading', { name: /technology stack/i })).toBeInTheDocument();

        // Check for developer information
        expect(screen.getByText(/doron shalom & alexey kozlov/i)).toBeInTheDocument();
    });

    test('negative: when logged out, Navbar shows About link but no Logout button', () => {
        // Mock unauthenticated user
        mockUseAuth.mockReturnValue({
            user: null,
            token: null,
            login: jest.fn(),
            logout: jest.fn(),
            isAuthenticated: false,
            isLoading: false,
        });

        render(
            <MemoryRouter initialEntries={["/about"]}>
                <Navbar />
                <Routes>
                    <Route path="/about" element={<About />} />
                </Routes>
            </MemoryRouter>
        );

        // About link should be visible (use more specific selector)
        expect(screen.getByRole('link', { name: /about/i })).toBeInTheDocument();

        // Logout button should not appear when not authenticated
        expect(screen.queryByText(/logout/i)).not.toBeInTheDocument();

        // Dashboard link should not appear when not authenticated (check for navigation link specifically)
        expect(screen.queryByRole('link', { name: /dashboard/i })).not.toBeInTheDocument();
    });
});
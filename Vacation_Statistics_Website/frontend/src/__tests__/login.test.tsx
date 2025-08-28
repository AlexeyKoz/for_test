import React from 'react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock AuthContext useAuth hook
const mockUseAuth = jest.fn();
jest.mock('../context/AuthContext', () => ({
    useAuth: () => mockUseAuth(),
}));

import Login from '../pages/Login';

describe('Login Page', () => {
    const mockLogin = jest.fn();

    beforeEach(() => {
        jest.clearAllMocks();
        mockUseAuth.mockReturnValue({
            login: mockLogin,
            isAuthenticated: false,
            user: null,
            token: null,
            logout: jest.fn(),
            isLoading: false,
        });
    });

    test('positive: submits valid credentials and calls login', async () => {
        render(
            <MemoryRouter initialEntries={["/login"]}>
                <Routes>
                    <Route path="/login" element={<Login />} />
                </Routes>
            </MemoryRouter>
        );

        // Fill in the form
        fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'admin@example.com' } });
        fireEvent.change(screen.getByLabelText(/password/i), { target: { value: '1234' } });

        // Submit the form
        fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

        // Verify login was called with correct credentials
        await waitFor(() => {
            expect(mockLogin).toHaveBeenCalledWith({ email: 'admin@example.com', password: '1234' });
        });
    });

    test('negative: shows client-side validation error when email is empty', async () => {
        render(
            <MemoryRouter initialEntries={["/login"]}>
                <Routes>
                    <Route path="/login" element={<Login />} />
                </Routes>
            </MemoryRouter>
        );

        // Try to submit without filling email
        fireEvent.change(screen.getByLabelText(/password/i), { target: { value: '1234' } });
        fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

        // Should show validation error
        expect(await screen.findByText(/email is required/i)).toBeInTheDocument();

        // Ensure login was not called
        expect(mockLogin).not.toHaveBeenCalled();
    });
});
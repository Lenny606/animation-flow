import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const isAuthDisabled = import.meta.env.VITE_DISABLE_AUTH === 'true';

    const checkSession = async () => {
        if (isAuthDisabled) {
            setUser({ id: 'disabled', email: 'auth@disabled.com', full_name: 'Auth Disabled' });
            setLoading(false);
            return;
        }

        try {
            const apiUrl = import.meta.env.VITE_API_URL || '';
            const normalizedApiUrl = apiUrl.startsWith('http') ? apiUrl : `https://${apiUrl}`;
            const response = await fetch(`${normalizedApiUrl}/auth/me`, {
                credentials: 'include',
            });

            if (response.ok) {
                const userData = await response.json();
                setUser(userData);
            } else {
                setUser(null);
            }
        } catch (error) {
            console.error('Failed to check session:', error);
            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        checkSession();
    }, []);

    const login = async (email, password) => {
        const apiUrl = import.meta.env.VITE_API_URL || '';
        const normalizedApiUrl = apiUrl.startsWith('http') ? apiUrl : `https://${apiUrl}`;
        const response = await fetch(`${normalizedApiUrl}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
            credentials: 'include',
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Login failed');
        }

        // After successful login, check session to get user info
        await checkSession();
    };

    const logout = async () => {
        try {
            const apiUrl = import.meta.env.VITE_API_URL || '';
            const normalizedApiUrl = apiUrl.startsWith('http') ? apiUrl : `https://${apiUrl}`;
            await fetch(`${normalizedApiUrl}/auth/logout`, {
                method: 'POST',
                credentials: 'include',
            });
        } catch (error) {
            console.error('Logout failed:', error);
        } finally {
            setUser(null);
        }
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, logout, isAuthenticated: !!user }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

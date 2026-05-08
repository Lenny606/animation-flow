import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();
    const { login, isAuthenticated } = useAuth();

    useEffect(() => {
        if (isAuthenticated) {
            navigate('/home');
        }
    }, [isAuthenticated, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            await login(email, password);
            navigate('/home');
        } catch (err) {
            console.error('Login error:', err);
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <h2 style={styles.title}>Login</h2>
                <form onSubmit={handleSubmit} style={styles.form}>
                    {error && <div style={styles.error} role="alert" id="login-error">{error}</div>}
                    <div style={styles.inputGroup}>
                        <label htmlFor="email" style={styles.label}>
                            Email <span aria-hidden="true" style={{color: '#dc3545'}}>*</span>
                        </label>
                        <input
                            id="email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            aria-invalid={!!error}
                            aria-describedby={error ? "login-error" : undefined}
                            style={{ ...styles.input, ...(isLoading ? styles.inputDisabled : {}) }}
                            placeholder="Enter your email"
                            disabled={isLoading}
                        />
                    </div>
                    <div style={styles.inputGroup}>
                        <label htmlFor="password" style={styles.label}>
                            Password <span aria-hidden="true" style={{color: '#dc3545'}}>*</span>
                        </label>
                        <div style={styles.passwordWrapper}>
                            <input
                                id="password"
                                type={showPassword ? "text" : "password"}
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                aria-invalid={!!error}
                                aria-describedby={error ? "login-error" : undefined}
                                style={{ ...styles.input, ...styles.passwordInput, ...(isLoading ? styles.inputDisabled : {}) }}
                                placeholder="Enter your password"
                                disabled={isLoading}
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                style={styles.toggleButton}
                                aria-label={showPassword ? "Hide password" : "Show password"}
                            >
                                {showPassword ? "Hide" : "Show"}
                            </button>
                        </div>
                    </div>
                    <button type="submit" style={{ ...styles.button, ...(isLoading ? styles.buttonDisabled : {}) }} disabled={isLoading}>
                        {isLoading ? 'Signing In...' : 'Sign In'}
                    </button>
                </form>
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#f5f5f5',
    },
    card: {
        padding: '2rem',
        borderRadius: '8px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        backgroundColor: '#ffffff',
        width: '100%',
        maxWidth: '400px',
    },
    title: {
        textAlign: 'center',
        marginBottom: '1.5rem',
        color: '#333',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
    },
    inputGroup: {
        marginBottom: '1rem',
    },
    label: {
        display: 'block',
        marginBottom: '0.5rem',
        fontWeight: '600',
        color: '#666',
    },
    input: {
        width: '100%',
        padding: '0.75rem',
        borderRadius: '4px',
        border: '1px solid #ccc',
        fontSize: '1rem',
        boxSizing: 'border-box',
    },
    passwordWrapper: {
        position: 'relative',
        display: 'flex',
        alignItems: 'center',
    },
    passwordInput: {
        paddingRight: '4rem',
    },
    toggleButton: {
        position: 'absolute',
        right: '0.5rem',
        background: 'none',
        border: 'none',
        padding: '0.25rem 0.5rem',
        fontSize: '0.875rem',
        color: '#007bff',
        cursor: 'pointer',
        fontWeight: '500',
    },
    inputDisabled: {
        backgroundColor: '#e9ecef',
        cursor: 'not-allowed',
        opacity: 0.7,
    },
    button: {
        padding: '0.75rem',
        borderRadius: '4px',
        border: 'none',
        backgroundColor: '#007bff',
        color: 'white',
        fontSize: '1rem',
        fontWeight: '600',
        cursor: 'pointer',
        marginTop: '1rem',
        transition: 'background-color 0.2s',
    },
    buttonDisabled: {
        backgroundColor: '#6c757d',
        cursor: 'not-allowed',
        opacity: 0.7,
    },
    error: {
        color: '#dc3545',
        backgroundColor: '#f8d7da',
        border: '1px solid #f5c6cb',
        padding: '0.75rem',
        borderRadius: '4px',
        marginBottom: '1rem',
        textAlign: 'center',
        fontSize: '0.9rem',
    },
};

export default Login;

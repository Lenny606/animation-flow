import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const TopBar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        await logout();
        navigate('/login');
    };

    const getInitials = (name) => {
        if (!name) return 'U';
        return name.split(' ').map(n => n[0]).join('').toUpperCase();
    };

    return (
        <header className="topbar">
            <div className="topbar-left">
                {/* Space for breadcrumbs or page title if needed */}
            </div>
            <div className="topbar-right">
                <div className="user-profile">
                    <div className="avatar">{getInitials(user?.full_name || user?.email)}</div>
                    <span className="user-name">{user?.full_name || user?.email || 'User'}</span>
                    <button onClick={handleLogout} className="logout-button" title="Logout">
                        Logout 🚪
                    </button>
                </div>
            </div>
        </header>
    );
};

export default TopBar;

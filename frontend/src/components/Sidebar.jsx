import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                <div className="logo">
                    <span className="logo-icon">✨</span>
                    <span>AnimFlow</span>
                </div>
            </div>
            <nav className="sidebar-nav">
                <NavLink
                    to="/home"
                    className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}
                >
                    <span className="nav-icon">🏠</span>
                    Home
                </NavLink>
                <NavLink
                    to="/songs"
                    className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}
                >
                    <span className="nav-icon">🎵</span>
                    Songs
                </NavLink>
            </nav>
        </aside>
    );
};

export default Sidebar;

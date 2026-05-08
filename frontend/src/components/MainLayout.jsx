import React from 'react';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import '../styles/Layout.css';

const MainLayout = ({ children }) => {
    return (
        <div className="main-layout">
            <Sidebar />
            <TopBar />
            <main className="page-container">
                {children}
            </main>
        </div>
    );
};

export default MainLayout;

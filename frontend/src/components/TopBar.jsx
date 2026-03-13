import React from 'react';

const TopBar = () => {
    return (
        <header className="topbar">
            <div className="topbar-left">
                {/* Space for breadcrumbs or page title if needed */}
            </div>
            <div className="topbar-right">
                <div className="user-profile">
                    <div className="avatar">JD</div>
                    <span className="user-name">John Doe</span>
                </div>
            </div>
        </header>
    );
};

export default TopBar;

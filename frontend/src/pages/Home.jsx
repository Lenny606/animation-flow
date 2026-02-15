import React from 'react';

const Home = () => {
    return (
        <div style={styles.container}>
            <div style={styles.content}>
                <h1 style={styles.title}>Welcome to Animation Flow</h1>
                <p style={styles.text}>This is your simple responsive homepage.</p>
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        backgroundColor: '#f0f2f5',
        padding: '20px',
    },
    content: {
        textAlign: 'center',
        backgroundColor: '#ffffff',
        padding: '2.5rem',
        borderRadius: '12px',
        boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
        width: '100%',
        maxWidth: '600px',
    },
    title: {
        color: '#1a1a1a',
        fontSize: 'clamp(1.5rem, 5vw, 2.5rem)',
        marginBottom: '1rem',
        fontWeight: '700',
    },
    text: {
        color: '#4b5563',
        fontSize: '1.1rem',
        lineHeight: '1.6',
    },
};

export default Home;

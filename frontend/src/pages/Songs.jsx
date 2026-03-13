import React from 'react';

const Songs = () => {
    return (
        <div style={styles.container}>
            <header style={styles.header}>
                <h1 style={styles.title}>Songs Library</h1>
                <p style={styles.subtitle}>Manage your generated soundtracks and favorites.</p>
            </header>
            
            <div style={styles.placeholderCard}>
                <div style={styles.icon}>🎵</div>
                <h2>Your music will appear here</h2>
                <p>Start by generating an animation with a custom soundtrack.</p>
                <button style={styles.btn}>Browse Categories</button>
            </div>
        </div>
    );
};

const styles = {
    container: {
        width: '100%',
        padding: '2rem 0',
    },
    header: {
        marginBottom: '3rem',
    },
    title: {
        fontSize: '2.5rem',
        color: '#0f172a',
        fontWeight: '800',
        marginBottom: '0.5rem',
    },
    subtitle: {
        color: '#64748b',
        fontSize: '1.1rem',
    },
    placeholderCard: {
        backgroundColor: '#ffffff',
        borderRadius: '24px',
        padding: '5rem 2rem',
        textAlign: 'center',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
        border: '1px solid rgba(0, 0, 0, 0.05)',
    },
    icon: {
        fontSize: '4rem',
        marginBottom: '1.5rem',
    },
    btn: {
        marginTop: '2rem',
        backgroundColor: '#3b82f6',
        color: 'white',
        border: 'none',
        borderRadius: '12px',
        padding: '0.75rem 2rem',
        fontSize: '1rem',
        fontWeight: '700',
        cursor: 'pointer',
    },
};

export default Songs;

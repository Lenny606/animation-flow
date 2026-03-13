import React from 'react';
import { useQuery } from '@tanstack/react-query';

const Songs = () => {
    const getAuthHeaders = () => {
        const token = localStorage.getItem('token');
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
    };

    const fetchSongs = async () => {
        const apiUrl = import.meta.env.VITE_API_URL || '';
        const normalizedApiUrl = apiUrl.startsWith('http') ? apiUrl : `https://${apiUrl}`;
        const response = await fetch(`${normalizedApiUrl}/songs/`, {
            headers: getAuthHeaders(),
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    };

    const { data: songs, isLoading, error } = useQuery({
        queryKey: ['songs'],
        queryFn: fetchSongs,
    });

    if (isLoading) {
        return (
            <div style={styles.container}>
                <div style={styles.loadingContainer}>
                    <div className="loading-spinner"></div>
                    <p>Loading your melodies...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div style={styles.container}>
                <div style={styles.errorContainer}>
                    <h3>Oops! Something went wrong</h3>
                    <p>{error.message}</p>
                    <button onClick={() => window.location.reload()} style={styles.btn}>Try Again</button>
                </div>
            </div>
        );
    }

    return (
        <div style={styles.container}>
            <header style={styles.header}>
                <h1 style={styles.title}>Songs Library</h1>
                <p style={styles.subtitle}>Your collection of AI-generated music and lyrics.</p>
            </header>

            {songs && songs.length > 0 ? (
                <div style={styles.songGrid}>
                    {songs.map((song) => (
                        <div key={song._id || song.id} style={styles.songCard}>
                            <div style={styles.songIcon}>🎵</div>
                            <div style={styles.songInfo}>
                                <h3 style={styles.songTitle}>{song.title}</h3>
                                <p style={styles.songMeta}>
                                    <span style={styles.tag}>{song.category}</span>
                                    <span style={styles.playlist}>{song.playlist_name}</span>
                                </p>
                                <div style={styles.lyricsPreview}>
                                    {song.text.substring(0, 100)}...
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div style={styles.placeholderCard}>
                    <div style={styles.icon}>🎵</div>
                    <h2>Your music will appear here</h2>
                    <p>Start by generating an animation with a custom soundtrack.</p>
                </div>
            )}
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
    songGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
        gap: '1.5rem',
    },
    songCard: {
        backgroundColor: '#ffffff',
        borderRadius: '20px',
        padding: '1.5rem',
        display: 'flex',
        gap: '1.25rem',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
        border: '1px solid rgba(0, 0, 0, 0.05)',
        transition: 'transform 0.2s, box-shadow 0.2s',
        cursor: 'pointer',
    },
    songIcon: {
        fontSize: '1.75rem',
        backgroundColor: '#eff6ff',
        color: '#3b82f6',
        width: '56px',
        height: '56px',
        borderRadius: '16px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexShrink: 0,
    },
    songInfo: {
        flex: 1,
        overflow: 'hidden',
    },
    songTitle: {
        fontSize: '1.1rem',
        fontWeight: '700',
        color: '#1e293b',
        marginBottom: '0.5rem',
        whiteSpace: 'nowrap',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
    },
    songMeta: {
        display: 'flex',
        gap: '0.5rem',
        marginBottom: '0.75rem',
        flexWrap: 'wrap',
    },
    tag: {
        fontSize: '0.75rem',
        backgroundColor: '#f1f5f9',
        color: '#475569',
        padding: '0.2rem 0.6rem',
        borderRadius: '100px',
        fontWeight: '600',
    },
    playlist: {
        fontSize: '0.75rem',
        color: '#64748b',
        display: 'flex',
        alignItems: 'center',
    },
    lyricsPreview: {
        fontSize: '0.875rem',
        color: '#64748b',
        lineHeight: '1.5',
        display: '-webkit-box',
        WebkitLineClamp: 2,
        WebkitBoxOrient: 'vertical',
        overflow: 'hidden',
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
    loadingContainer: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '5rem 0',
        color: '#64748b',
    },
    errorContainer: {
        textAlign: 'center',
        padding: '5rem 2rem',
        backgroundColor: '#fef2f2',
        borderRadius: '24px',
        color: '#dc2626',
    }
};

export default Songs;

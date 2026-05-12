import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { useSelection } from '../context/SelectionContext';

const Songs = () => {
    const navigate = useNavigate();
    const { selection, toggleSongSelection } = useSelection();

    const getAuthHeaders = () => {
        return {
            'Content-Type': 'application/json',
        };
    };

    const fetchSongs = async () => {
        const apiUrl = import.meta.env.VITE_API_URL || '';
        let normalizedApiUrl = apiUrl.startsWith('http') ? apiUrl : `https://${apiUrl}`;
        // Remove trailing slash if exists
        normalizedApiUrl = normalizedApiUrl.replace(/\/$/, '');
        
        // Ensure we call /songs/ directly (without api/v1 if the backend is at root)
        const response = await fetch(`${normalizedApiUrl}/songs/`, {
            headers: getAuthHeaders(),
            credentials: 'include',
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
                <div style={styles.headerTop}>
                    <div>
                        <h1 style={styles.title}>Songs Library (v2)</h1>
                        <p style={styles.subtitle}>Your collection of AI-generated music and lyrics.</p>
                    </div>
                    {selection.song && (
                        <button 
                            style={styles.nextBtn}
                            onClick={() => navigate('/prompts')}
                        >
                            Next: Generate Prompt →
                        </button>
                    )}
                </div>
            </header>

            {songs && songs.length > 0 ? (
                <div style={styles.songList}>
                    {songs.map((song) => {
                        const songId = song._id || song.id;
                        const isSelected = selection.song && (selection.song._id === songId || selection.song.id === songId);
                        return (
                            <div
                                key={songId}
                                style={{
                                    ...styles.songItem,
                                    ...(isSelected ? styles.songItemActive : {})
                                }}
                                onClick={() => toggleSongSelection(song)}
                            >
                                <h3 style={styles.songTitle}>{song.title}</h3>
                                <button
                                    style={{
                                        ...styles.selectBtn,
                                        ...(isSelected ? styles.selectBtnActive : {})
                                    }}
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        toggleSongSelection(song);
                                    }}
                                    aria-label={(isSelected ? 'Unselect ' : 'Select ') + song.title}
                                >
                                    {isSelected ? 'Unselect' : 'Select'}
                                </button>
                            </div>
                        );
                    })}
                </div>
            ) : (
                <div style={styles.placeholderCard}>
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
    headerTop: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '1rem',
        flexWrap: 'wrap',
    },
    nextBtn: {
        backgroundColor: '#3b82f6',
        color: 'white',
        border: 'none',
        borderRadius: '12px',
        padding: '0.8rem 1.5rem',
        fontSize: '1rem',
        fontWeight: '700',
        cursor: 'pointer',
        boxShadow: '0 4px 6px -1px rgba(59, 130, 246, 0.3)',
        transition: 'transform 0.2s, background-color 0.2s',
        animation: 'slideIn 0.3s ease-out',
    },
    title: {
        fontSize: '1.5rem',
        color: '#0f172a',
        fontWeight: '800',
        marginBottom: '0.25rem',
    },
    subtitle: {
        color: '#64748b',
        fontSize: '1.1rem',
    },
    songList: {
        display: 'flex',
        flexDirection: 'column',
        gap: '0.75rem',
    },
    songItem: {
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        padding: '1rem 1.5rem',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
        border: '1px solid rgba(0, 0, 0, 0.05)',
        transition: 'all 0.2s ease',
        cursor: 'pointer',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    songItemActive: {
        borderColor: '#3b82f6',
        backgroundColor: '#eff6ff',
        transform: 'translateX(4px)',
    },
    songTitle: {
        fontSize: '1.1rem',
        fontWeight: '600',
        color: '#1e293b',
        margin: 0,
    },
    selectBtn: {
        backgroundColor: '#f1f5f9',
        color: '#475569',
        border: 'none',
        borderRadius: '8px',
        padding: '0.4rem 1rem',
        fontSize: '0.875rem',
        fontWeight: '600',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    selectBtnActive: {
        backgroundColor: '#3b82f6',
        color: '#ffffff',
    },
    placeholderCard: {
        backgroundColor: '#ffffff',
        borderRadius: '24px',
        padding: '5rem 2rem',
        textAlign: 'center',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
        border: '1px solid rgba(0, 0, 0, 0.05)',
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

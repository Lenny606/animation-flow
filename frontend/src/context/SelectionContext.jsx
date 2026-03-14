import React, { createContext, useContext, useState, useEffect } from 'react';

const SelectionContext = createContext();

export const SelectionProvider = ({ children }) => {
    // Load initial state from localStorage
    const [selection, setSelection] = useState(() => {
        try {
            const saved = localStorage.getItem('animation_flow_selection');
            if (saved) return JSON.parse(saved);
        } catch (error) {
            console.error('Error parsing selection from localStorage:', error);
        }
        return {
            song: null,
            style: 'pastel-cartoon',
            imageCount: 4,
        };
    });

    // Save to localStorage whenever selection changes
    useEffect(() => {
        localStorage.setItem('animation_flow_selection', JSON.stringify(selection));
    }, [selection]);

    const setSongSelection = (song) => {
        setSelection(prev => ({
            ...prev,
            song: song
        }));
    };

    const setStyleSelection = (style) => {
        setSelection(prev => ({
            ...prev,
            style: style
        }));
    };

    const setImageCountSelection = (count) => {
        setSelection(prev => ({
            ...prev,
            imageCount: count
        }));
    };

    const clearSongSelection = () => {
        setSelection(prev => ({
            ...prev,
            song: null
        }));
    };

    const toggleSongSelection = (song) => {
        setSelection(prev => {
            if (prev.song && (prev.song._id === (song._id || song.id) || prev.song.id === (song._id || song.id))) {
                return { ...prev, song: null };
            }
            return { ...prev, song: song };
        });
    };

    return (
        <SelectionContext.Provider value={{ 
            selection, 
            setSongSelection, 
            setStyleSelection, 
            setImageCountSelection,
            clearSongSelection, 
            toggleSongSelection 
        }}>
            {children}
        </SelectionContext.Provider>
    );
};

export const useSelection = () => {
    const context = useContext(SelectionContext);
    if (!context) {
        throw new Error('useSelection must be used within a SelectionProvider');
    }
    return context;
};

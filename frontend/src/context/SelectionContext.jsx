import React, { createContext, useContext, useState } from 'react';

const SelectionContext = createContext();

export const SelectionProvider = ({ children }) => {
    const [selection, setSelection] = useState({
        song: null,
        style: 'pastel-cartoon', // Default style
    });

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
        <SelectionContext.Provider value={{ selection, setSongSelection, setStyleSelection, clearSongSelection, toggleSongSelection }}>
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

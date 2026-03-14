import React, { useState } from 'react';
import { useSelection } from '../context/SelectionContext';

const PromptGeneration = () => {
    const { selection, setStyleSelection } = useSelection();
    const [generatedPrompt, setGeneratedPrompt] = useState('');
    const [isGenerating, setIsGenerating] = useState(false);

    const stylesList = [
        { id: 'pastel-cartoon', name: 'Pastel Cartoon', prompt: 'pastel cartoon with soft gradients and thick outlines' },
        { id: 'watercolor-storybook', name: 'Watercolor Storybook', prompt: 'dreamy watercolor storybook illustration with textured paper' },
        { id: 'kawaii-cartoon', name: 'Kawaii Cartoon', prompt: 'vibrant kawaii cartoon style with clean lines and cute proportions' },
        { id: 'crayon-drawing', name: 'Crayon Drawing', prompt: 'hand-drawn crayon drawing with rough textures and playful strokes' },
        { id: 'soft-3d-cartoon', name: 'Soft 3D Cartoon', prompt: 'soft 3D cartoon render with clay-like textures and warm lighting' },
        { id: 'paper-cut', name: 'Paper Cut Animation', prompt: 'intricate paper cut animation style with layered depth and shadows' }
    ];

    const handleGenerate = async () => {
        if (!selection.song) return;
        
        setIsGenerating(true);
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/prompts/generate-prompt`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    song_title: selection.song.title,
                    song_text: selection.song.text,
                    style: selection.style || 'pastel-cartoon'
                }),
            });

            if (!response.ok) throw new Error('Failed to generate prompt');
            
            const data = await response.json();
            setGeneratedPrompt(data.optimized_text);
        } catch (error) {
            console.error('Error generating prompt:', error);
            // Fallback for UI if API fails
            const selectedStyle = stylesList.find(s => s.id === selection.style);
            setGeneratedPrompt(`Based on "${selection.song.title}": ${selectedStyle?.prompt || 'visual'}. Ethereal atmosphere.`);
        } finally {
            setIsGenerating(false);
        }
    };

    return (
        <div style={styles.container}>
            <header style={styles.header}>
                <h1 style={styles.title}>Prompt Generation</h1>
                <p style={styles.subtitle}>Transform your selected song or ideas into detailed AI prompts.</p>
            </header>

            {selection.song && (
                <div style={styles.infoCard}>
                    <strong>Selected Song:</strong> {selection.song.title}
                </div>
            )}

            <div style={styles.card}>
                <div style={styles.options}>
                    {stylesList.map(style => (
                        <button 
                            key={style.id}
                            style={{...styles.optionBtn, ...(selection.style === style.id ? styles.activeOption : {})}}
                            onClick={() => setStyleSelection(style.id)}
                        >
                            {style.name}
                        </button>
                    ))}
                </div>

                <button 
                    style={styles.generateBtn} 
                    onClick={handleGenerate}
                    disabled={isGenerating}
                >
                    {isGenerating ? 'Analyzing...' : 'Generate Optimized Prompt ✨'}
                </button>

                {generatedPrompt && (
                    <div style={styles.result}>
                        <h3 style={styles.resultTitle}>Generated Prompt:</h3>
                        <p style={styles.resultText}>{generatedPrompt}</p>
                        <button 
                            style={styles.copyBtn}
                            onClick={() => navigator.clipboard.writeText(generatedPrompt)}
                        >
                            Copy to Clipboard
                        </button>
                    </div>
                )}
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
        fontSize: '1.5rem',
        color: '#0f172a',
        fontWeight: '800',
        marginBottom: '0.25rem',
    },
    subtitle: {
        color: '#64748b',
        fontSize: '1.1rem',
    },
    infoCard: {
        backgroundColor: '#eff6ff',
        color: '#1e40af',
        padding: '1rem 1.5rem',
        borderRadius: '12px',
        marginBottom: '2rem',
        border: '1px solid #bfdbfe',
        fontSize: '0.95rem',
    },
    card: {
        backgroundColor: 'white',
        borderRadius: '24px',
        padding: '2rem',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
        border: '1px solid rgba(0, 0, 0, 0.05)',
        display: 'flex',
        flexDirection: 'column',
        gap: '2rem',
    },
    options: {
        display: 'flex',
        gap: '1rem',
        flexWrap: 'wrap',
    },
    optionBtn: {
        padding: '0.6rem 1.2rem',
        borderRadius: '10px',
        border: '1px solid #e2e8f0',
        backgroundColor: 'white',
        color: '#64748b',
        fontSize: '0.9rem',
        fontWeight: '600',
        cursor: 'pointer',
        transition: 'all 0.2s',
    },
    activeOption: {
        backgroundColor: '#3b82f6',
        color: 'white',
        borderColor: '#3b82f6',
    },
    generateBtn: {
        backgroundColor: '#0f172a',
        color: 'white',
        border: 'none',
        borderRadius: '12px',
        padding: '1rem',
        fontSize: '1rem',
        fontWeight: '700',
        cursor: 'pointer',
        transition: 'background-color 0.2s',
    },
    result: {
        marginTop: '1rem',
        padding: '1.5rem',
        backgroundColor: '#f8fafc',
        borderRadius: '16px',
        border: '1px solid #e2e8f0',
    },
    resultTitle: {
        fontSize: '0.9rem',
        fontWeight: '700',
        color: '#475569',
        marginBottom: '0.75rem',
    },
    resultText: {
        fontSize: '1rem',
        lineHeight: '1.6',
        color: '#1e293b',
        marginBottom: '1.25rem',
    },
    copyBtn: {
        backgroundColor: 'white',
        color: '#0f172a',
        border: '1px solid #e2e8f0',
        borderRadius: '8px',
        padding: '0.5rem 1rem',
        fontSize: '0.875rem',
        fontWeight: '600',
        cursor: 'pointer',
    }
};

export default PromptGeneration;

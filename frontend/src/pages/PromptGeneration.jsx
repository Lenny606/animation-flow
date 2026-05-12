import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSelection } from '../context/SelectionContext';

const SceneCard = ({ idx, scene, hoveredIdx, setHoveredIdx, onRegenerate, isGlobalGenerating }) => {
    const [feedback, setFeedback] = useState('');
    const [isRegenerating, setIsRegenerating] = useState(false);

    const handleRefine = async () => {
        if (!feedback.trim()) return;
        setIsRegenerating(true);
        try {
            await onRegenerate(feedback);
            setFeedback('');
        } finally {
            setIsRegenerating(false);
        }
    };

    return (
        <div 
            style={{
                ...styles.sceneCard,
                ...(hoveredIdx === idx ? styles.sceneCardHover : {})
            }}
            onMouseEnter={() => setHoveredIdx(idx)}
            onMouseLeave={() => setHoveredIdx(null)}
        >
            <div style={styles.sceneHeader}>
                <span style={styles.sceneNumber}>Scene {scene.scene || idx + 1}</span>
                <button 
                    style={styles.inlineCopyBtn}
                    onClick={() => navigator.clipboard.writeText(scene.prompt)}
                    aria-label={"Copy prompt for Scene " + (scene.scene || idx + 1)}
                >
                    Copy
                </button>
            </div>
            <p style={styles.scenePrompt}>{scene.prompt}</p>
            
            <div style={styles.feedbackSection}>
                <input 
                    type="text" 
                    placeholder="Add feedback..."
                    style={styles.feedbackInput}
                    value={feedback}
                    onChange={(e) => setFeedback(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleRefine()}
                    disabled={isRegenerating || isGlobalGenerating}
                />
                <button 
                    style={{
                        ...styles.refineBtn,
                        ...(isRegenerating || isGlobalGenerating || !feedback.trim() ? styles.disabledRefineBtn : {})
                    }}
                    onClick={handleRefine}
                    disabled={isRegenerating || isGlobalGenerating || !feedback.trim()}
                    aria-label={"Refine prompt for Scene " + (scene.scene || idx + 1)}
                >
                    {isRegenerating ? '...' : '✨'}
                </button>
            </div>
        </div>
    );
};

const PromptGeneration = () => {
    const { selection, setStyleSelection, setImageCountSelection } = useSelection();
    const [generatedPrompt, setGeneratedPrompt] = useState(() => {
        return localStorage.getItem('lastGeneratedPrompt') || '';
    });
    const [isGenerating, setIsGenerating] = useState(false);
    const [hoveredIdx, setHoveredIdx] = useState(null);
    const navigate = useNavigate();

    React.useEffect(() => {
        if (generatedPrompt) {
            localStorage.setItem('lastGeneratedPrompt', generatedPrompt);
        } else {
            localStorage.removeItem('lastGeneratedPrompt');
        }
    }, [generatedPrompt]);

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
                    style: selection.style || 'pastel-cartoon',
                    image_count: selection.imageCount || 4
                }),
                credentials: 'include',
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

    const handleRegenerateScene = async (sceneIdx, feedback, currentPrompts) => {
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
                    style: selection.style || 'pastel-cartoon',
                    image_count: selection.imageCount || 4,
                    feedback: feedback,
                    scene_index: sceneIdx,
                    current_prompts: currentPrompts
                }),
                credentials: 'include',
            });

            if (!response.ok) throw new Error('Failed to regenerate prompt');
            
            const data = await response.json();
            setGeneratedPrompt(data.optimized_text);
        } catch (error) {
            console.error('Error regenerating prompt:', error);
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
                <div style={styles.controlsRow}>
                    <div style={styles.controlItem}>
                        <label style={styles.label}>Visual Style</label>
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
                    </div>

                    <div style={styles.controlItem}>
                        <label style={styles.label}>Number of Scenes</label>
                        <select 
                            style={styles.select}
                            value={selection.imageCount || 4}
                            onChange={(e) => setImageCountSelection(parseInt(e.target.value))}
                        >
                            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(n => (
                                <option key={n} value={n}>{n} {n === 1 ? 'Scene' : 'Scenes'}</option>
                            ))}
                        </select>
                    </div>
                </div>

                <button 
                    style={{
                        ...styles.generateBtn, 
                        ...(!selection.song ? styles.disabledBtn : {})
                    }} 
                    onClick={handleGenerate}
                    disabled={isGenerating || !selection.song}
                >
                    {!selection.song ? 'Please Select a Song First' : (isGenerating ? 'Analyzing...' : 'Generate Optimized Prompt ✨')}
                </button>

                {generatedPrompt && (() => {
                    let parsedData = null;
                    try {
                        // Check if it's a JSON string (possibly wrapped in markdown)
                        let cleanJson = generatedPrompt.trim();
                        if (cleanJson.startsWith('```json')) {
                            cleanJson = cleanJson.replace(/```json|```/g, '').trim();
                        } else if (cleanJson.startsWith('```')) {
                            cleanJson = cleanJson.replace(/```/g, '').trim();
                        }
                        parsedData = JSON.parse(cleanJson);
                    } catch {
                        parsedData = null;
                    }

                    if (parsedData && parsedData.image_prompts) {
                        return (
                            <div style={styles.resultContainer}>
                                <div style={styles.resultHeader}>
                                    <div>
                                        <h3 style={styles.resultMainTitle}>{parsedData.title || selection.song.title}</h3>
                                        <p style={styles.resultSubtitle}>Visual Style: <span style={styles.styleBadge}>{parsedData.style || selection.style}</span></p>
                                    </div>
                                    <button 
                                        style={styles.copyAllBtn}
                                        onClick={() => navigator.clipboard.writeText(generatedPrompt)}
                                    >
                                        Copy JSON
                                    </button>
                                </div>
                                <div style={styles.scenesGrid}>
                                    {parsedData.image_prompts.map((scene, idx) => (
                                        <SceneCard 
                                            key={idx}
                                            idx={idx}
                                            scene={scene}
                                            hoveredIdx={hoveredIdx}
                                            setHoveredIdx={setHoveredIdx}
                                            onRegenerate={(feedback) => handleRegenerateScene(idx, feedback, parsedData.image_prompts)}
                                            isGlobalGenerating={isGenerating}
                                        />
                                    ))}
                                </div>
                                <div style={styles.nextButtonContainer}>
                                    <button 
                                        style={styles.nextButton}
                                        onClick={() => navigate('/image-generation')}
                                    >
                                        Next Stage ➔
                                    </button>
                                </div>
                            </div>
                        );
                    }

                    return (
                        <>
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
                            <div style={styles.nextButtonContainer}>
                                <button 
                                    style={styles.nextButton}
                                    onClick={() => navigate('/image-generation')}
                                >
                                    Next Stage ➔
                                </button>
                            </div>
                        </>
                    );
                })()}
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
        gap: '0.75rem',
        flexWrap: 'wrap',
    },
    controlsRow: {
        display: 'flex',
        flexDirection: 'column',
        gap: '2rem',
    },
    controlItem: {
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
    },
    label: {
        fontSize: '0.9rem',
        fontWeight: '700',
        color: '#475569',
        textTransform: 'uppercase',
        letterSpacing: '0.05em',
    },
    select: {
        padding: '0.75rem 1rem',
        borderRadius: '12px',
        border: '1px solid #e2e8f0',
        backgroundColor: '#f8fafc',
        color: '#0f172a',
        fontSize: '1rem',
        fontWeight: '600',
        cursor: 'pointer',
        width: 'fit-content',
        minWidth: '150px',
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
    disabledBtn: {
        backgroundColor: '#94a3b8',
        cursor: 'not-allowed',
        opacity: 0.7,
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
    },
    resultContainer: {
        marginTop: '2rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '1.5rem',
    },
    resultHeader: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderBottom: '1px solid #f1f5f9',
        paddingBottom: '1rem',
    },
    resultMainTitle: {
        fontSize: '1.25rem',
        fontWeight: '800',
        color: '#0f172a',
        marginBottom: '0.25rem',
    },
    resultSubtitle: {
        fontSize: '0.875rem',
        color: '#64748b',
    },
    styleBadge: {
        display: 'inline-block',
        padding: '2px 8px',
        backgroundColor: '#f1f5f9',
        borderRadius: '6px',
        color: '#334155',
        fontWeight: '600',
    },
    copyAllBtn: {
        padding: '0.5rem 1rem',
        backgroundColor: '#f8fafc',
        border: '1px solid #e2e8f0',
        borderRadius: '8px',
        color: '#64748b',
        fontSize: '0.75rem',
        fontWeight: '600',
        cursor: 'pointer',
    },
    scenesGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
        gap: '1rem',
    },
    sceneCard: {
        backgroundColor: '#f8fafc',
        borderRadius: '16px',
        padding: '1.25rem',
        border: '1px solid #e2e8f0',
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
        transition: 'transform 0.2s, box-shadow 0.2s',
        cursor: 'default',
    },
    sceneCardHover: {
        transform: 'translateY(-4px)',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    },
    sceneHeader: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    sceneNumber: {
        backgroundColor: '#3b82f6',
        color: 'white',
        fontSize: '0.75rem',
        fontWeight: '800',
        padding: '2px 10px',
        borderRadius: '20px',
        textTransform: 'uppercase',
    },
    inlineCopyBtn: {
        backgroundColor: 'transparent',
        border: 'none',
        color: '#3b82f6',
        fontSize: '0.75rem',
        fontWeight: '700',
        cursor: 'pointer',
        padding: '0',
    },
    scenePrompt: {
        fontSize: '0.9rem',
        lineHeight: '1.5',
        color: '#1e293b',
        margin: 0,
        fontStyle: 'italic',
    },
    nextButtonContainer: {
        marginTop: '3.5rem',
        display: 'flex',
        justifyContent: 'center',
        padding: '2rem 0',
        borderTop: '1px solid #f1f5f9',
    },
    nextButton: {
        backgroundColor: '#3b82f6',
        color: 'white',
        border: 'none',
        borderRadius: '12px',
        padding: '1rem 3.5rem',
        fontSize: '1.1rem',
        fontWeight: '700',
        cursor: 'pointer',
        boxShadow: '0 10px 15px -3px rgba(59, 130, 246, 0.4)',
        transition: 'all 0.2s',
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
    },
    feedbackSection: {
        display: 'flex',
        gap: '0.5rem',
        marginTop: 'auto',
        paddingTop: '0.75rem',
        borderTop: '1px solid #f1f5f9',
    },
    feedbackInput: {
        flex: 1,
        padding: '0.4rem 0.75rem',
        borderRadius: '8px',
        border: '1px solid #e2e8f0',
        fontSize: '0.8rem',
        backgroundColor: 'white',
    },
    refineBtn: {
        backgroundColor: '#0f172a',
        color: 'white',
        border: 'none',
        borderRadius: '8px',
        width: '32px',
        height: '32px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        cursor: 'pointer',
        fontSize: '0.9rem',
        transition: 'all 0.2s',
    },
    disabledRefineBtn: {
        backgroundColor: '#e2e8f0',
        color: '#94a3b8',
        cursor: 'not-allowed',
    }
};

export default PromptGeneration;

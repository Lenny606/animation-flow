import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSelection } from '../context/SelectionContext';

const ImageGeneration = () => {
    const navigate = useNavigate();
    const { selection } = useSelection();
    const [parsedData, setParsedData] = useState(null);
    const [imageUrls, setImageUrls] = useState({});
    const [isGenerating, setIsGenerating] = useState({});
    const [hoveredIdx, setHoveredIdx] = useState(null);

    useEffect(() => {
        const lastPrompt = localStorage.getItem('lastGeneratedPrompt');
        if (lastPrompt) {
            try {
                let cleanJson = lastPrompt.trim();
                if (cleanJson.startsWith('```json')) {
                    cleanJson = cleanJson.replace(/```json|```/g, '').trim();
                } else if (cleanJson.startsWith('```')) {
                    cleanJson = cleanJson.replace(/```/g, '').trim();
                }
                const data = JSON.parse(cleanJson);
                setParsedData(data);
                
                // Load cached image URLs if any
                const cachedImages = localStorage.getItem('generatedImages');
                if (cachedImages) {
                    setImageUrls(JSON.parse(cachedImages));
                }
            } catch (e) {
                console.error("Failed to parse prompt from cache", e);
            }
        }
    }, []);

    const handleGenerateImage = async (idx, prompt) => {
        setIsGenerating(prev => ({ ...prev, [idx]: true }));
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/assets/generate-single`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

            if (!response.ok) throw new Error('Failed to generate image');
            
            const data = await response.json();
            const newUrls = { ...imageUrls, [idx]: data.image_url };
            setImageUrls(newUrls);
            localStorage.setItem('generatedImages', JSON.stringify(newUrls));
        } catch (error) {
            console.error('Error generating image:', error);
        } finally {
            setIsGenerating(prev => ({ ...prev, [idx]: false }));
        }
    };

    if (!parsedData) {
        return (
            <div style={styles.container}>
                <div style={styles.content}>
                    <p>No prompt found. Please generate a prompt first.</p>
                    <button onClick={() => navigate('/prompts')} style={styles.primaryButton}>Go to Prompts</button>
                </div>
            </div>
        );
    }

    return (
        <div style={styles.container}>
            <header style={styles.header}>
                <button onClick={() => navigate('/prompts')} style={styles.backLink}>← Back to Prompts</button>
                <h1 style={styles.title}>Image Generation</h1>
                <p style={styles.subtitle}>Bring your scenes to life with AI-generated visuals.</p>
            </header>

            <div style={styles.infoCard}>
                <strong>Song:</strong> {parsedData.title || selection.song?.title} | <strong>Style:</strong> {parsedData.style || selection.style}
            </div>

            <div style={styles.scenesGrid}>
                {parsedData.image_prompts.map((scene, idx) => (
                    <div 
                        key={idx} 
                        style={{
                            ...styles.sceneCard,
                            ...(hoveredIdx === idx ? styles.sceneCardHover : {})
                        }}
                        onMouseEnter={() => setHoveredIdx(idx)}
                        onMouseLeave={() => setHoveredIdx(null)}
                    >
                        <div style={styles.imagePreview}>
                            {imageUrls[idx] ? (
                                <img 
                                    src={imageUrls[idx]} 
                                    alt={`Scene ${idx + 1}`} 
                                    style={styles.sceneImage}
                                    onError={(e) => {
                                        console.error("Image load failed", e);
                                        // Optionally remove from state if it's a persistent error
                                    }}
                                />
                            ) : (
                                <div style={styles.placeholder}>
                                    {isGenerating[idx] ? 'Generating Visual... ✨' : 'No image yet'}
                                </div>
                            )}
                        </div>
                        <div style={styles.sceneInfo}>
                            <span style={styles.sceneNumber}>Scene {scene.scene || idx + 1}</span>
                            <p style={styles.scenePrompt}>{scene.prompt}</p>
                            <button 
                                style={{
                                    ...styles.generateBtn,
                                    ...(isGenerating[idx] ? styles.generating : {})
                                }}
                                onClick={() => handleGenerateImage(idx, scene.prompt)}
                                disabled={isGenerating[idx]}
                            >
                                {isGenerating[idx] ? 'Working...' : (imageUrls[idx] ? 'Regenerate 🔄' : 'Generate Image ✨')}
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            <div style={styles.nextButtonContainer}>
                <button style={styles.nextButton}>
                    Next Stage: Video Assembly ➔
                </button>
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
        marginBottom: '2rem',
    },
    backLink: {
        background: 'none',
        border: 'none',
        color: '#3b82f6',
        fontSize: '0.9rem',
        fontWeight: '600',
        cursor: 'pointer',
        padding: 0,
        marginBottom: '1rem',
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
        fontSize: '0.9rem',
    },
    scenesGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
        gap: '2rem',
    },
    sceneCard: {
        backgroundColor: 'white',
        borderRadius: '24px',
        overflow: 'hidden',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
        border: '1px solid rgba(0, 0, 0, 0.05)',
        display: 'flex',
        flexDirection: 'column',
        transition: 'transform 0.2s, box-shadow 0.2s',
    },
    sceneCardHover: {
        transform: 'translateY(-4px)',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    },
    imagePreview: {
        width: '100%',
        aspectRatio: '16/9',
        backgroundColor: '#f1f5f9',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
    },
    sceneImage: {
        width: '100%',
        height: '100%',
        objectFit: 'cover',
    },
    placeholder: {
        color: '#94a3b8',
        fontSize: '0.9rem',
        fontWeight: '600',
    },
    sceneInfo: {
        padding: '1.5rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
        flex: 1,
    },
    sceneNumber: {
        backgroundColor: '#3b82f6',
        color: 'white',
        fontSize: '0.75rem',
        fontWeight: '800',
        padding: '2px 10px',
        borderRadius: '20px',
        textTransform: 'uppercase',
        alignSelf: 'flex-start',
    },
    scenePrompt: {
        fontSize: '0.95rem',
        lineHeight: '1.5',
        color: '#1e293b',
        margin: 0,
        fontStyle: 'italic',
        flex: 1,
    },
    generateBtn: {
        backgroundColor: '#0f172a',
        color: 'white',
        border: 'none',
        borderRadius: '12px',
        padding: '0.75rem',
        fontSize: '0.9rem',
        fontWeight: '700',
        cursor: 'pointer',
        transition: 'background-color 0.2s',
    },
    generating: {
        backgroundColor: '#64748b',
        cursor: 'not-allowed',
    },
    nextButtonContainer: {
        marginTop: '4rem',
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
        padding: '1rem 3rem',
        fontSize: '1.1rem',
        fontWeight: '700',
        cursor: 'pointer',
        boxShadow: '0 10px 15px -3px rgba(59, 130, 246, 0.4)',
        transition: 'all 0.2s',
    },
    primaryButton: {
        backgroundColor: '#3b82f6',
        color: 'white',
        border: 'none',
        borderRadius: '12px',
        padding: '0.75rem 1.5rem',
        fontSize: '1rem',
        fontWeight: '600',
        cursor: 'pointer',
        marginTop: '1rem',
    },
    content: {
        textAlign: 'center',
        padding: '4rem 2rem',
    }
};

export default ImageGeneration;

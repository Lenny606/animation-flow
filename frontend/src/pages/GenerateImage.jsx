import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const GenerateImage = () => {
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false);
    const [step, setStep] = useState(1); // 1: Form, 2: Scenario Ready, 3: Images Ready, 4: Plan Review, 5: Result
    const [error, setError] = useState('');
    const [songs, setSongs] = useState([]);
    const [showSongSelect, setShowSongSelect] = useState(false);

    // Form State
    const [formData, setFormData] = useState({
        topic: '',
        style: 'cinematic',
        target_audience: 'General Audience',
        duration: 30,
        llm_provider: 'openai'
    });

    const [scenario, setScenario] = useState(null);
    const [images, setImages] = useState([]);
    const [plan, setPlan] = useState(null);
    const [videoAssets, setVideoAssets] = useState([]);

    const getAuthHeaders = () => {
        const token = localStorage.getItem('token');
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
    };

    const fetchSongs = async () => {
        try {
            const apiUrl = import.meta.env.VITE_API_URL || '';
            const normalizedApiUrl = apiUrl.startsWith('http') ? apiUrl : `https://${apiUrl}`;
            const response = await fetch(`${normalizedApiUrl}/songs/`, {
                headers: getAuthHeaders(),
            });
            if (response.ok) {
                const data = await response.json();
                setSongs(data);
            }
        } catch (err) {
            console.error('Failed to fetch songs:', err);
        }
    };

    useEffect(() => {
        fetchSongs();
    }, []);

    const handleSongSelect = (e) => {
        const songId = e.target.value;
        const selectedSong = songs.find(s => s._id === songId || s.id === songId);
        if (selectedSong) {
            setFormData(prev => ({
                ...prev,
                topic: `${selectedSong.title}: ${selectedSong.text.substring(0, 200)}`
            }));
            setShowSongSelect(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleGenerateScenario = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            const apiUrl = import.meta.env.VITE_API_URL || '';
            const normalizedApiUrl = apiUrl.startsWith('http') ? apiUrl : `https://${apiUrl}`;

            const response = await fetch(`${normalizedApiUrl}/scenarios/generate`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(formData),
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Failed to generate scenario');

            setScenario(data);
            setStep(2);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const handleGenerateImages = async () => {
        setIsLoading(true);
        setError('');

        try {
            const apiUrl = import.meta.env.VITE_API_URL || '';
            const normalizedApiUrl = apiUrl.startsWith('http') ? apiUrl : `https://${apiUrl}`;

            const response = await fetch(`${normalizedApiUrl}/assets/generate_from_scenario`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify({
                    scenario: scenario,
                    llm_provider: formData.llm_provider
                }),
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Failed to generate images');

            setImages(data);
            setStep(3);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const handleGeneratePlan = async () => {
        setIsLoading(true);
        setError('');

        try {
            const apiUrl = import.meta.env.VITE_API_URL || '';
            const normalizedApiUrl = apiUrl.startsWith('http') ? apiUrl : `https://${apiUrl}`;

            // Prepare request for video planning
            const requestBody = {
                scenario_id: scenario.id || "temp-id",
                image_assets: images,
                provider: "mock", // Default for now
                generate_voiceover: false
            };

            const response = await fetch(`${normalizedApiUrl}/video/plan`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(requestBody),
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Failed to generate plan');

            setPlan(data);
            setStep(4);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const handleExecutePlan = async () => {
        setIsLoading(true);
        setError('');

        try {
            const apiUrl = import.meta.env.VITE_API_URL || '';
            const normalizedApiUrl = apiUrl.startsWith('http') ? apiUrl : `https://${apiUrl}`;

            const response = await fetch(`${normalizedApiUrl}/video/execute`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify({ plan_id: plan.plan_id }),
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Failed to execute plan');

            setVideoAssets(data);
            setStep(5);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const renderForm = () => (
        <form onSubmit={handleGenerateScenario} style={styles.form}>
            <div style={styles.inputGroup}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <label htmlFor="topic" style={styles.label}>Topic</label>
                    {songs.length > 0 && (
                        <button
                            type="button"
                            onClick={() => setShowSongSelect(!showSongSelect)}
                            style={{ ...styles.linkButton, ...(isLoading ? styles.disabledInput : {}) }}
                            disabled={isLoading}
                        >
                            {showSongSelect ? 'Cancel' : 'Select from saved songs'}
                        </button>
                    )}
                </div>
                {showSongSelect && (
                    <select
                        onChange={handleSongSelect}
                        style={{ ...styles.songSelect, ...(isLoading ? styles.disabledInput : {}) }}
                        defaultValue=""
                        aria-label="Select a saved song"
                        disabled={isLoading}
                    >
                        <option value="" disabled>-- Pick a song --</option>
                        {songs.map(song => (
                            <option key={song._id || song.id} value={song._id || song.id}>
                                {song.title} ({song.category})
                            </option>
                        ))}
                    </select>
                )}
                <input
                    id="topic"
                    name="topic"
                    value={formData.topic}
                    onChange={handleInputChange}
                    placeholder="e.g. The future of robotics"
                    required
                    style={{ ...styles.input, ...(isLoading ? styles.disabledInput : {}) }}
                    disabled={isLoading}
                />
            </div>
            <div style={styles.row}>
                <div style={styles.inputGroup}>
                    <label htmlFor="style" style={styles.label}>Style</label>
                    <select
                        id="style"
                        name="style"
                        value={formData.style}
                        onChange={handleInputChange}
                        style={{ ...styles.select, ...(isLoading ? styles.disabledInput : {}) }}
                        disabled={isLoading}
                    >
                        <option value="cinematic">Cinematic</option>
                        <option value="anime">Anime</option>
                        <option value="3d-render">3D Render</option>
                        <option value="sketch">Sketch</option>
                    </select>
                </div>
                <div style={styles.inputGroup}>
                    <label htmlFor="duration" style={styles.label}>Duration (sec)</label>
                    <input
                        id="duration"
                        type="number"
                        name="duration"
                        value={formData.duration}
                        onChange={handleInputChange}
                        style={{ ...styles.input, ...(isLoading ? styles.disabledInput : {}) }}
                        disabled={isLoading}
                    />
                </div>
            </div>
            <button type="submit" style={{ ...styles.primaryButton, ...(isLoading ? styles.disabledButton : {}) }} disabled={isLoading}>
                {isLoading ? 'Planning Storyboard...' : 'Generate Storyboard'}
            </button>
        </form>
    );

    const renderScenario = () => (
        <div style={styles.scenarioPreview}>
            <h3 style={styles.subTitle}>{scenario.title}</h3>
            <div style={styles.sceneList}>
                {scenario.scenes.map((scene, idx) => (
                    <div key={idx} style={styles.sceneCard}>
                        <strong>Scene {scene.id}:</strong> {scene.visual_description}
                    </div>
                ))}
            </div>
            <div style={styles.buttonGroup}>
                <button onClick={() => setStep(1)} style={styles.secondaryButton}>Edit Prompt</button>
                <button onClick={handleGenerateImages} style={{ ...styles.primaryButton, ...(isLoading ? styles.disabledButton : {}) }} disabled={isLoading}>
                    {isLoading ? 'Generating Images...' : 'Generate AI Images'}
                </button>
            </div>
        </div>
    );

    const renderImages = () => (
        <div style={styles.stepContainer}>
            <div style={styles.imageGrid}>
                {images.map((img, idx) => (
                    <div key={idx} style={styles.imageCard}>
                        <img src={img.image_url} alt={`Scene ${img.order}`} style={styles.image} />
                        <p style={styles.imageLabel}>Frame {img.order}</p>
                    </div>
                ))}
            </div>
            <div style={styles.buttonGroupCenter}>
                <button onClick={() => setStep(1)} style={styles.secondaryButton}>Start Over</button>
                <button onClick={handleGeneratePlan} style={{ ...styles.primaryButton, ...(isLoading ? styles.disabledButton : {}) }} disabled={isLoading}>
                    {isLoading ? 'Generating Plan...' : 'Generate Video Plan'}
                </button>
            </div>
        </div>
    );

    const renderPlan = () => (
        <div style={styles.scenarioPreview}>
            <h3 style={styles.subTitle}>Review Execution Plan</h3>
            <p style={styles.description}>The AI Agent has prepared the following plan. Please confirm execution.</p>
            <div style={styles.sceneList}>
                {plan.script.map((step, idx) => (
                    <div key={idx} style={styles.sceneCard}>
                        <strong>Step {idx + 1}:</strong> {step}
                    </div>
                ))}
            </div>
            <div style={styles.buttonGroup}>
                <button onClick={() => setStep(3)} style={styles.secondaryButton}>Back to Images</button>
                <button onClick={handleExecutePlan} style={{ ...styles.primaryButton, ...(isLoading ? styles.disabledButton : {}) }} disabled={isLoading}>
                    {isLoading ? 'Executing Plan...' : 'Confirm & Execute'}
                </button>
            </div>
        </div>
    );

    const renderProgress = () => {
        const totalSteps = 5;
        return (
            <div
                style={styles.progressContainer}
                role="progressbar"
                aria-valuenow={step}
                aria-valuemin="1"
                aria-valuemax={totalSteps}
                aria-label={`Step ${step} of ${totalSteps}`}
            >
                {Array.from({ length: totalSteps }, (_, i) => i + 1).map((s) => (
                    <React.Fragment key={s}>
                        <div
                            style={{
                                ...styles.progressDot,
                                ...(s < step ? styles.progressDotCompleted : {}),
                                ...(s === step ? styles.progressDotActive : {})
                            }}
                            aria-current={s === step ? "step" : undefined}
                            title={`Step ${s}`}
                        >
                            {s < step ? '✓' : s}
                        </div>
                        {s < totalSteps && (
                            <div
                                style={{
                                    ...styles.progressLine,
                                    ...(s < step ? styles.progressLineCompleted : {})
                                }}
                            />
                        )}
                    </React.Fragment>
                ))}
            </div>
        );
    };

    const renderFinalVideo = () => (
        <div style={styles.stepContainer}>
            <h3 style={styles.subTitleSuccess}>Video Generation Complete!</h3>
            <div style={styles.videoGrid}>
                {videoAssets.map((asset, idx) => (
                    <div key={idx} style={styles.videoCard}>
                        <video controls style={styles.video} src={asset.video_url}></video>
                        <p style={styles.imageLabel}>Format: {asset.provider}</p>
                    </div>
                ))}
            </div>
            <div style={styles.buttonGroupCenter}>
                <button onClick={() => setStep(1)} style={styles.primaryButton}>Create New Project</button>
            </div>
        </div>
    );

    return (
        <div style={styles.container}>
            <div style={styles.content}>
                <button onClick={() => navigate('/home')} style={styles.backButton}>← Back Home</button>
                <h1 style={styles.title}>AI Generation Flow</h1>

                {renderProgress()}

                <p style={styles.description}>
                    {step === 1 && "Start by describing your vision."}
                    {step === 2 && "The AI has planned your storyboard. Ready to generate?"}
                    {step === 3 && "Your AI assets are ready. Proceed to video planning?"}
                    {step === 4 && "Review the Agent's plan before execution."}
                    {step === 5 && "Here is your generated video content."}
                </p>

                {error && <div style={styles.error}>{error}</div>}

                {step === 1 && renderForm()}
                {step === 2 && renderScenario()}
                {step === 3 && renderImages()}
                {step === 4 && renderPlan()}
                {step === 5 && renderFinalVideo()}
            </div>
        </div>
    );
};

const styles = {
    container: {
        minHeight: '100vh',
        backgroundColor: '#f8fafc',
        padding: '2rem',
        display: 'flex',
        justifyContent: 'center',
        fontFamily: "'Inter', sans-serif",
    },
    content: {
        width: '100%',
        maxWidth: '800px',
        backgroundColor: '#ffffff',
        padding: '3rem',
        borderRadius: '24px',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.05)',
    },
    title: {
        color: '#0f172a',
        fontSize: '2rem',
        fontWeight: '800',
        marginBottom: '0.5rem',
        textAlign: 'center',
    },
    subTitle: {
        fontSize: '1.25rem',
        color: '#1e293b',
        marginBottom: '1rem',
    },
    description: {
        color: '#64748b',
        textAlign: 'center',
        marginBottom: '2.5rem',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
        gap: '1.5rem',
    },
    row: {
        display: 'flex',
        gap: '1rem',
    },
    inputGroup: {
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem',
    },
    label: {
        fontSize: '0.875rem',
        fontWeight: '600',
        color: '#475569',
    },
    input: {
        padding: '0.75rem 1rem',
        borderRadius: '12px',
        border: '1px solid #e2e8f0',
        fontSize: '1rem',
        transition: 'border-color 0.2s',
    },
    disabledInput: {
        backgroundColor: '#f1f5f9',
        cursor: 'not-allowed',
        opacity: 0.7,
    },
    select: {
        padding: '0.75rem 1rem',
        borderRadius: '12px',
        border: '1px solid #e2e8f0',
        fontSize: '1rem',
        backgroundColor: '#fff',
    },
    primaryButton: {
        padding: '1rem',
        borderRadius: '12px',
        border: 'none',
        backgroundColor: '#3b82f6',
        color: 'white',
        fontSize: '1rem',
        fontWeight: '600',
        cursor: 'pointer',
        transition: 'background-color 0.2s',
        marginTop: '1rem',
    },
    disabledButton: {
        backgroundColor: '#94a3b8',
        cursor: 'not-allowed',
        opacity: 0.7,
    },
    secondaryButton: {
        padding: '1rem',
        borderRadius: '12px',
        border: '1px solid #e2e8f0',
        backgroundColor: 'white',
        color: '#475569',
        fontSize: '1rem',
        fontWeight: '600',
        cursor: 'pointer',
    },
    backButton: {
        background: 'none',
        border: 'none',
        color: '#64748b',
        cursor: 'pointer',
        marginBottom: '1rem',
        fontSize: '1rem',
    },
    error: {
        padding: '1rem',
        backgroundColor: '#fef2f2',
        color: '#dc2626',
        borderRadius: '12px',
        marginBottom: '1.5rem',
        fontSize: '0.875rem',
        textAlign: 'center',
    },
    scenarioPreview: {
        display: 'flex',
        flexDirection: 'column',
        gap: '1.5rem',
    },
    sceneList: {
        display: 'flex',
        flexDirection: 'column',
        gap: '0.75rem',
        maxHeight: '400px',
        overflowY: 'auto',
        padding: '1rem',
        backgroundColor: '#f1f5f9',
        borderRadius: '16px',
    },
    sceneCard: {
        padding: '1rem',
        backgroundColor: '#fff',
        borderRadius: '8px',
        fontSize: '0.875rem',
        lineHeight: '1.5',
        color: '#334155',
        boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
    },
    buttonGroup: {
        display: 'flex',
        gap: '1rem',
        justifyContent: 'flex-end',
    },
    imageGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
        gap: '1.5rem',
        marginBottom: '2rem',
    },
    imageCard: {
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem',
    },
    image: {
        width: '100%',
        aspectRatio: '16/9',
        borderRadius: '12px',
        objectFit: 'cover',
        boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
    },
    imageLabel: {
        fontSize: '0.75rem',
        color: '#94a3b8',
        textAlign: 'center',
    },
    stepContainer: {
        display: 'flex',
        flexDirection: 'column',
        gap: '2rem',
    },
    buttonGroupCenter: {
        display: 'flex',
        gap: '1rem',
        justifyContent: 'center',
        marginTop: '1rem',
    },
    subTitleSuccess: {
        fontSize: '1.5rem',
        color: '#10b981',
        marginBottom: '1.5rem',
        textAlign: 'center',
        fontWeight: '700',
    },
    videoGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
        gap: '2rem',
        marginBottom: '2rem',
    },
    videoCard: {
        display: 'flex',
        flexDirection: 'column',
        gap: '0.75rem',
        backgroundColor: '#f8fafc',
        padding: '1rem',
        borderRadius: '16px',
    },
    video: {
        width: '100%',
        aspectRatio: '16/9',
        borderRadius: '8px',
        backgroundColor: '#000',
    },
    linkButton: {
        background: 'none',
        border: 'none',
        color: '#3b82f6',
        fontSize: '0.75rem',
        fontWeight: '600',
        cursor: 'pointer',
        padding: '0',
        textDecoration: 'underline',
    },
    songSelect: {
        padding: '0.75rem 1rem',
        borderRadius: '12px',
        border: '1px solid #3b82f6',
        fontSize: '0.9rem',
        backgroundColor: '#eff6ff',
        marginBottom: '0.5rem',
    },
    progressContainer: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        margin: '1.5rem 0 2rem 0',
        width: '100%',
    },
    progressDot: {
        width: '28px',
        height: '28px',
        borderRadius: '50%',
        backgroundColor: '#f1f5f9',
        color: '#94a3b8',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '0.875rem',
        fontWeight: '600',
        transition: 'all 0.3s ease',
        zIndex: 1,
    },
    progressDotActive: {
        backgroundColor: '#3b82f6',
        color: 'white',
        boxShadow: '0 0 0 4px rgba(59, 130, 246, 0.2)',
    },
    progressDotCompleted: {
        backgroundColor: '#10b981',
        color: 'white',
    },
    progressLine: {
        flex: 1,
        height: '3px',
        backgroundColor: '#f1f5f9',
        margin: '0 4px',
        maxWidth: '50px',
        transition: 'background-color 0.3s ease',
    },
    progressLineCompleted: {
        backgroundColor: '#10b981',
    }
};

export default GenerateImage;

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Modal from '../components/Modal';

const Home = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const navigate = useNavigate();

    return (
        <div style={styles.container}>
            <div style={styles.content}>
                <h1 style={styles.title}>Welcome to Animation Flow</h1>
                <div style={styles.buttonGroup}>
                    <button
                        onClick={() => navigate('/generate')}
                        style={{
                            ...styles.ctaButton,
                            ...styles.disabledCta
                        }}
                        disabled
                    >
                        Start Generation
                    </button>

                    <button
                        onClick={() => setIsModalOpen(true)}
                        style={styles.linkButton}
                    >
                        How does it work?
                    </button>
                </div>
            </div>

            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title="How AI Agents Work"
            >
                <div style={styles.modalContent}>
                    <div style={styles.point}>
                        <span style={styles.number}>1</span>
                        <div>
                            <strong style={styles.pointTitle}>Scene Analysis</strong>
                            <p style={styles.pointText}>The AI agent analyzes your prompt to understand the visual style, motion, and atmosphere you want to create.</p>
                        </div>
                    </div>
                    <div style={styles.point}>
                        <span style={styles.number}>2</span>
                        <div>
                            <strong style={styles.pointTitle}>Sequential Planning</strong>
                            <p style={styles.pointText}>It plans the frame-by-frame progression and chooses the best AI models for consistency and detail.</p>
                        </div>
                    </div>
                    <div style={styles.point}>
                        <span style={styles.number}>3</span>
                        <div>
                            <strong style={styles.pointTitle}>Drafting & Generation</strong>
                            <p style={styles.pointText}>The agent communicates with high-performance video engines to render the animation flow.</p>
                        </div>
                    </div>
                    <div style={styles.point}>
                        <span style={styles.number}>4</span>
                        <div>
                            <strong style={styles.pointTitle}>Final Rendering</strong>
                            <p style={styles.pointText}>Finally, it optimizes the video quality, ensuring smooth transitions and the perfect final result.</p>
                        </div>
                    </div>
                </div>
            </Modal>
        </div>
    );
};

const styles = {
    container: {
        width: '100%',
        padding: '2rem 0',
    },
    content: {
        textAlign: 'left',
        width: '100%',
    },
    title: {
        color: '#0f172a',
        fontSize: 'clamp(1.75rem, 5vw, 2.5rem)',
        marginBottom: '1rem',
        fontWeight: '800',
        letterSpacing: '-0.025em',
    },
    text: {
        color: '#64748b',
        fontSize: '1.125rem',
        lineHeight: '1.75',
        marginBottom: '2rem',
    },
    linkButton: {
        background: 'none',
        border: 'none',
        color: '#64748b',
        fontSize: '0.95rem',
        fontWeight: '500',
        cursor: 'pointer',
        textDecoration: 'underline',
        textUnderlineOffset: '4px',
        transition: 'color 0.2s',
        padding: '0.5rem 1rem',
    },
    buttonGroup: {
        display: 'flex',
        gap: '1rem',
        marginTop: '2rem',
    },
    ctaButton: {
        backgroundColor: '#3b82f6',
        color: 'white',
        border: 'none',
        borderRadius: '12px',
        padding: '0.75rem 2rem',
        fontSize: '1rem',
        fontWeight: '700',
        cursor: 'pointer',
        boxShadow: '0 4px 6px -1px rgba(59, 130, 246, 0.3)',
        transition: 'transform 0.2s, background-color 0.2s',
    },
    disabledCta: {
        backgroundColor: '#94a3b8',
        boxShadow: 'none',
        cursor: 'not-allowed',
        transform: 'none',
    },
    modalContent: {
        display: 'flex',
        flexDirection: 'column',
        gap: '1.5rem',
    },
    point: {
        display: 'flex',
        gap: '1rem',
        alignItems: 'flex-start',
    },
    number: {
        backgroundColor: '#eff6ff',
        color: '#3b82f6',
        width: '32px',
        height: '32px',
        borderRadius: '50%',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontWeight: '700',
        flexShrink: 0,
        fontSize: '0.875rem',
    },
    pointTitle: {
        display: 'block',
        color: '#1e293b',
        fontSize: '1rem',
        marginBottom: '0.25rem',
    },
    pointText: {
        margin: 0,
        color: '#64748b',
        fontSize: '0.925rem',
        lineHeight: '1.5',
    },
};

export default Home;


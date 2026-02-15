import React, { useState } from 'react';
import Modal from '../components/Modal';

const Home = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    return (
        <div style={styles.container}>
            <div style={styles.content}>
                <h1 style={styles.title}>Welcome to Animation Flow</h1>
                <p style={styles.text}>This is your simple responsive homepage.</p>

                <button
                    onClick={() => setIsModalOpen(true)}
                    style={styles.linkButton}
                >
                    How does it work?
                </button>
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
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        backgroundColor: '#f8fafc',
        padding: '20px',
        fontFamily: "'Inter', sans-serif",
    },
    content: {
        textAlign: 'center',
        backgroundColor: '#ffffff',
        padding: '3rem',
        borderRadius: '20px',
        boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05)',
        width: '100%',
        maxWidth: '500px',
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
        color: '#3b82f6',
        fontSize: '1rem',
        fontWeight: '600',
        cursor: 'pointer',
        textDecoration: 'underline',
        textUnderlineOffset: '4px',
        transition: 'color 0.2s',
        padding: '0.5rem 1rem',
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


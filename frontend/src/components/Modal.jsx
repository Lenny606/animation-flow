import React from 'react';

const Modal = ({ isOpen, onClose, title, children }) => {
    if (!isOpen) return null;

    return (
        <div style={styles.overlay} onClick={onClose}>
            <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
                <div style={styles.header}>
                    <h2 style={styles.title}>{title}</h2>
                    <button style={styles.closeButton} onClick={onClose}>&times;</button>
                </div>
                <div style={styles.content}>
                    {children}
                </div>
            </div>
        </div>
    );
};

const styles = {
    overlay: {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1000,
        backdropFilter: 'blur(4px)',
    },
    modal: {
        backgroundColor: '#fff',
        padding: '2rem',
        borderRadius: '16px',
        maxWidth: '500px',
        width: '90%',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        position: 'relative',
        animation: 'modalFadeIn 0.3s ease-out',
    },
    header: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '1.5rem',
        borderBottom: '1px solid #e5e7eb',
        paddingBottom: '1rem',
    },
    title: {
        margin: 0,
        fontSize: '1.5rem',
        color: '#111827',
        fontWeight: '600',
    },
    closeButton: {
        background: 'none',
        border: 'none',
        fontSize: '2rem',
        cursor: 'pointer',
        color: '#6b7280',
        lineHeight: 1,
        padding: '0 0.5rem',
        transition: 'color 0.2s',
    },
    content: {
        color: '#374151',
        lineHeight: '1.6',
    },
};

// Add fade-in animation via standard CSS in a real app, 
// but for this simple version we'll just use inline styles.
// In a full app, I'd put this in index.css

export default Modal;

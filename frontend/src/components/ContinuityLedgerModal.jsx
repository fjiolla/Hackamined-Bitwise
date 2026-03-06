import React, { useState } from 'react';

const ContinuityLedgerModal = ({ ledger }) => {
    const [isOpen, setIsOpen] = useState(false);

    if (!ledger) return null;

    if (!isOpen) {
        return (
            <button 
                onClick={() => setIsOpen(true)} 
                style={styles.floatingButton}
                title="Story Continuity"
            >
                📚 Ledger
            </button>
        );
    }

    return (
        <div style={styles.modalOverlay} onClick={() => setIsOpen(false)}>
            <div style={styles.modalContent} onClick={(e) => e.stopPropagation()}>
                <div style={styles.modalHeader}>
                    <h2 style={styles.modalTitle}>Continuity Ledger</h2>
                    <button onClick={() => setIsOpen(false)} style={styles.closeBtn}>×</button>
                </div>

                <div style={styles.modalScrollArea}>
                    
                    <div style={styles.section}>
                        <h3 style={styles.sectionTitle}>Characters Introduced</h3>
                        <div style={styles.tagContainer}>
                            {ledger.characters_introduced?.length > 0 ? (
                                ledger.characters_introduced.map((char, i) => (
                                    <span key={i} style={{...styles.tag, ...styles.tagGreen}}>{char}</span>
                                ))
                            ) : (
                                <span style={styles.emptyText}>None</span>
                            )}
                        </div>
                    </div>

                    <div style={styles.section}>
                        <h3 style={styles.sectionTitle}>Revealed Secrets</h3>
                        <div style={styles.tagContainer}>
                            {ledger.revealed_secrets?.length > 0 ? (
                                ledger.revealed_secrets.map((sec, i) => (
                                    <span key={i} style={{...styles.tag, ...styles.tagYellow}}>{sec}</span>
                                ))
                            ) : (
                                <span style={styles.emptyText}>None</span>
                            )}
                        </div>
                    </div>

                    <div style={styles.section}>
                        <h3 style={styles.sectionTitle}>Unresolved Threads</h3>
                        <div style={styles.tagContainer}>
                            {ledger.unresolved_threads?.length > 0 ? (
                                ledger.unresolved_threads.map((thr, i) => (
                                    <span key={i} style={{...styles.tag, ...styles.tagRed}}>{thr}</span>
                                ))
                            ) : (
                                <span style={styles.emptyText}>None</span>
                            )}
                        </div>
                    </div>

                    <div style={styles.section}>
                        <h3 style={styles.sectionTitle}>Timeline Events</h3>
                        <div style={styles.timelineList}>
                            {ledger.timeline_events?.length > 0 ? (
                                ledger.timeline_events.map((evt, i) => (
                                    <div key={i} style={styles.timelineItem}>
                                        <div style={styles.timelineDot}></div>
                                        <div style={styles.timelineText}>{evt}</div>
                                    </div>
                                ))
                            ) : (
                                <span style={styles.emptyText}>None</span>
                            )}
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

const styles = {
    floatingButton: {
        position: 'fixed',
        bottom: '30px',
        left: '30px',
        backgroundColor: 'var(--card-bg)',
        color: 'var(--text-primary)',
        border: '1px solid var(--border-color)',
        padding: '12px 24px',
        borderRadius: '30px',
        fontSize: '16px',
        fontWeight: '600',
        cursor: 'pointer',
        boxShadow: 'var(--box-shadow)',
        zIndex: 1000,
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
    },
    modalOverlay: {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        backdropFilter: 'blur(4px)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1001,
        padding: '20px'
    },
    modalContent: {
        backgroundColor: 'var(--bg-color)',
        width: '100%',
        maxWidth: '800px',
        maxHeight: '90vh',
        borderRadius: '16px',
        border: '1px solid var(--border-color)',
        boxShadow: '0 24px 48px rgba(0,0,0,0.5)',
        display: 'flex',
        flexDirection: 'column'
    },
    modalHeader: {
        padding: '24px 32px',
        borderBottom: '1px solid var(--border-color)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    modalTitle: {
        margin: 0,
        fontSize: '24px',
        fontWeight: '700'
    },
    closeBtn: {
        background: 'transparent',
        border: 'none',
        color: 'var(--text-secondary)',
        fontSize: '32px',
        lineHeight: '1',
        padding: '0',
        cursor: 'pointer',
        width: '32px',
        height: '32px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: '50%'
    },
    modalScrollArea: {
        padding: '32px',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '32px'
    },
    section: {
        display: 'flex',
        flexDirection: 'column',
        gap: '12px'
    },
    sectionTitle: {
        margin: 0,
        fontSize: '16px',
        fontWeight: '600',
        color: 'var(--text-primary)',
        textTransform: 'uppercase',
        letterSpacing: '1px'
    },
    tagContainer: {
        display: 'flex',
        flexWrap: 'wrap',
        gap: '8px'
    },
    tag: {
        padding: '6px 12px',
        borderRadius: '16px',
        fontSize: '13px',
        fontWeight: '500',
        border: '1px solid transparent'
    },
    tagGreen: {
        backgroundColor: 'rgba(0, 255, 136, 0.1)',
        color: 'var(--accent-color)',
        borderColor: 'rgba(0, 255, 136, 0.3)'
    },
    tagYellow: {
        backgroundColor: 'rgba(255, 170, 0, 0.1)',
        color: '#ffaa00',
        borderColor: 'rgba(255, 170, 0, 0.3)'
    },
    tagRed: {
        backgroundColor: 'rgba(255, 68, 68, 0.1)',
        color: '#ff4444',
        borderColor: 'rgba(255, 68, 68, 0.3)'
    },
    emptyText: {
        color: 'var(--text-secondary)',
        fontStyle: 'italic',
        fontSize: '14px'
    },
    timelineList: {
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
        borderLeft: '2px solid var(--border-color)',
        marginLeft: '12px',
        paddingLeft: '20px'
    },
    timelineItem: {
        position: 'relative',
        fontSize: '15px',
        color: 'var(--text-secondary)'
    },
    timelineDot: {
        position: 'absolute',
        left: '-27px',
        top: '6px',
        width: '12px',
        height: '12px',
        backgroundColor: 'var(--card-bg)',
        border: '2px solid var(--accent-color)',
        borderRadius: '50%'
    },
    timelineText: {
        lineHeight: '1.5'
    }
};

export default ContinuityLedgerModal;

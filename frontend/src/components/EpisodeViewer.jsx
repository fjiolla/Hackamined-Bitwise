import React, { useState } from 'react';

const EpisodeViewer = ({ episodes }) => {
    // Keep track of which scripts are toggled open (by episode number)
    const [openScripts, setOpenScripts] = useState({});

    if (!episodes || episodes.length === 0) {
        return null;
    }

    const toggleScript = (episodeNumber) => {
        setOpenScripts(prev => ({
            ...prev,
            [episodeNumber]: !prev[episodeNumber]
        }));
    };

    const handleDownload = (episodeNumber, scriptText) => {
        const element = document.createElement("a");
        const file = new Blob([scriptText], { type: 'text/plain;charset=utf-8' });
        element.href = URL.createObjectURL(file);
        element.download = `Episode_${episodeNumber}_Script.txt`;
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

    return (
        <div className="episode-viewer-container" style={styles.container}>
            <h2>Generated Episodes</h2>
            <div style={styles.episodesList}>
                {episodes.map((episode) => {
                    const isOpen = openScripts[episode.episode_number] || false;
                    const hasScript = Boolean(episode.script);

                    return (
                        <div key={episode.episode_number} style={styles.episodeCard}>
                            <div style={styles.headerRow}>
                                <h3 style={styles.episodeTitle}>Episode {episode.episode_number}</h3>
                                {hasScript && (
                                    <div style={styles.actionButtons}>
                                        <button 
                                            onClick={() => toggleScript(episode.episode_number)}
                                            style={styles.toggleBtn}
                                        >
                                            {isOpen ? 'Hide Preview' : 'Show Preview'}
                                        </button>
                                        <button 
                                            onClick={() => handleDownload(episode.episode_number, episode.script)}
                                            style={styles.downloadBtn}
                                        >
                                            Download
                                        </button>
                                    </div>
                                )}
                            </div>

                            {isOpen && hasScript && (
                                <div style={styles.scriptContainer}>
                                    <pre style={styles.scriptText}>
                                        {episode.script}
                                    </pre>
                                </div>
                            )}
                            
                            {!hasScript && (
                                <p style={{color: '#888'}}>No script generated for this episode.</p>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

const styles = {
    container: {
        maxWidth: '800px',
        margin: '30px auto',
        width: '100%',
        textAlign: 'left',
    },
    episodesList: {
        display: 'flex',
        flexDirection: 'column',
        gap: '20px'
    },
    episodeCard: {
        backgroundColor: '#1e1e1e',
        border: '1px solid #333',
        borderRadius: '8px',
        padding: '20px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)'
    },
    headerRow: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderBottom: '1px solid #333',
        paddingBottom: '15px',
        marginBottom: '15px'
    },
    episodeTitle: {
        margin: '0',
        color: '#4af626'
    },
    actionButtons: {
        display: 'flex',
        gap: '10px'
    },
    toggleBtn: {
        backgroundColor: '#333',
        color: '#fff',
        border: '1px solid #555',
        padding: '6px 14px',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '13px',
        fontFamily: 'monospace'
    },
    downloadBtn: {
        backgroundColor: '#007bff',
        color: '#fff',
        border: 'none',
        padding: '6px 14px',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '13px',
        fontFamily: 'monospace'
    },
    scriptContainer: {
        backgroundColor: '#111',
        padding: '20px',
        borderRadius: '6px',
        borderLeft: '4px solid #4af626',
        maxHeight: '600px',
        overflowY: 'auto'
    },
    scriptText: {
        margin: 0,
        color: '#f8f8f2',
        fontFamily: '"Courier New", Courier, monospace',
        fontSize: '15px',
        lineHeight: '1.6',
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-word'
    }
};

export default EpisodeViewer;

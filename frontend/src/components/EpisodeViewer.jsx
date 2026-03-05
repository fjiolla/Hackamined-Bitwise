import React from 'react';

const EpisodeViewer = ({ episodes }) => {
    if (!episodes || episodes.length === 0) {
        return null;
    }

    return (
        <div className="episode-viewer-container" style={styles.container}>
            <h2>Generated Episodes</h2>
            <div style={styles.episodesList}>
                {episodes.map((episode) => (
                    <div key={episode.episode_number} style={styles.episodeCard}>
                        <h3 style={styles.episodeTitle}>Episode {episode.episode_number}</h3>

                        <div style={styles.beatsList}>
                            {episode.beats && episode.beats.map((beat, index) => (
                                <div key={index} style={styles.beatItem}>
                                    <div style={styles.beatHeader}>
                                        <span style={styles.beatType}>
                                            {beat.beat_type.charAt(0).toUpperCase() + beat.beat_type.slice(1)}
                                        </span>
                                        <span style={styles.timeRange}>({beat.time_range})</span>
                                    </div>
                                    <p style={styles.beatContent}>{beat.content}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
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
    episodeTitle: {
        margin: '0 0 15px 0',
        color: '#4af626',
        borderBottom: '1px solid #333',
        paddingBottom: '10px'
    },
    beatsList: {
        display: 'flex',
        flexDirection: 'column',
        gap: '12px'
    },
    beatItem: {
        backgroundColor: '#252525',
        padding: '12px',
        borderRadius: '6px',
        borderLeft: '4px solid #007bff'
    },
    beatHeader: {
        display: 'flex',
        gap: '10px',
        alignItems: 'baseline',
        marginBottom: '8px'
    },
    beatType: {
        fontWeight: 'bold',
        color: '#ddd',
        fontSize: '15px'
    },
    timeRange: {
        color: '#888',
        fontSize: '13px'
    },
    beatContent: {
        margin: 0,
        color: '#ccc',
        lineHeight: '1.5',
        fontSize: '14px'
    }
};

export default EpisodeViewer;

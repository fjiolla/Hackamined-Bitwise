import React, { useState } from 'react';
import EmotionalChart from './EmotionalChart';
import RetentionChart from './RetentionChart';
import SuggestionsPanel from './SuggestionsPanel';

const EpisodeViewer = ({ episode, allEpisodes = [], seriesBible, onRegenerateSuccess }) => {
    const [activeTab, setActiveTab] = useState('screenplay');

    if (!episode) return null;

    const handleInternalRegenerateSuccess = (updatedEpisode) => {
        if (onRegenerateSuccess) {
            onRegenerateSuccess(updatedEpisode);
        }
        setActiveTab('analysis');
    };

    const handleDownload = () => {
        if (!episode.script) return;
        const element = document.createElement("a");
        const file = new Blob([episode.script], { type: 'text/plain;charset=utf-8' });
        element.href = URL.createObjectURL(file);
        element.download = `Episode_${episode.episode_number}_Script.txt`;
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

    const renderScreenplayTab = () => (
        <div className="fade-in">
            <div style={styles.tabHeader}>
                <h2 style={styles.episodeTitle}>Episode {episode.episode_number}</h2>
                <button onClick={handleDownload} style={styles.downloadBtn} disabled={!episode.script}>
                    Download Script
                </button>
            </div>
            
            <div style={styles.scriptContainer}>
                {episode.script ? (
                    <pre style={styles.scriptText}>{episode.script}</pre>
                ) : (
                    <div style={styles.emptyState}>No script generated for this episode yet.</div>
                )}
            </div>
        </div>
    );

    const renderAnalysisTab = () => {
        const cScore = episode.cliffhanger_score;
        const breakdown = cScore?.breakdown || {};
        
        return (
            <div className="fade-in" style={styles.analysisContainer}>
                <h2 style={styles.episodeTitle}>Episode {episode.episode_number} Analysis</h2>
                
                <div style={styles.chartsRow}>
                    <div style={styles.chartCard}>
                        <h3 style={styles.cardTitle}>Emotional Arc</h3>
                        <EmotionalChart analysis={episode.emotional_analysis} />
                    </div>
                    <div style={styles.chartCard}>
                        <h3 style={styles.cardTitle}>Retention Risk</h3>
                        <RetentionChart riskData={episode.retention_risk} />
                    </div>
                </div>

                {cScore && (
                    <div style={styles.cliffhangerCard}>
                        <div style={styles.cliffTop}>
                            <div>
                                <h3 style={styles.cardTitle}>Cliffhanger Impact</h3>
                                <p style={styles.cliffExplanation}>{cScore.explanation}</p>
                            </div>
                            <div style={styles.cliffScoreValue}>
                                {cScore.score}<span style={styles.cliffScoreMax}>/10</span>
                            </div>
                        </div>

                        <div style={styles.barsGrid}>
                            {['unresolved_tension', 'stakes_escalation', 'character_jeopardy', 'revelation_hook', 'time_pressure'].map(dim => (
                                <div key={dim} style={styles.barContainer}>
                                    <div style={styles.barLabelGroup}>
                                        <span style={styles.barLabel}>{dim.replace('_', ' ').toUpperCase()}</span>
                                        <span style={styles.barValue}>{breakdown[dim] || 0}/2</span>
                                    </div>
                                    <div style={styles.barWrap}>
                                        <div style={{
                                            ...styles.barFill, 
                                            width: `${((breakdown[dim] || 0) / 2) * 100}%`
                                        }}></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        );
    };

    const renderSuggestionsTab = () => (
        <div className="fade-in">
            <h2 style={styles.episodeTitle}>Episode {episode.episode_number} Optimization</h2>
            <div style={styles.cardSpacing}>
                <SuggestionsPanel 
                    suggestions={episode.suggestions}
                    episodeNum={episode.episode_number}
                    seriesBible={seriesBible}
                    isLastEpisode={episode.is_last_episode}
                    episodesList={allEpisodes}
                    onRegenerateSuccess={handleInternalRegenerateSuccess}
                />
            </div>
        </div>
    );

    return (
        <div style={styles.container}>
            <div className="tab-navigation">
                <button 
                    className={`tab-btn ${activeTab === 'screenplay' ? 'active' : ''}`}
                    onClick={() => setActiveTab('screenplay')}
                >
                    Screenplay
                </button>
                <button 
                    className={`tab-btn ${activeTab === 'analysis' ? 'active' : ''}`}
                    onClick={() => setActiveTab('analysis')}
                >
                    Analysis
                </button>
                <button 
                    className={`tab-btn ${activeTab === 'suggestions' ? 'active' : ''}`}
                    onClick={() => setActiveTab('suggestions')}
                >
                    Suggestions
                </button>
            </div>

            <div style={styles.tabContent}>
                {activeTab === 'screenplay' && renderScreenplayTab()}
                {activeTab === 'analysis' && renderAnalysisTab()}
                {activeTab === 'suggestions' && renderSuggestionsTab()}
            </div>
        </div>
    );
};

const styles = {
    container: {
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        height: '100%'
    },
    tabContent: {
        flex: 1,
        paddingTop: '16px'
    },
    tabHeader: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '24px'
    },
    episodeTitle: {
        margin: 0,
        fontSize: '28px',
        fontWeight: '700',
        letterSpacing: '-0.5px'
    },
    downloadBtn: {
        padding: '10px 20px',
        fontSize: '14px'
    },
    scriptContainer: {
        backgroundColor: 'var(--card-bg)',
        padding: '40px',
        borderRadius: 'var(--border-radius)',
        border: '1px solid var(--border-color)',
        boxShadow: 'var(--box-shadow)',
        minHeight: '400px'
    },
    scriptText: {
        color: 'var(--text-primary)',
        fontFamily: '"Courier New", Courier, monospace',
        fontSize: '15px',
        lineHeight: '1.6',
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-word',
        maxWidth: '850px',
        margin: '0 auto' // Center screenplay text
    },
    emptyState: {
        color: 'var(--text-secondary)',
        textAlign: 'center',
        padding: '60px 0',
        fontStyle: 'italic'
    },
    analysisContainer: {
        display: 'flex',
        flexDirection: 'column',
        gap: '24px'
    },
    chartsRow: {
        display: 'flex',
        gap: '24px',
        marginTop: '24px'
    },
    chartCard: {
        flex: 1,
        backgroundColor: 'var(--card-bg)',
        padding: '24px',
        borderRadius: 'var(--border-radius)',
        border: '1px solid var(--border-color)',
        boxShadow: 'var(--box-shadow)'
    },
    cardTitle: {
        margin: '0 0 16px 0',
        fontSize: '18px',
        fontWeight: '600'
    },
    cliffhangerCard: {
        backgroundColor: 'var(--card-bg)',
        padding: '32px',
        borderRadius: 'var(--border-radius)',
        border: '1px solid var(--border-color)',
        boxShadow: 'var(--box-shadow)'
    },
    cliffTop: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        borderBottom: '1px solid var(--border-color)',
        paddingBottom: '20px',
        marginBottom: '24px'
    },
    cliffExplanation: {
        color: 'var(--text-secondary)',
        margin: '8px 0 0 0',
        fontSize: '15px',
        lineHeight: '1.5',
        maxWidth: '600px'
    },
    cliffScoreValue: {
        fontSize: '48px',
        fontWeight: '800',
        color: 'var(--accent-color)',
        lineHeight: '1'
    },
    cliffScoreMax: {
        fontSize: '20px',
        color: 'var(--text-secondary)',
        fontWeight: '500'
    },
    barsGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: '24px'
    },
    barContainer: {
        display: 'flex',
        flexDirection: 'column',
        gap: '8px'
    },
    barLabelGroup: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    barLabel: {
        fontSize: '12px',
        fontWeight: '600',
        color: 'var(--text-secondary)',
        letterSpacing: '0.5px'
    },
    barValue: {
        fontSize: '13px',
        fontWeight: 'bold',
        color: 'var(--text-primary)'
    },
    barWrap: {
        width: '100%',
        height: '8px',
        backgroundColor: 'var(--bg-color)',
        borderRadius: '4px',
        overflow: 'hidden',
        border: '1px solid var(--border-color)'
    },
    barFill: {
        height: '100%',
        backgroundColor: 'var(--accent-color)',
        borderRadius: '4px'
    },
    cardSpacing: {
        marginTop: '24px'
    }
};

export default EpisodeViewer;

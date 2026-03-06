import React, { useState } from 'react';
import './App.css';
import StoryInput from './components/StoryInput';
import EpisodeViewer from './components/EpisodeViewer';
import ContinuityLedgerModal from './components/ContinuityLedgerModal';

function App() {
  const [result, setResult] = useState(null);
  const [activeEpisodeNum, setActiveEpisodeNum] = useState(null);

  const handleGenerationResult = (data) => {
    setResult(data);
    // Auto-select the first episode when data comes in
    if (data.episodes && data.episodes.length > 0) {
        setActiveEpisodeNum(data.episodes[0].episode_number);
    }
  };

  const handleRegenerateSuccess = (updatedEpisode) => {
    setResult(prevResult => {
        const newEpisodes = prevResult.episodes.map(ep => 
            ep.episode_number === updatedEpisode.episode_number ? updatedEpisode : ep
        );
        return {
            ...prevResult,
            episodes: newEpisodes
        };
    });
  };

  const getRiskColor = (ep) => {
    // Determine overall risk color dot based on the highest risk in the episode
    const risks = ep.retention_risk || [];
    const hasHigh = risks.some(r => r.risk_level === 'HIGH');
    const hasMed = risks.some(r => r.risk_level === 'MEDIUM');
    if (hasHigh) return '#ff4444'; // Red
    if (hasMed) return '#ffaa00'; // Yellow
    return '#00ff88'; // Green
  };

  if (!result) {
    return (
      <div className="app-container">
        <StoryInput onGenerateFullResult={handleGenerationResult} />
      </div>
    );
  }

  const { series_bible, series_arc_score, episodes } = result;
  
  const safeEpisodes = episodes || [];

  const activeEpisodeData = safeEpisodes.find(e => e.episode_number === activeEpisodeNum);

  return (
    <div className="app-container dashboard-layout">
      {/* LEFT SIDEBAR */}
      <aside className="sidebar">
        <div style={styles.sidebarHeader}>
            <h2 style={styles.sidebarLogo}>Episode<span style={{color: 'var(--accent-color)'}}>IQ</span></h2>
            <div style={styles.seriesTitle}>{series_bible?.title || "Generated Series"}</div>
        </div>

        {/* Series Arc Score Card */}
        {series_arc_score && (
            <div style={styles.arcCard}>
                <div style={styles.arcTop}>
                    <div>
                        <div style={styles.arcLabel}>SERIES ARC SCORE</div>
                        <div style={styles.arcScore}>
                            {series_arc_score.series_arc_score}<span style={styles.arcMax}>/100</span>
                        </div>
                    </div>
                    <div style={styles.arcGrade}>{series_arc_score.grade}</div>
                </div>
                
                <p style={styles.arcVerdict}>{series_arc_score.verdict}</p>

                <div style={styles.arcBarContainer}>
                    <div style={styles.arcBarRow}>
                        <span>Cliffhangers</span>
                        <div style={styles.barWrap}>
                            <div style={{...styles.barFill, width: `${(series_arc_score.breakdown.cliffhanger_strength / 40) * 100}%`}}></div>
                        </div>
                    </div>
                    <div style={styles.arcBarRow}>
                        <span>Emotion</span>
                        <div style={styles.barWrap}>
                            <div style={{...styles.barFill, width: `${(series_arc_score.breakdown.emotional_variance / 35) * 100}%`}}></div>
                        </div>
                    </div>
                    <div style={styles.arcBarRow}>
                        <span>Retention</span>
                        <div style={styles.barWrap}>
                            <div style={{...styles.barFill, width: `${(series_arc_score.breakdown.retention_health / 25) * 100}%`}}></div>
                        </div>
                    </div>
                </div>
            </div>
        )}

        {/* Episode Selectors */}
        <div style={styles.navSection}>
            <div style={styles.navLabel}>EPISODES</div>
            <div style={styles.navList}>
                {safeEpisodes.map(ep => {
                    const isActive = ep.episode_number === activeEpisodeNum;
                    return (
                        <button
                            key={ep.episode_number}
                            onClick={() => setActiveEpisodeNum(ep.episode_number)}
                            style={{
                                ...styles.navButton,
                                backgroundColor: isActive ? 'rgba(0, 255, 136, 0.1)' : 'transparent',
                                borderLeft: isActive ? '3px solid var(--accent-color)' : '3px solid transparent'
                            }}
                        >
                            <span style={{ 
                                ...styles.statusDot, 
                                backgroundColor: getRiskColor(ep) 
                            }}></span>
                            Episode {ep.episode_number}
                        </button>
                    );
                })}
            </div>
        </div>

      </aside>

      {/* MAIN CONTENT AREA */}
      <main className="main-content">
          {activeEpisodeData && (
              <EpisodeViewer 
                  episode={activeEpisodeData} 
                  seriesBible={series_bible}
                  onRegenerateSuccess={handleRegenerateSuccess}
              />
          )}
      </main>

      {series_bible?.continuity_ledger && (
          <ContinuityLedgerModal ledger={series_bible.continuity_ledger} />
      )}

    </div>
  );
}

const styles = {
    sidebarHeader: {
        borderBottom: '1px solid var(--border-color)',
        paddingBottom: '20px'
    },
    sidebarLogo: {
        fontSize: '24px',
        margin: '0 0 16px 0',
        letterSpacing: '-0.5px'
    },
    seriesTitle: {
        fontSize: '18px',
        fontWeight: '600',
        color: 'var(--text-primary)',
        lineHeight: '1.3'
    },
    arcCard: {
        backgroundColor: 'var(--bg-color)',
        padding: '20px',
        borderRadius: '8px',
        border: '1px solid var(--border-color)',
    },
    arcTop: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: '12px'
    },
    arcLabel: {
        fontSize: '11px',
        fontWeight: 'bold',
        color: 'var(--text-secondary)',
        letterSpacing: '1px',
        marginBottom: '4px'
    },
    arcScore: {
        fontSize: '32px',
        fontWeight: '800',
        lineHeight: '1'
    },
    arcMax: {
        fontSize: '16px',
        color: 'var(--text-secondary)',
        fontWeight: '500'
    },
    arcGrade: {
        fontSize: '36px',
        fontWeight: '900',
        color: 'var(--accent-color)',
        lineHeight: '1'
    },
    arcVerdict: {
        fontSize: '13px',
        color: 'var(--text-secondary)',
        margin: '0 0 16px 0',
        lineHeight: '1.4'
    },
    arcBarContainer: {
        display: 'flex',
        flexDirection: 'column',
        gap: '8px'
    },
    arcBarRow: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontSize: '12px',
        color: 'var(--text-secondary)'
    },
    barWrap: {
        width: '80px',
        height: '6px',
        backgroundColor: 'var(--card-bg)',
        borderRadius: '3px',
        overflow: 'hidden'
    },
    barFill: {
        height: '100%',
        backgroundColor: 'var(--accent-color)'
    },
    navSection: {
        marginTop: '8px',
        flex: 1
    },
    navLabel: {
        fontSize: '11px',
        fontWeight: 'bold',
        color: 'var(--text-secondary)',
        letterSpacing: '1px',
        marginBottom: '12px'
    },
    navList: {
        display: 'flex',
        flexDirection: 'column',
        gap: '4px'
    },
    navButton: {
        display: 'flex',
        alignItems: 'center',
        width: '100%',
        textAlign: 'left',
        padding: '12px 16px',
        border: 'none',
        borderLeft: '3px solid transparent', // reserve space
        borderRadius: '0 6px 6px 0',
        color: 'var(--text-primary)',
        fontSize: '15px',
        fontWeight: '500',
        cursor: 'pointer',
        transition: 'all 0.2s',
        gap: '12px'
    },
    statusDot: {
        width: '8px',
        height: '8px',
        borderRadius: '50%',
        display: 'inline-block'
    }
};

export default App;

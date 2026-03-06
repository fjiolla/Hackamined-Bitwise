import React, { useState } from 'react';
import { regenerateEpisode } from '../api';

const SuggestionsPanel = ({ suggestions, episodeNum, seriesBible, isLastEpisode, episodesList = [], onRegenerateSuccess }) => {
    const [isRegenerating, setIsRegenerating] = useState(false);

    if (!suggestions || suggestions.length === 0) {
        return (
            <div style={styles.emptyStateContainer} className="fade-in">
                <div style={styles.emptyState}>No narrative optimizations needed. Great job!</div>
            </div>
        );
    }

    const formatIssueType = (type) => {
        return type
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    };

    const handleRegenerate = async () => {
    setIsRegenerating(true);
    try {
        const suggestionTexts = suggestions.map(s => s.suggestion);

        const sortedEpisodes = [...episodesList].sort((a, b) => a.episode_number - b.episode_number);

        let priorContext = "";
        for (const ep of sortedEpisodes) {
            if (ep.episode_number >= episodeNum) break;
            const cliffhanger = ep.beats?.at(-1)?.content || "";
            const beatSummary = ep.beats?.map(b => `${b.beat_type}: ${b.content}`).join(" | ") || "";
            priorContext += `Episode ${ep.episode_number} full summary: ${beatSummary}\nEpisode ${ep.episode_number} ended on this cliffhanger: ${cliffhanger}\n\n`;
        }

        const nextEp = sortedEpisodes.find(e => e.episode_number === episodeNum + 1);
        const nextHook = nextEp?.beats?.find(b => b.beat_type.toLowerCase() === 'hook')?.content || "";

        const payload = {
            episode_number: episodeNum,
            series_bible: seriesBible,
            suggestions: suggestionTexts,
            is_last_episode: isLastEpisode || false,
            prior_context: priorContext,
            next_episode_hook: nextHook
        };
            
            const updatedEpisode = await regenerateEpisode(payload);
            if (onRegenerateSuccess) {
                onRegenerateSuccess(updatedEpisode);
            }
        } catch (error) {
            console.error("Failed to regenerate episode:", error);
            alert("Failed to regenerate episode. Check console for details.");
        } finally {
            setIsRegenerating(false);
        }
    };

    return (
        <div>
            <div style={styles.gridContainer}>
                {suggestions.map((item, index) => (
                    <div key={index} style={styles.suggestionCard} className="fade-in">
                        <div style={styles.issueType}>{formatIssueType(item.issue_type)}</div>
                        <p style={styles.suggestionText}>{item.suggestion}</p>
                    </div>
                ))}
            </div>
            
            <button
                onClick={handleRegenerate}
                disabled={isRegenerating}
                style={{
                    marginTop: '24px',
                    padding: '12px 24px',
                    background: '#00ff88',
                    color: '#000',
                    border: 'none',
                    borderRadius: '8px',
                    fontWeight: 'bold',
                    cursor: isRegenerating ? 'not-allowed' : 'pointer',
                    width: '100%',
                    opacity: isRegenerating ? 0.7 : 1
                }}
            >
                {isRegenerating ? 'Regenerating Episode...' : '⚡ Regenerate Episode with Fixes'}
            </button>
        </div>
    );
};

const styles = {
    emptyStateContainer: {
        backgroundColor: 'var(--card-bg)',
        padding: '40px',
        borderRadius: 'var(--border-radius)',
        border: '1px solid var(--border-color)',
        boxShadow: 'var(--box-shadow)',
        textAlign: 'center'
    },
    emptyState: {
        color: 'var(--accent-color)',
        fontStyle: 'italic',
        fontSize: '16px'
    },
    gridContainer: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
        gap: '24px'
    },
    suggestionCard: {
        backgroundColor: 'var(--card-bg)',
        borderLeft: '4px solid #ffaa00',
        padding: '24px',
        borderRadius: 'var(--border-radius)',
        boxShadow: 'var(--box-shadow)',
        display: 'flex',
        flexDirection: 'column',
        gap: '12px'
    },
    issueType: {
        fontWeight: '700',
        color: '#ffaa00',
        fontSize: '18px',
        letterSpacing: '-0.3px',
        margin: 0
    },
    suggestionText: {
        margin: 0,
        color: 'var(--text-secondary)',
        lineHeight: '1.6',
        fontSize: '15px'
    }
};

export default SuggestionsPanel;

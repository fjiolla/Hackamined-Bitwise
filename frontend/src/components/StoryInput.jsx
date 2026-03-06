import React, { useState, useEffect } from 'react';
import { generateSeries } from '../api';

const LOADING_STEPS = [
    "Generating Series Bible...",
    "Generating Episodes...",
    "Analysing Emotional Arc...",
    "Scoring Cliffhangers...",
    "Predicting Retention Risk...",
    "Writing Screenplays..."
];

const StoryInput = ({ onGenerateFullResult }) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [genre, setGenre] = useState('Drama');
    const [episodeCount, setEpisodeCount] = useState(5);
    
    const [isGenerating, setIsGenerating] = useState(false);
    const [loadingStepIndex, setLoadingStepIndex] = useState(-1);
    const [error, setError] = useState('');

    // Timer effect for sequential loading text visualization
    useEffect(() => {
        let interval;
        if (isGenerating && loadingStepIndex < LOADING_STEPS.length - 1) {
            interval = setInterval(() => {
                setLoadingStepIndex(prev => prev + 1);
            }, 3000);
        }
        return () => clearInterval(interval);
    }, [isGenerating, loadingStepIndex]);

    const handleGenerate = async (e) => {
        e.preventDefault();
        setIsGenerating(true);
        setLoadingStepIndex(0);
        setError('');

        try {
            const result = await generateSeries({
                title,
                description,
                genre,
                episode_count: parseInt(episodeCount, 10)
            });
            onGenerateFullResult(result);
        } catch (err) {
            setError('Failed to generate series. Please check the backend connection.');
            setIsGenerating(false);
        }
    };

    if (isGenerating) {
        return (
            <div className="landing-page">
                <div style={styles.loadingContainer} className="fade-in">
                    <h2 style={styles.loadingTitle}>Forging your Series</h2>
                    <div style={styles.stepsList}>
                        {LOADING_STEPS.map((step, index) => {
                            const isPast = index < loadingStepIndex;
                            const isActive = index === loadingStepIndex;
                            const isFuture = index > loadingStepIndex;
                            
                            return (
                                <div 
                                    key={index}
                                    style={{
                                        ...styles.loadingStep,
                                        opacity: isFuture ? 0.3 : 1,
                                        color: isPast ? 'var(--accent-color)' : 'var(--text-primary)'
                                    }}
                                >
                                    <span style={{ width: '24px', display: 'inline-block' }}>
                                        {isPast ? '✓' : isActive ? '⏳' : '○'}
                                    </span>
                                    <span>{step}</span>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="landing-page fade-in">
            <div style={styles.header}>
                <h1 style={styles.logo}>Episode<span style={{ color: 'var(--accent-color)' }}>IQ</span></h1>
                <p style={styles.tagline}>Turn any idea into a complete short-form series</p>
            </div>

            <div style={styles.cardContainer}>
                <form onSubmit={handleGenerate} style={styles.form}>
                    <div style={styles.formGroup}>
                        <label style={styles.label}>Story Title</label>
                        <input
                            type="text"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                            style={styles.input}
                            placeholder="E.g. The Truth Frequency"
                        />
                    </div>

                    <div style={styles.rowGroup}>
                        <div style={{...styles.formGroup, flex: 2}}>
                            <label style={styles.label}>Genre</label>
                            <select 
                                value={genre} 
                                onChange={(e) => setGenre(e.target.value)}
                                style={styles.select}
                            >
                                <option value="Drama">Drama</option>
                                <option value="Thriller">Thriller</option>
                                <option value="Romance">Romance</option>
                                <option value="Horror">Horror</option>
                                <option value="Comedy">Comedy</option>
                                <option value="Sci-Fi">Sci-Fi</option>
                            </select>
                        </div>

                        <div style={{...styles.formGroup, flex: 1}}>
                            <label style={styles.label}>Episode Count</label>
                            <select 
                                value={episodeCount} 
                                onChange={(e) => setEpisodeCount(e.target.value)}
                                style={styles.select}
                            >
                                <option value="5">5</option>
                                <option value="6">6</option>
                                <option value="7">7</option>
                                <option value="8">8</option>
                            </select>
                        </div>
                    </div>

                    <div style={styles.formGroup}>
                        <label style={styles.label}>Description</label>
                        <textarea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            required
                            style={styles.textarea}
                            placeholder="A girl discovers she can hear people's lies..."
                            rows="3"
                        />
                    </div>

                    {error && <div style={styles.error}>{error}</div>}

                    <button type="submit" style={styles.submitBtn}>
                        Generate Series
                    </button>
                </form>
            </div>
        </div>
    );
};

const styles = {
    header: {
        textAlign: 'center',
        marginBottom: '40px'
    },
    logo: {
        fontSize: '48px',
        fontWeight: '900',
        letterSpacing: '-1px',
        margin: '0 0 8px 0'
    },
    tagline: {
        fontSize: '18px',
        color: 'var(--text-secondary)',
        margin: 0
    },
    cardContainer: {
        backgroundColor: 'var(--card-bg)',
        padding: '40px',
        borderRadius: 'var(--border-radius)',
        border: '1px solid var(--border-color)',
        boxShadow: 'var(--box-shadow)',
        width: '100%',
        maxWidth: '600px'
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
        gap: '24px'
    },
    rowGroup: {
        display: 'flex',
        gap: '20px'
    },
    formGroup: {
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
        textAlign: 'left'
    },
    label: {
        fontWeight: '600',
        fontSize: '14px',
        color: 'var(--text-secondary)'
    },
    input: {
        padding: '12px 16px',
        borderRadius: '8px',
        border: '1px solid var(--border-color)',
        background: 'var(--bg-color)',
        color: 'var(--text-primary)',
        fontSize: '16px',
        fontFamily: 'var(--font-family)',
        outline: 'none',
        transition: 'border-color 0.2s'
    },
    select: {
        padding: '12px 16px',
        borderRadius: '8px',
        border: '1px solid var(--border-color)',
        background: 'var(--bg-color)',
        color: 'var(--text-primary)',
        fontSize: '16px',
        fontFamily: 'var(--font-family)',
        cursor: 'pointer',
        outline: 'none'
    },
    textarea: {
        padding: '12px 16px',
        borderRadius: '8px',
        border: '1px solid var(--border-color)',
        background: 'var(--bg-color)',
        color: 'var(--text-primary)',
        fontSize: '16px',
        fontFamily: 'var(--font-family)',
        resize: 'vertical',
        outline: 'none'
    },
    submitBtn: {
        marginTop: '16px',
        padding: '16px',
        fontSize: '18px',
        width: '100%'
    },
    error: {
        color: '#ff4444',
        fontSize: '14px',
        backgroundColor: 'rgba(255, 68, 68, 0.1)',
        padding: '12px',
        borderRadius: '6px',
        border: '1px solid rgba(255, 68, 68, 0.2)'
    },
    loadingContainer: {
        backgroundColor: 'var(--card-bg)',
        padding: '40px',
        borderRadius: 'var(--border-radius)',
        border: '1px solid var(--border-color)',
        minWidth: '400px',
        boxShadow: 'var(--box-shadow)'
    },
    loadingTitle: {
        textAlign: 'center',
        color: 'var(--accent-color)',
        marginBottom: '24px'
    },
    stepsList: {
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
    },
    loadingStep: {
        display: 'flex',
        alignItems: 'center',
        fontSize: '16px',
        fontWeight: '500',
        transition: 'all 0.5s ease'
    }
};

export default StoryInput;

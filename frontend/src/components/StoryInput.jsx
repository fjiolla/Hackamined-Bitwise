import React, { useState } from 'react';
import { generateSeries, suggestEpisodes } from '../api';

const StoryInput = ({ onGenerateFullResult }) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [genre, setGenre] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [step, setStep] = useState(1);
    const [episodeCount, setEpisodeCount] = useState(5);
    const [suggestionMessage, setSuggestionMessage] = useState('');

    const handleAnalyse = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const result = await suggestEpisodes({
                title,
                description,
                genre
            });
            const count = result.suggested_count || 5;
            setEpisodeCount(count);
            setSuggestionMessage(`We recommend ${count} episodes for this story.`);
            setStep(2);
        } catch (err) {
            setError('Failed to analyse story. Please check the backend connection.');
        } finally {
            setLoading(false);
        }
    };

    const handleGenerate = async (e) => {
        e.preventDefault();
        setLoading(true);
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
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="story-input-container" style={styles.container}>
            <h2>Generate EpisodeIQ Series</h2>
            <form onSubmit={step === 1 ? handleAnalyse : handleGenerate} style={styles.form}>
                <div style={styles.formGroup}>
                    <label style={styles.label}>Title</label>
                    <input
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                        disabled={step === 2}
                        style={styles.input}
                        placeholder="E.g. The Truth Frequency"
                    />
                </div>

                <div style={styles.formGroup}>
                    <label style={styles.label}>Genre</label>
                    <input
                        type="text"
                        value={genre}
                        onChange={(e) => setGenre(e.target.value)}
                        required
                        disabled={step === 2}
                        style={styles.input}
                        placeholder="E.g. Mystery"
                    />
                </div>

                <div style={styles.formGroup}>
                    <label style={styles.label}>Story Idea</label>
                    <textarea
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        required
                        disabled={step === 2}
                        style={styles.textarea}
                        placeholder="A girl discovers she can hear people's lies..."
                        rows="4"
                    />
                </div>

                {step === 2 && (
                    <div style={styles.suggestionBox}>
                        <p style={styles.suggestionText}>{suggestionMessage}</p>
                        <div style={styles.formGroup}>
                            <label style={styles.label}>Confirmed Episode Count (5-8)</label>
                            <select 
                                value={episodeCount} 
                                onChange={(e) => setEpisodeCount(e.target.value)}
                                style={styles.input}
                            >
                                <option value="5">5 Episodes</option>
                                <option value="6">6 Episodes</option>
                                <option value="7">7 Episodes</option>
                                <option value="8">8 Episodes</option>
                            </select>
                        </div>
                    </div>
                )}

                {error && <div style={styles.error}>{error}</div>}

                {step === 1 ? (
                    <button type="submit" disabled={loading} style={styles.button}>
                        {loading ? 'Analysing...' : 'Analyse Story'}
                    </button>
                ) : (
                    <button type="submit" disabled={loading} style={{...styles.button, backgroundColor: '#28a745'}}>
                        {loading ? 'Generating...' : 'Generate Series'}
                    </button>
                )}
            </form>
        </div>
    );
};

const styles = {
    container: {
        maxWidth: '600px',
        margin: '0 auto',
        padding: '20px',
        backgroundColor: '#1e1e1e',
        borderRadius: '8px',
        color: '#fff',
        border: '1px solid #333'
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
        gap: '15px'
    },
    formGroup: {
        display: 'flex',
        flexDirection: 'column',
        textAlign: 'left'
    },
    label: {
        marginBottom: '5px',
        fontWeight: 'bold',
        fontSize: '14px',
        color: '#ddd'
    },
    input: {
        padding: '10px',
        borderRadius: '4px',
        border: '1px solid #444',
        background: '#2d2d2d',
        color: '#fff',
        fontSize: '16px'
    },
    textarea: {
        padding: '10px',
        borderRadius: '4px',
        border: '1px solid #444',
        background: '#2d2d2d',
        color: '#fff',
        fontSize: '16px',
        resize: 'vertical'
    },
    button: {
        padding: '12px 20px',
        backgroundColor: '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        fontSize: '16px',
        cursor: 'pointer',
        fontWeight: 'bold',
        marginTop: '10px'
    },
    error: {
        color: '#ff6b6b',
        fontSize: '14px',
        marginTop: '-5px'
    },
    suggestionBox: {
        backgroundColor: '#2a2a2a',
        padding: '15px',
        borderRadius: '6px',
        borderLeft: '4px solid #f39c12',
        marginTop: '10px',
        marginBottom: '10px'
    },
    suggestionText: {
        margin: '0 0 10px 0',
        color: '#f1c40f',
        fontWeight: 'bold'
    }
};

export default StoryInput;

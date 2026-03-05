import React, { useState } from 'react';
import { generateSeries } from '../api';

const StoryInput = ({ onGenerateFullResult }) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [genre, setGenre] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const result = await generateSeries({
                title,
                description,
                genre
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
            <form onSubmit={handleSubmit} style={styles.form}>
                <div style={styles.formGroup}>
                    <label style={styles.label}>Title</label>
                    <input
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
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
                        style={styles.textarea}
                        placeholder="A girl discovers she can hear people's lies..."
                        rows="4"
                    />
                </div>

                {error && <div style={styles.error}>{error}</div>}

                <button type="submit" disabled={loading} style={styles.button}>
                    {loading ? 'Generating...' : 'Generate Series'}
                </button>
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
    }
};

export default StoryInput;

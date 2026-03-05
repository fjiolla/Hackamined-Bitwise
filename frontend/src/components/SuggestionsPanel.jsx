import React from 'react';

const SuggestionsPanel = ({ suggestions }) => {
    if (!suggestions || suggestions.length === 0) {
        return (
            <div style={styles.container}>
                <h3 style={styles.title}>Optimization Suggestions</h3>
                <div style={styles.emptyState}>No narrative optimizations needed. Great job!</div>
            </div>
        );
    }

    // Format the issue type to be more readable
    const formatIssueType = (type) => {
        return type
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    };

    return (
        <div style={styles.container}>
            <h3 style={styles.title}>Optimization Suggestions</h3>
            <div style={styles.suggestionsList}>
                {suggestions.map((item, index) => (
                    <div key={index} style={styles.suggestionCard}>
                        <div style={styles.issueType}>{formatIssueType(item.issue_type)}</div>
                        <p style={styles.suggestionText}>{item.suggestion}</p>
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
        backgroundColor: '#1e1e1e',
        padding: '20px',
        borderRadius: '8px',
        border: '1px solid #333'
    },
    title: {
        marginTop: 0,
        marginBottom: '20px',
        color: '#ddd'
    },
    suggestionsList: {
        display: 'flex',
        flexDirection: 'column',
        gap: '15px'
    },
    suggestionCard: {
        backgroundColor: '#252525',
        borderLeft: '4px solid #ff9800', // Orange to indicate a warning/suggestion
        padding: '15px',
        borderRadius: '4px',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)'
    },
    issueType: {
        fontWeight: 'bold',
        color: '#ff9800',
        marginBottom: '8px',
        fontSize: '16px'
    },
    suggestionText: {
        margin: 0,
        color: '#ccc',
        lineHeight: '1.5',
        fontSize: '15px'
    },
    emptyState: {
        color: '#4af626',
        fontStyle: 'italic',
        padding: '10px 0'
    }
};

export default SuggestionsPanel;

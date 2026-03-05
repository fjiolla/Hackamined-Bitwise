import React from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from 'recharts';

const EmotionalChart = ({ analysis }) => {
    if (!analysis || analysis.length === 0) {
        return null;
    }

    // Format data for Recharts
    const chartData = analysis.map((beat) => ({
        name: beat.beat_type.charAt(0).toUpperCase() + beat.beat_type.slice(1),
        score: beat.emotion_score
    }));

    return (
        <div style={styles.container}>
            <h3 style={styles.title}>Episode 1 - Emotional Arc</h3>
            <div style={styles.chartWrapper}>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                        data={chartData}
                        margin={{
                            top: 20,
                            right: 30,
                            left: 0,
                            bottom: 10,
                        }}
                    >
                        <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                        <XAxis dataKey="name" stroke="#ccc" />
                        <YAxis stroke="#ccc" domain={[-1, 1]} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#222', border: '1px solid #444', borderRadius: '4px' }}
                            itemStyle={{ color: '#4af626' }}
                        />
                        <Line
                            type="monotone"
                            dataKey="score"
                            name="Emotion Score"
                            stroke="#4af626"
                            strokeWidth={3}
                            activeDot={{ r: 8 }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

const styles = {
    container: {
        maxWidth: '800px',
        margin: '30px auto',
        width: '100%',
        padding: '20px',
        backgroundColor: '#1e1e1e',
        borderRadius: '8px',
        border: '1px solid #333'
    },
    title: {
        marginTop: 0,
        marginBottom: '20px',
        color: '#ddd',
        textAlign: 'left'
    },
    chartWrapper: {
        width: '100%',
        height: '300px'
    }
};

export default EmotionalChart;

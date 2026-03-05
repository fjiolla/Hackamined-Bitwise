import React from 'react';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Cell
} from 'recharts';

const RetentionChart = ({ riskData }) => {
    if (!riskData || riskData.length === 0) {
        return null;
    }

    // Map risk levels to numbers for chart rendering
    const riskMapping = {
        'LOW': { value: 1, color: '#4af626' },    // Green
        'MEDIUM': { value: 2, color: '#ffc107' }, // Yellow
        'HIGH': { value: 3, color: '#ff6b6b' }    // Red
    };

    // Format data for Recharts
    const chartData = riskData.map((beat) => ({
        name: beat.time_range,
        level: riskMapping[beat.risk_level]?.value || 0,
        color: riskMapping[beat.risk_level]?.color || '#888',
        originalLevel: beat.risk_level
    }));

    // Custom generic tooltip to show text label instead of raw number
    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            const data = payload[0].payload;
            return (
                <div style={styles.tooltip}>
                    <p style={styles.tooltipLabel}>{label}</p>
                    <p style={{ ...styles.tooltipDesc, color: data.color }}>
                        Risk: {data.originalLevel}
                    </p>
                </div>
            );
        }
        return null;
    };

    return (
        <div style={styles.container}>
            <h3 style={styles.title}>Episode 1 - Retention Risk</h3>
            <div style={styles.chartWrapper}>
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                        data={chartData}
                        margin={{
                            top: 20,
                            right: 30,
                            left: 0,
                            bottom: 10,
                        }}
                    >
                        <CartesianGrid strokeDasharray="3 3" stroke="#444" vertical={false} />
                        <XAxis dataKey="name" stroke="#ccc" />
                        <YAxis
                            stroke="#ccc"
                            domain={[0, 3]}
                            ticks={[1, 2, 3]}
                            tickFormatter={(val) => {
                                if (val === 1) return 'LOW';
                                if (val === 2) return 'MED';
                                if (val === 3) return 'HIGH';
                                return '';
                            }}
                        />
                        <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255, 255, 255, 0.05)' }} />
                        <Bar dataKey="level" radius={[4, 4, 0, 0]}>
                            {chartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Bar>
                    </BarChart>
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
    },
    tooltip: {
        backgroundColor: '#222',
        border: '1px solid #444',
        padding: '10px',
        borderRadius: '4px'
    },
    tooltipLabel: {
        color: '#fff',
        margin: '0 0 5px 0',
        fontWeight: 'bold'
    },
    tooltipDesc: {
        margin: 0,
        fontWeight: 'bold'
    }
};

export default RetentionChart;

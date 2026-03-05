import React, { useState } from 'react'
import './App.css'
import StoryInput from './components/StoryInput'
import EpisodeViewer from './components/EpisodeViewer'
import EmotionalChart from './components/EmotionalChart'
import RetentionChart from './components/RetentionChart'
import SuggestionsPanel from './components/SuggestionsPanel'

function App() {
  const [result, setResult] = useState(null)

  const handleGenerationResult = (data) => {
    setResult(data);
  }

  return (
    <div style={styles.app}>
      <header style={styles.header}>
        <h1>EpisodeIQ</h1>
        <p>AI-Powered Episodic Intelligence Engine</p>
      </header>

      <main style={styles.main}>
        <StoryInput onGenerateFullResult={handleGenerationResult} />

        {result && (
          <div style={styles.resultContainer}>
            <EpisodeViewer episodes={result.episodes} />
            {result.episodes && result.episodes.length > 0 && (
              <>
                <EmotionalChart analysis={result.episodes[0].emotional_analysis} />
                <RetentionChart riskData={result.episodes[0].retention_risk} />
                <SuggestionsPanel suggestions={result.episodes[0].suggestions} />
              </>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

const styles = {
  app: {
    fontFamily: 'system-ui, -apple-system, sans-serif',
    textAlign: 'center',
    padding: '20px',
    backgroundColor: '#121212',
    color: '#e0e0e0',
    minHeight: '100vh'
  },
  header: {
    marginBottom: '30px'
  },
  main: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '30px'
  },
  resultContainer: {
    maxWidth: '800px',
    width: '100%',
    textAlign: 'left',
    backgroundColor: '#1e1e1e',
    padding: '20px',
    borderRadius: '8px',
    border: '1px solid #333',
    overflowX: 'auto'
  },
  pre: {
    backgroundColor: '#000',
    padding: '15px',
    borderRadius: '6px',
    color: '#4af626',
    whiteSpace: 'pre-wrap',
    wordWrap: 'break-word',
    fontSize: '13px',
    maxHeight: '500px',
    overflowY: 'auto'
  }
}

export default App

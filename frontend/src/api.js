import axios from 'axios';

// Update the base URL to match the FastAPI routing setup
// The backend mounts the generate router at /api/generate
const API_BASE_URL = 'http://127.0.0.1:8000/api/generate';

export const generateSeries = async (storyData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/generate-series`, storyData);
        return response.data;
    } catch (error) {
        console.error('Error calling generate API:', error);
        throw error;
    }
};

export const suggestEpisodes = async (storyData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/suggest-episodes`, storyData);
        return response.data;
    } catch (error) {
        console.error('Error calling suggest API:', error);
        throw error;
    }
};

export const regenerateEpisode = async (regenerateData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/regenerate-episode`, regenerateData);
        return response.data;
    } catch (error) {
        console.error('Error calling regenerate API:', error);
        throw error;
    }
};

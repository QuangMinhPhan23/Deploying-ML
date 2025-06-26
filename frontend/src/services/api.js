// API service for personality prediction app
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8888';

export const predictPersonality = async (data) => {
  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    return response.json();
  } catch (error) {
    console.error('Error predicting personality:', error);
    throw error;
  }
};

export const submitFeedback = async (predictionId, feedback) => {
  try {
    const response = await fetch(`${API_URL}/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prediction_id: predictionId,
        feedback: feedback
      }),
    });
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    return response.json();
  } catch (error) {
    console.error('Error submitting feedback:', error);
    throw error;
  }
};

export const getHistory = async (limit = 5) => {
  try {
    const response = await fetch(`${API_URL}/history?limit=${limit}`);
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    return response.json();
  } catch (error) {
    console.error('Error fetching history:', error);
    throw error;
  }
};

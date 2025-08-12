import axios from "axios";

const API_BASE_URL = "http://localhost:5000";

// Create axios instance with better error handling
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    if (error.code === 'ECONNREFUSED') {
      console.error('❌ Backend connection refused. Is the Flask API running?');
      throw new Error('Backend service is not running. Please start the backend first.');
    } else if (error.code === 'ENOTFOUND') {
      console.error('❌ Backend service not found');
      throw new Error('Backend service not found. Please check if the API is running on port 5000.');
    } else if (error.response) {
      console.error('❌ API Error Response:', error.response.status, error.response.data);
      throw new Error(error.response.data?.error || `HTTP ${error.response.status}: ${error.response.statusText}`);
    } else if (error.request) {
      console.error('❌ No response received from backend');
      throw new Error('No response from backend. Please check if the API is running.');
    } else {
      console.error('❌ API Error:', error.message);
      throw new Error(error.message);
    }
  }
);

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  
  try {
    const response = await api.post('/api/verify', formData);
    return response;
  } catch (error) {
    // Re-throw the error with better context
    throw error;
  }
};

export const getVerificationHistory = async () => {
  try {
    const response = await api.get('/api/verify/history');
    return response;
  } catch (error) {
    throw error;
  }
};

export const getVerificationById = async (id) => {
  try {
    const response = await api.get(`/api/verify/history/${id}`);
    return response;
  } catch (error) {
    throw error;
  }
};

export const getVerificationStatus = async (fileHash) => {
  try {
    const response = await api.get(`/api/verify/status/${fileHash}`);
    return response;
  } catch (error) {
    throw error;
  }
};

// Health check function
export const checkBackendHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.status === 200;
  } catch (error) {
    return false;
  }
};

// Test connection function
export const testConnection = async () => {
  try {
    const isHealthy = await checkBackendHealth();
    if (isHealthy) {
      console.log('✅ Backend connection successful');
      return true;
    } else {
      console.log('❌ Backend health check failed');
      return false;
    }
  } catch (error) {
    console.error('❌ Backend connection test failed:', error.message);
    return false;
  }
};

import React, { useState } from 'react';
import { uploadDocument, verifyCertificateText, checkApiHealth } from '../services/api';

export default function ApiTest() {
  const [healthStatus, setHealthStatus] = useState(null);
  const [testResult, setTestResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [testText, setTestText] = useState('This is a real estate document with property details and ownership information.');

  const testHealth = async () => {
    try {
      setLoading(true);
      const response = await checkApiHealth();
      setHealthStatus(response.data);
      console.log('Health check response:', response.data);
    } catch (error) {
      console.error('Health check failed:', error);
      setHealthStatus({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  const testTextVerification = async () => {
    try {
      setLoading(true);
      const response = await verifyCertificateText(testText);
      setTestResult(response.data);
      console.log('Text verification response:', response.data);
    } catch (error) {
      console.error('Text verification failed:', error);
      setTestResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  const testFileUpload = async () => {
    try {
      setLoading(true);
      // Create a test file
      const testFile = new File([testText], 'test-document.txt', { type: 'text/plain' });
      const response = await uploadDocument(testFile);
      setTestResult(response.data);
      console.log('File upload response:', response.data);
    } catch (error) {
      console.error('File upload failed:', error);
      setTestResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6">API Connection Test</h2>
      
      {/* Health Check */}
      <div className="mb-6 p-4 border rounded-lg">
        <h3 className="text-lg font-semibold mb-2">Health Check</h3>
        <button
          onClick={testHealth}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
        >
          {loading ? 'Testing...' : 'Test Health'}
        </button>
        {healthStatus && (
          <div className="mt-2 p-2 bg-gray-100 rounded">
            <pre className="text-sm">{JSON.stringify(healthStatus, null, 2)}</pre>
          </div>
        )}
      </div>

      {/* Text Verification Test */}
      <div className="mb-6 p-4 border rounded-lg">
        <h3 className="text-lg font-semibold mb-2">Text Verification Test</h3>
        <textarea
          value={testText}
          onChange={(e) => setTestText(e.target.value)}
          className="w-full p-2 border rounded mb-2"
          rows="3"
          placeholder="Enter certificate text to test..."
        />
        <button
          onClick={testTextVerification}
          disabled={loading}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:bg-gray-400"
        >
          {loading ? 'Testing...' : 'Test Text Verification'}
        </button>
      </div>

      {/* File Upload Test */}
      <div className="mb-6 p-4 border rounded-lg">
        <h3 className="text-lg font-semibold mb-2">File Upload Test</h3>
        <button
          onClick={testFileUpload}
          disabled={loading}
          className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 disabled:bg-gray-400"
        >
          {loading ? 'Testing...' : 'Test File Upload'}
        </button>
      </div>

      {/* Results */}
      {testResult && (
        <div className="p-4 border rounded-lg bg-gray-50">
          <h3 className="text-lg font-semibold mb-2">Test Results</h3>
          <pre className="text-sm overflow-auto">{JSON.stringify(testResult, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

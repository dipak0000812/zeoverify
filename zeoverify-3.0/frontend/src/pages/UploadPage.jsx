import React, { useState, useRef, useEffect } from 'react';
import { uploadDocument, checkBackendHealth } from '../services/api';
import { useVerification } from '../context/VerificationContext';
import { Upload, FileText, Shield, Lock, CheckCircle, AlertCircle, Loader2, X, Wifi, WifiOff } from 'lucide-react';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [backendStatus, setBackendStatus] = useState('checking'); // 'checking', 'connected', 'disconnected'
  const fileInputRef = useRef(null);
  const { addVerificationToHistory } = useVerification();


  // Check backend connection on component mount
  useEffect(() => {
    checkBackendConnection();
    // Check connection every 30 seconds
    const interval = setInterval(checkBackendConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkBackendConnection = async () => {
    try {
      const isHealthy = await checkBackendHealth();
      setBackendStatus(isHealthy ? 'connected' : 'disconnected');
    } catch (error) {
      setBackendStatus('disconnected');
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setResult(null);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    // Check backend connection before uploading
    if (backendStatus !== 'connected') {
      alert("Backend service is not connected. Please check if the API is running on port 5000.");
      return;
    }

    setLoading(true);
    try {
      const response = await uploadDocument(file);
      setResult(response.data);
      console.log("Verification result:", response.data);
      
      // Add verification result to history
      addVerificationToHistory(response.data);
      
    } catch (err) {
      console.error("Error uploading file:", err);
      
      // Show more specific error messages
      let errorMessage = "Error uploading file. Please try again.";
      
      if (err.message.includes('Backend service is not running')) {
        errorMessage = "Backend service is not running. Please start the backend first.";
        setBackendStatus('disconnected');
      } else if (err.message.includes('connection refused')) {
        errorMessage = "Cannot connect to backend. Please check if the API is running on port 5000.";
        setBackendStatus('disconnected');
      } else if (err.message.includes('timeout')) {
        errorMessage = "Request timed out. Please try again.";
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      alert(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop().toLowerCase();
    switch (extension) {
      case 'pdf':
        return <FileText className="w-8 h-8 text-red-500" />;
      case 'jpg':
      case 'jpeg':
      case 'png':
        return <FileText className="w-8 h-8 text-blue-500" />;
      default:
        return <FileText className="w-8 h-8 text-gray-500" />;
    }
  };

  const getFraudRiskColor = (risk) => {
    if (risk === 'Low') return 'text-green-600 bg-green-100';
    if (risk === 'Medium') return 'text-yellow-600 bg-yellow-100';
    if (risk === 'High') return 'text-red-600 bg-red-100';
    return 'text-gray-600 bg-gray-100';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Document Verification
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Upload your real estate documents for AI-powered verification, fraud detection, and blockchain storage.
          </p>
        </div>

        {/* Connection Status */}
        <div className="text-center mb-8">
          <div className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium ${
            backendStatus === 'connected' 
              ? 'bg-green-100 text-green-800' 
              : backendStatus === 'disconnected' 
              ? 'bg-red-100 text-red-800' 
              : 'bg-yellow-100 text-yellow-800'
          }`}>
            {backendStatus === 'connected' ? (
              <>
                <Wifi className="w-4 h-4 mr-2" />
                Backend Connected
              </>
            ) : backendStatus === 'disconnected' ? (
              <>
                <WifiOff className="w-4 h-4 mr-2" />
                Backend Disconnected
              </>
            ) : (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Checking Connection...
              </>
            )}
          </div>
          {backendStatus === 'disconnected' && (
            <p className="text-sm text-red-600 mt-2">
              Please start the backend service on port 5000
            </p>
          )}
        </div>

        {/* Upload Section */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <div className="text-center mb-8">
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Upload className="w-10 h-10 text-white" />
            </div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">
              Upload Your Document
            </h2>
            <p className="text-gray-600">
              Supported formats: PDF, JPG, PNG, JPEG
            </p>
          </div>

          {/* Drag & Drop Area */}
          <div
            className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 ${
              dragActive
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {file ? (
              <div className="flex items-center justify-center space-x-4">
                {getFileIcon(file.name)}
                <div className="text-left">
                  <p className="font-medium text-gray-900">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                <button
                  onClick={() => {
                    setFile(null);
                    setResult(null);
                  }}
                  className="text-red-500 hover:text-red-700"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <div>
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-lg text-gray-600 mb-2">
                  Drag and drop your document here
                </p>
                <p className="text-gray-500 mb-4">or</p>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                >
                  Browse Files
                </button>
              </div>
            )}
            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileChange}
              accept=".pdf,.jpg,.jpeg,.png"
              className="hidden"
            />
          </div>

          {/* Upload Button */}
          {file && (
            <div className="text-center mt-6">
              <button
                onClick={handleUpload}
                disabled={loading}
                className={`px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-200 ${
                  loading
                    ? 'bg-gray-400 cursor-not-allowed text-white'
                    : 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105 shadow-lg hover:shadow-xl'
                }`}
              >
                {loading ? (
                  <>
                    <Loader2 className="inline w-5 h-5 mr-2 animate-spin" />
                    Verifying Document...
                  </>
                ) : (
                  <>
                    <Shield className="inline w-5 h-5 mr-2" />
                    Verify Document
                  </>
                )}
              </button>
            </div>
          )}
        </div>

        {/* Results Section */}
        {result && (
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <div className="text-center mb-8">
              <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                Verification Complete
              </h2>
              <p className="text-gray-600">
                Your document has been processed and verified
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              {/* Document Information */}
              <div className="space-y-6">
                <div className="bg-blue-50 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <FileText className="w-5 h-5 mr-2 text-blue-600" />
                    Document Analysis
                  </h3>
                  <div className="space-y-3">
                    <div>
                      <span className="text-sm font-medium text-gray-600">Document Type (ML):</span>
                      <p className="text-gray-900 font-semibold">{result.doc_type_ml}</p>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-600">Document Type (Rule-based):</span>
                      <p className="text-gray-900 font-semibold">{result.doc_type_rule}</p>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-600">Fraud Risk:</span>
                      <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getFraudRiskColor(result.fraud_risk)}`}>
                        {result.fraud_risk}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="bg-green-50 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <Lock className="w-5 h-5 mr-2 text-green-600" />
                    Blockchain Security
                  </h3>
                  <div>
                    <span className="text-sm font-medium text-gray-600">Document Hash:</span>
                    <p className="text-gray-900 font-mono text-sm break-all mt-1">
                      {result.file_hash}
                    </p>
                  </div>
                </div>
              </div>

              {/* Extracted Text */}
              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <FileText className="w-5 h-5 mr-2 text-gray-600" />
                  Extracted Text
                </h3>
                <div className="bg-white rounded-lg p-4 max-h-64 overflow-y-auto">
                  <p className="text-gray-700 text-sm leading-relaxed">
                    {result.extracted_text || 'No text extracted'}
                  </p>
                </div>
              </div>
            </div>

            {/* Fraud Issues */}
            {result.fraud_issues && result.fraud_issues.length > 0 && (
              <div className="mt-8 bg-red-50 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <AlertCircle className="w-5 h-5 mr-2 text-red-600" />
                  Fraud Detection Issues
                </h3>
                <ul className="space-y-2">
                  {result.fraud_issues.map((issue, index) => (
                    <li key={index} className="flex items-start">
                      <AlertCircle className="w-4 h-4 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{issue}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

import React, { useEffect, useState } from 'react';
import { useVerification } from '../context/VerificationContext';
import { 
  FileText, 
  CheckCircle, 
  AlertTriangle, 
  Clock, 
  Eye, 
  Shield, 
  TrendingUp,
  Calendar,
  Search,
  Filter,
  Download,
  RefreshCw,
  ExternalLink,
  FileDown
} from 'lucide-react';

// Empty array - will be populated from backend
const mockVerificationHistory = [];

export default function ResultPage() {
  const { verificationHistory, loading, fetchVerificationHistory } = useVerification();
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterResult, setFilterResult] = useState('all');

  // Fetch verification history from backend
  useEffect(() => {
    fetchVerificationHistory();
  }, []);
  
  // Refresh data when page becomes visible (for when user navigates from upload page)
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        fetchVerificationHistory();
      }
    };
    
    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, []);



    try {
      setLoading(true);
      const response = await getVerificationHistory();
  const addVerificationToHistory = (verificationData) => {
    const newVerification = {
      id: Date.now(),
      filename: verificationData.filename,
      verifiedAt: new Date().toISOString(),
      fraudRisk: getFraudRiskPercentage(verificationData.fraud_risk),
      result: verificationData.fraud_risk === 'Low' ? 'Genuine' : 'Invalid',
      documentType: verificationData.doc_type_ml || verificationData.doc_type_rule,
      extractedText: verificationData.extracted_text,
      fraudIssues: verificationData.fraud_issues || [],
      fileHash: verificationData.file_hash
    };

    setVerificationHistory(prev => [newVerification, ...prev]);
  };

  const getFraudRiskPercentage = (risk) => {
    if (risk === 'Low') return 25;
    if (risk === 'Medium') return 60;
    if (risk === 'High') return 90;
    return 50;
  };

  const getFraudRiskColor = (risk) => {
    if (risk <= 30) return 'bg-green-500';
    if (risk <= 70) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getResultColor = (result) => {
    return result === 'Genuine' ? 'text-green-600' : 'text-red-600';
  };

  const getResultIcon = (result) => {
    return result === 'Genuine' ? 
      <CheckCircle className="w-5 h-5 text-green-500" /> : 
      <AlertTriangle className="w-5 h-5 text-red-500" />;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const filteredHistory = verificationHistory.filter(doc => {
    const matchesSearch = doc.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         doc.documentType.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterResult === 'all' || 
                         (filterResult === 'genuine' && doc.result === 'Genuine') ||
                         (filterResult === 'invalid' && doc.result === 'Invalid');
    
    return matchesSearch && matchesFilter;
  });

  const openModal = (document) => {
    setSelectedDocument(document);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedDocument(null);
  };

  // Export functions
  const exportToCSV = () => {
    const headers = ['Filename', 'Document Type', 'Verified Date', 'Fraud Risk (%)', 'Result', 'Blockchain Hash'];
    const csvData = verificationHistory.map(doc => [
      doc.filename,
      doc.documentType,
      formatDate(doc.verifiedAt),
      doc.fraudRisk,
      doc.result,
      doc.fileHash
    ]);
    
    const csvContent = [headers, ...csvData]
      .map(row => row.map(field => `"${field}"`).join(','))
      .join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `zeoverify_history_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const exportToPDF = () => {
    // Simple PDF generation using browser print
    const printContent = `
      <html>
        <head>
          <title>ZeoVerify - Verification History</title>
          <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .header { text-align: center; margin-bottom: 30px; }
            .stats { display: flex; justify-content: space-around; margin-bottom: 20px; }
            .stat { text-align: center; }
          </style>
        </head>
        <body>
          <div class="header">
            <h1>ZeoVerify - Document Verification History</h1>
            <p>Generated on: ${new Date().toLocaleString()}</p>
          </div>
          
          <div class="stats">
            <div class="stat">
              <h3>Total Documents</h3>
              <p>${verificationHistory.length}</p>
            </div>
            <div class="stat">
              <h3>Genuine</h3>
              <p>${verificationHistory.filter(doc => doc.result === 'Genuine').length}</p>
            </div>
            <div class="stat">
              <h3>Invalid</h3>
              <p>${verificationHistory.filter(doc => doc.result === 'Invalid').length}</p>
            </div>
          </div>
          
          <table>
            <thead>
              <tr>
                <th>Filename</th>
                <th>Document Type</th>
                <th>Verified Date</th>
                <th>Fraud Risk (%)</th>
                <th>Result</th>
              </tr>
            </thead>
            <tbody>
              ${verificationHistory.map(doc => `
                <tr>
                  <td>${doc.filename}</td>
                  <td>${doc.documentType}</td>
                  <td>${formatDate(doc.verifiedAt)}</td>
                  <td>${doc.fraudRisk}%</td>
                  <td>${doc.result}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </body>
      </html>
    `;

    // Create a new window and print content
    setTimeout(() => {
      const win = window.open('', '_blank');
      win.document.write(printContent);
      win.document.close();
      win.onload = () => {
        win.print();
        win.close();
      };
    }, 250);
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(printContent);
    printWindow.document.close();
    printWindow.print();
  };

  const getBlockchainExplorerUrl = (hash) => {
    // For Hardhat local network, you can use a local explorer or Etherscan testnet
    return `https://sepolia.etherscan.io/tx/${hash}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading verification history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center mb-4">
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-3 rounded-xl shadow-lg">
              <Shield className="w-8 h-8 text-white" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Verification Results
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Track and manage all your document verifications in one place
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center">
              <div className="bg-blue-100 p-3 rounded-lg">
                <FileText className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Documents</p>
                <p className="text-2xl font-bold text-gray-900">{verificationHistory.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center">
              <div className="bg-green-100 p-3 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Genuine</p>
                <p className="text-2xl font-bold text-gray-900">
                  {verificationHistory.filter(doc => doc.result === 'Genuine').length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center">
              <div className="bg-red-100 p-3 rounded-lg">
                <AlertTriangle className="w-6 h-6 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Invalid</p>
                <p className="text-2xl font-bold text-gray-900">
                  {verificationHistory.filter(doc => doc.result === 'Invalid').length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center">
              <div className="bg-purple-100 p-3 rounded-lg">
                <TrendingUp className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Avg Risk</p>
                <p className="text-2xl font-bold text-gray-900">
                  {verificationHistory.length > 0 
                    ? Math.round(verificationHistory.reduce((sum, doc) => sum + doc.fraudRisk, 0) / verificationHistory.length)
                    : 0}%
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Search, Filter, and Export */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search documents..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={fetchVerificationHistory}
                className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </button>
              
              <select
                value={filterResult}
                onChange={(e) => setFilterResult(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Results</option>
                <option value="genuine">Genuine Only</option>
                <option value="invalid">Invalid Only</option>
              </select>
            </div>
            {verificationHistory.length > 0 && (
              <div className="flex gap-2">
                <button
                  onClick={exportToCSV}
                  className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200"
                >
                  <FileDown className="w-4 h-4 mr-2" />
                  Export CSV
                </button>
                <button
                  onClick={exportToPDF}
                  className="flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors duration-200"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Export PDF
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Results Table */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {filteredHistory.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                {verificationHistory.length === 0 ? 'No documents verified yet' : 'No documents match your search'}
              </h3>
              <p className="text-gray-600 mb-6">
                {verificationHistory.length === 0 
                  ? 'Start by uploading and verifying your first document.'
                  : 'Try adjusting your search terms or filters.'
                }
              </p>
              {verificationHistory.length === 0 && (
                <button
                  onClick={() => window.location.href = '/'}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-200"
                >
                  Upload First Document
                </button>
              )}
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Document
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date Verified
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Fraud Risk
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Result
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Blockchain
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredHistory.map((document) => (
                    <tr key={document.id} className="hover:bg-gray-50 transition-colors duration-200">
                      <td className="px-6 py-4">
                        <div>
                          <div className="flex items-center">
                            <FileText className="w-5 h-5 text-blue-500 mr-3" />
                            <div>
                              <p className="text-sm font-medium text-gray-900">{document.filename}</p>
                              <p className="text-sm text-gray-500">{document.documentType}</p>
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center text-sm text-gray-900">
                          <Calendar className="w-4 h-4 mr-2 text-gray-400" />
                          {formatDate(document.verifiedAt)}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center">
                          <div className="w-16 bg-gray-200 rounded-full h-2 mr-3">
                            <div
                              className={`h-2 rounded-full ${getFraudRiskColor(document.fraudRisk)}`}
                              style={{ width: `${document.fraudRisk}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium text-gray-900">{document.fraudRisk}%</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center">
                          {getResultIcon(document.result)}
                          <span className={`ml-2 text-sm font-medium ${getResultColor(document.result)}`}>
                            {document.result} {document.result === 'Genuine' ? '✅' : '⚠️'}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <a
                          href={getBlockchainExplorerUrl(document.fileHash)}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center text-blue-600 hover:text-blue-800 transition-colors duration-200"
                        >
                          <ExternalLink className="w-4 h-4 mr-1" />
                          View TX
                        </a>
                      </td>
                      <td className="px-6 py-4">
                        <button
                          onClick={() => openModal(document)}
                          className="flex items-center text-blue-600 hover:text-blue-800 transition-colors duration-200"
                        >
                          <Eye className="w-4 h-4 mr-1" />
                          View Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Details Modal */}
      {showModal && selectedDocument && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200">
              <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900">Document Details</h2>
                <button
                  onClick={closeModal}
                  className="text-gray-400 hover:text-gray-600 transition-colors duration-200"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            <div className="p-6 space-y-6">
              {/* Document Info */}
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-blue-50 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <FileText className="w-5 h-5 mr-2 text-blue-600" />
                    Document Information
                  </h3>
                  <div className="space-y-3">
                    <div>
                      <span className="text-sm font-medium text-gray-600">Filename:</span>
                      <p className="text-gray-900 font-medium">{selectedDocument.filename}</p>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-600">Document Type:</span>
                      <p className="text-gray-900 font-medium">{selectedDocument.documentType}</p>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-600">Verified:</span>
                      <p className="text-gray-900 font-medium">{formatDate(selectedDocument.verifiedAt)}</p>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-600">Result:</span>
                      <div className="flex items-center mt-1">
                        {getResultIcon(selectedDocument.result)}
                        <span className={`ml-2 font-medium ${getResultColor(selectedDocument.result)}`}>
                          {selectedDocument.result} {selectedDocument.result === 'Genuine' ? '✅' : '⚠️'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-green-50 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <Shield className="w-5 h-5 mr-2 text-green-600" />
                    Security & Risk
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <span className="text-sm font-medium text-gray-600">Fraud Risk:</span>
                      <div className="flex items-center mt-2">
                        <div className="w-full bg-gray-200 rounded-full h-3 mr-3">
                          <div
                            className={`h-3 rounded-full ${getFraudRiskColor(selectedDocument.fraudRisk)}`}
                            style={{ width: `${selectedDocument.fraudRisk}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-bold text-gray-900">{selectedDocument.fraudRisk}%</span>
                      </div>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-600">Blockchain Hash:</span>
                      <p className="text-gray-900 font-mono text-sm break-all mt-1">
                        {selectedDocument.fileHash}
                      </p>
                      <a
                        href={getBlockchainExplorerUrl(selectedDocument.fileHash)}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-blue-600 hover:text-blue-800 text-sm mt-2 transition-colors duration-200"
                      >
                        <ExternalLink className="w-4 h-4 mr-1" />
                        View on Blockchain Explorer
                      </a>
                    </div>
                  </div>
                </div>
              </div>

              {/* Fraud Issues */}
              {selectedDocument.fraudIssues && selectedDocument.fraudIssues.length > 0 && (
                <div className="bg-red-50 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <AlertTriangle className="w-5 h-5 mr-2 text-red-600" />
                    Fraud Detection Issues
                  </h3>
                  <ul className="space-y-2">
                    {selectedDocument.fraudIssues.map((issue, index) => (
                      <li key={index} className="flex items-start">
                        <AlertTriangle className="w-4 h-4 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span className="text-gray-700">{issue}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Extracted Text */}
              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <FileText className="w-5 h-5 mr-2 text-gray-600" />
                  Extracted Text
                </h3>
                <div className="bg-white rounded-lg p-4 max-h-48 overflow-y-auto border">
                  <p className="text-gray-700 text-sm leading-relaxed">
                    {selectedDocument.extractedText || 'No text extracted'}
                  </p>
                </div>
              </div>
            </div>

            <div className="p-6 border-t border-gray-200">
              <button
                onClick={closeModal}
                className="w-full bg-gray-100 text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-200 transition-colors duration-200"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

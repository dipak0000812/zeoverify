import React, { createContext, useContext, useState, useEffect } from 'react';
import { getVerificationHistory } from '../services/api';

const VerificationContext = createContext();

export const useVerification = () => {
  const context = useContext(VerificationContext);
  if (!context) {
    throw new Error('useVerification must be used within a VerificationProvider');
  }
  return context;
};

export const VerificationProvider = ({ children }) => {
  const [verificationHistory, setVerificationHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchVerificationHistory = async () => {
    try {
      setLoading(true);
      const response = await getVerificationHistory();
      setVerificationHistory(response.data.data || []);
    } catch (error) {
      console.error('Error fetching verification history:', error);
    } finally {
      setLoading(false);
    }
  };

  const addVerificationToHistory = (verificationData) => {
    // Generate a filename if not provided (for backward compatibility)
    const filename = verificationData.filename || `document_${Date.now()}.pdf`;
    
    const newVerification = {
      id: verificationData.verification_id || Date.now(),
      filename: filename,
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

  useEffect(() => {
    fetchVerificationHistory();
  }, []);

  const value = {
    verificationHistory,
    loading,
    fetchVerificationHistory,
    addVerificationToHistory
  };

  return (
    <VerificationContext.Provider value={value}>
      {children}
    </VerificationContext.Provider>
  );
}; 
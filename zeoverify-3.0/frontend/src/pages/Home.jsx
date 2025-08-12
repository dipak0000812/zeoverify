import { Link } from 'react-router-dom';
import { 
  Shield, 
  FileText, 
  Zap, 
  Lock, 
  CheckCircle, 
  Brain, 
  Database, 
  Eye,
  ArrowRight,
  Sparkles,
  BadgeCheck,
  Fingerprint
} from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            {/* Main Icon */}
            <div className="flex justify-center mb-8">
              <div className="relative">
                <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 rounded-3xl shadow-2xl">
                  <Shield className="w-20 h-20 text-white" />
                </div>
                <div className="absolute -top-2 -right-2 bg-green-500 p-2 rounded-full shadow-lg">
                  <CheckCircle className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
            
            {/* Main Headline */}
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Secure & Seamless
              </span>
              <br />
              <span className="text-gray-900">Real Estate Document Verification</span>
            </h1>
            
            {/* Subtext */}
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto leading-relaxed">
              Powered by <span className="font-semibold text-blue-600">AI + Blockchain</span>. 
              Built to detect fraud and ensure trust — instantly.
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
              <Link
                to="/upload"
                className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl inline-flex items-center justify-center"
              >
                <Zap className="w-5 h-5 mr-2" />
                Start Verification
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
              <button 
                onClick={() => {
                  // Scroll to the "How It Works" section
                  document.getElementById('how-it-works').scrollIntoView({ 
                    behavior: 'smooth' 
                  });
                }}
                className="border-2 border-blue-600 text-blue-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-600 hover:text-white transition-all duration-200 inline-flex items-center justify-center"
              >
                <Eye className="w-5 h-5 mr-2" />
                Learn How It Works
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Trust & Security Badges */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200">
              <div className="bg-green-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Database className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Blockchain Secured</h3>
              <p className="text-gray-600">Every verification is immutably stored on the blockchain</p>
            </div>
            
            <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200">
              <div className="bg-blue-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Fraud Detection</h3>
              <p className="text-gray-600">Advanced machine learning detects suspicious patterns</p>
            </div>
            
            <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-purple-50 to-violet-50 border border-purple-200">
              <div className="bg-purple-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Lock className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Privacy First</h3>
              <p className="text-gray-600">Your documents are processed securely and privately</p>
            </div>
          </div>
        </div>
      </div>

      {/* Key Highlights Section */}
      <div className="py-20 bg-gradient-to-r from-gray-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Why Choose ZeoVerify?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Advanced technology meets real estate compliance for seamless document verification
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* AI Model Accuracy */}
            <div className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 border border-gray-100">
              <div className="flex items-center mb-6">
                <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-3 rounded-xl">
                  <Brain className="w-8 h-8 text-white" />
                </div>
                <div className="ml-4">
                  <h3 className="text-2xl font-bold text-gray-900">96%+</h3>
                  <p className="text-gray-600">Document Type Accuracy</p>
                </div>
              </div>
              <p className="text-gray-700 leading-relaxed">
                Our AI models have been trained on millions of real estate documents, 
                achieving industry-leading accuracy in document classification and text extraction.
              </p>
            </div>
            
            {/* Immutable Blockchain */}
            <div className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 border border-gray-100">
              <div className="flex items-center mb-6">
                <div className="bg-gradient-to-r from-green-600 to-emerald-600 p-3 rounded-xl">
                  <Database className="w-8 h-8 text-white" />
                </div>
                <div className="ml-4">
                  <h3 className="text-2xl font-bold text-gray-900">100%</h3>
                  <p className="text-gray-600">Immutable Records</p>
                </div>
              </div>
              <p className="text-gray-700 leading-relaxed">
                Every verification is permanently recorded on the blockchain, 
                creating an unchangeable audit trail that ensures document authenticity.
              </p>
            </div>
            
            {/* Fraud Detection */}
            <div className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 border border-gray-100">
              <div className="flex items-center mb-6">
                <div className="bg-gradient-to-r from-red-600 to-pink-600 p-3 rounded-xl">
                  <Shield className="w-8 h-8 text-white" />
                </div>
                <div className="ml-4">
                  <h3 className="text-2xl font-bold text-gray-900">Real-time</h3>
                  <p className="text-gray-600">Fraud Detection</p>
                </div>
              </div>
              <p className="text-gray-700 leading-relaxed">
                Instantly detects missing fields, tampering, suspicious patterns, 
                and provides risk assessment for every document uploaded.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div id="how-it-works" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Simple, secure, and lightning-fast document verification process
            </p>
          </div>
          
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-white font-bold text-xl">1</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Upload Document</h3>
              <p className="text-gray-600">Simply drag & drop or select your real estate document</p>
            </div>
            
            <div className="text-center">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-white font-bold text-xl">2</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">AI Analysis</h3>
              <p className="text-gray-600">Our AI extracts text and analyzes for fraud patterns</p>
            </div>
            
            <div className="text-center">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-white font-bold text-xl">3</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Blockchain Storage</h3>
              <p className="text-gray-600">Document hash is stored immutably on the blockchain</p>
            </div>
            
            <div className="text-center">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-white font-bold text-xl">4</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Get Results</h3>
              <p className="text-gray-600">Receive instant verification results and risk assessment</p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="py-20 bg-gradient-to-r from-blue-600 to-indigo-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-white mb-2">10K+</div>
              <div className="text-blue-100">Documents Verified</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-white mb-2">96%</div>
              <div className="text-blue-100">Accuracy Rate</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-white mb-2">500+</div>
              <div className="text-blue-100">Real Estate Firms</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-white mb-2">24/7</div>
              <div className="text-blue-100">Instant Verification</div>
            </div>
          </div>
        </div>
      </div>

      {/* Privacy Note */}
      <div className="py-12 bg-gray-50">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center mb-4">
            <Fingerprint className="w-6 h-6 text-blue-600 mr-2" />
            <span className="text-lg font-semibold text-gray-900">Privacy & Security</span>
          </div>
          <p className="text-gray-600 text-lg">
            All verifications are private, secure, and fully transparent. 
            Your documents are processed with enterprise-grade security.
          </p>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 bg-white">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            Ready to Transform Your Document Verification?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands of real estate professionals who trust ZeoVerify for secure, 
            fast, and accurate document verification.
          </p>
          <Link
            to="/upload"
            className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-10 py-4 rounded-xl font-semibold text-lg hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl inline-flex items-center"
          >
            <Sparkles className="w-5 h-5 mr-2" />
            Start Your First Verification
            <ArrowRight className="w-5 h-5 ml-2" />
          </Link>
        </div>
      </div>
    </div>
  );
}

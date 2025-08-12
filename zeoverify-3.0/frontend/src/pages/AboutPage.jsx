import React, { useEffect, useRef } from 'react';
import { 
  Shield, 
  Target, 
  Code, 
  Brain, 
  Database, 
  Eye, 
  Users, 
  Linkedin,
  ArrowRight,
  Sparkles,
  CheckCircle,
  Zap
} from 'lucide-react';

export default function AboutPage() {
  const sectionRefs = useRef([]);

  // Smooth scroll animation on mount
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in');
          }
        });
      },
      { threshold: 0.1 }
    );

    sectionRefs.current.forEach((ref) => {
      if (ref) observer.observe(ref);
    });

    return () => observer.disconnect();
  }, []);

  // Team data
  const teamMembers = [
    {
      name: "Dipak Dhangar",
      role: "AI & Blockchain Developer",
      description: "Combines AI and blockchain to build trustless systems for real estate. Focused on designing the AI fraud detection engine and blockchain smart contract logic powering ZeoVerify.",
      linkedin: "https://www.linkedin.com/in/dipak-dhangar",
      image: "/dipak.jpg"
    },
    {
      name: "Yashodeep More",
      role: "Lead Developer",
      description: "Strongest coder on the team. Brings experience in designing scalable systems, writing complex backend logic, and driving technical decisions to take ZeoVerify beyond the MVP.",
      linkedin: "https://www.linkedin.com/in/yashodipmore22/",
      image: "/yashodeep.jpg"
    },
    {
      name: "Bhupesh Patil",
      role: "Full Stack Developer (MERN)",
      description: "Integrates the entire product: frontend UI, backend APIs, and smart contract connections. Ensures the AI engine and blockchain verification flow seamlessly for users.",
      linkedin: "https://www.linkedin.com/in/bhupesh-patil-0799ab293/",
      image: "/bupesh.jpg"
    },
    {
      name: "Aakanksha Borse",
      role: "Pitch & Communications Lead",
      description: "Crafts the story, pitch deck and demo presentation. Translates the technical vision into a compelling narrative judges, investors, and end users can understand.",
      linkedin: "https://www.linkedin.com/in/aakanksha-borse-bb574632b/",
      image: "/aakanksha.jpg"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Hero Section */}
      <section 
        ref={(el) => (sectionRefs.current[0] = el)}
        className="relative overflow-hidden py-24"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
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
            
            {/* Main Title */}
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              About <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">ZeoVerify</span>
            </h1>
            
            {/* Subtitle */}
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto leading-relaxed">
              Building trust and security in real estate through 
              <span className="font-semibold text-blue-600"> AI and Blockchain</span>
            </p>
            
            {/* Decorative Elements */}
            <div className="flex justify-center space-x-4">
              <div className="flex items-center text-blue-600">
                <Sparkles className="w-5 h-5 mr-2" />
                <span className="text-sm font-medium">AI-Powered</span>
              </div>
              <div className="flex items-center text-green-600">
                <Database className="w-5 h-5 mr-2" />
                <span className="text-sm font-medium">Blockchain Secured</span>
              </div>
              <div className="flex items-center text-purple-600">
                <Shield className="w-5 h-5 mr-2" />
                <span className="text-sm font-medium">Fraud Protected</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section 
        ref={(el) => (sectionRefs.current[1] = el)}
        className="py-20 bg-white"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="flex justify-center mb-6">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 rounded-2xl">
                <Target className="w-8 h-8 text-white" />
              </div>
            </div>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Mission</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              We aim to eliminate fraud and inefficiency in real estate legal processes by creating a one-stop, 
              automated verification and compliance platform. Using AI to detect fraud and blockchain to store 
              immutable proof, we reduce time, cost and remove middlemen.
            </p>
          </div>

          {/* Mission Values */}
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-8 rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200">
              <div className="bg-blue-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Efficiency</h3>
              <p className="text-gray-600">
                Automate manual processes and reduce verification time from days to minutes
              </p>
            </div>
            
            <div className="text-center p-8 rounded-2xl bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200">
              <div className="bg-green-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Security</h3>
              <p className="text-gray-600">
                Blockchain-immutable records ensure document authenticity and prevent tampering
              </p>
            </div>
            
            <div className="text-center p-8 rounded-2xl bg-gradient-to-br from-purple-50 to-violet-50 border border-purple-200">
              <div className="bg-purple-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Intelligence</h3>
              <p className="text-gray-600">
                AI-powered fraud detection identifies suspicious patterns and missing information
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* What We Built Section */}
      <section 
        ref={(el) => (sectionRefs.current[2] = el)}
        className="py-20 bg-gradient-to-r from-gray-50 to-blue-50"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="flex justify-center mb-6">
              <div className="bg-gradient-to-r from-green-600 to-emerald-600 p-4 rounded-2xl">
                <Code className="w-8 h-8 text-white" />
              </div>
            </div>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">What We've Built So Far</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              A comprehensive platform that combines cutting-edge technology with real estate expertise
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* AI Engine */}
            <div className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 border border-gray-100">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 rounded-xl mb-6">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">AI Engine</h3>
              <p className="text-gray-600 mb-4">
                Advanced machine learning models to detect document fraud and suspicious patterns
              </p>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Pattern recognition
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Anomaly detection
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Risk assessment
                </li>
              </ul>
            </div>

            {/* OCR System */}
            <div className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 border border-gray-100">
              <div className="bg-gradient-to-r from-green-600 to-emerald-600 p-4 rounded-xl mb-6">
                <Eye className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">OCR System</h3>
              <p className="text-gray-600 mb-4">
                Optical Character Recognition to extract key fields from documents automatically
              </p>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Text extraction
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Field mapping
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Multi-format support
                </li>
              </ul>
            </div>

            {/* Smart Contracts */}
            <div className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 border border-gray-100">
              <div className="bg-gradient-to-r from-purple-600 to-violet-600 p-4 rounded-xl mb-6">
                <Database className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Smart Contracts</h3>
              <p className="text-gray-600 mb-4">
                Blockchain-based smart contracts to store immutable proof of verification
              </p>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Immutable records
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Audit trail
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Decentralized storage
                </li>
              </ul>
            </div>

            {/* Dashboard */}
            <div className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 border border-gray-100">
              <div className="bg-gradient-to-r from-orange-600 to-red-600 p-4 rounded-xl mb-6">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Dashboard</h3>
              <p className="text-gray-600 mb-4">
                Comprehensive dashboard to track verifications and manage document history
              </p>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Real-time tracking
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Analytics & reports
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Export capabilities
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section 
        ref={(el) => (sectionRefs.current[3] = el)}
        className="py-20 bg-white"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="flex justify-center mb-6">
              <div className="bg-gradient-to-r from-purple-600 to-violet-600 p-4 rounded-2xl">
                <Users className="w-8 h-8 text-white" />
              </div>
            </div>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Meet the Team</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              The passionate minds behind ZeoVerify's innovative document verification platform
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {teamMembers.map((member, index) => (
              <div key={index} className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 overflow-hidden group">
                <div className="p-6">
                  <div className="text-center">
                    {/* Profile Image */}
                    <div className="w-28 h-28 rounded-full overflow-hidden mx-auto mb-6 border-4 border-white shadow-xl group-hover:scale-105 transition-transform duration-300">
                      <img 
                        src={member.image} 
                        alt={member.name}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(member.name)}&background=3B82F6&color=fff&size=112`;
                        }}
                      />
                    </div>
                    
                    {/* Member Info */}
                    <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors duration-200">
                      {member.name}
                    </h3>
                    <p className="text-blue-600 font-semibold mb-3 text-sm uppercase tracking-wide">
                      {member.role}
                    </p>
                    <p className="text-gray-600 text-sm leading-relaxed mb-6 min-h-[3rem]">
                      {member.description}
                    </p>
                    
                    {/* LinkedIn Link */}
                    <a
                      href={member.linkedin}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center justify-center w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 group-hover:shadow-lg"
                    >
                      <Linkedin className="w-4 h-4 mr-2" />
                      Connect on LinkedIn
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-indigo-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-white mb-6">
            Ready to Transform Document Verification?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join us in building a more secure and efficient real estate industry
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-gray-100 transition-all duration-200 inline-flex items-center justify-center">
              <Sparkles className="w-5 h-5 mr-2" />
              Start Using ZeoVerify
              <ArrowRight className="w-5 h-5 ml-2" />
            </button>
            <button className="border-2 border-white text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white hover:text-blue-600 transition-all duration-200 inline-flex items-center justify-center">
              <Users className="w-5 h-5 mr-2" />
              Join Our Team
            </button>
          </div>
        </div>
      </section>

      {/* Custom CSS for animations */}
      <style jsx>{`
        .animate-fade-in {
          animation: fadeInUp 0.8s ease-out forwards;
        }
        
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
} 
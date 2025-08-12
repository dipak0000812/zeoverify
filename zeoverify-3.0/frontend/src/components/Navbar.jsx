import { Link, useLocation } from "react-router-dom";
import { Shield, Menu, X, Mail, Phone, MapPin, Send } from "lucide-react";
import { useState } from "react";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [showContactModal, setShowContactModal] = useState(false);
  const [contactForm, setContactForm] = useState({
    name: '',
    email: '',
    company: '',
    message: ''
  });
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  const handleContactSubmit = (e) => {
    e.preventDefault();
    // Here you would typically send the form data to your backend
    console.log('Contact form submitted:', contactForm);
    alert('Thank you for your message! We\'ll get back to you soon.');
    setContactForm({ name: '', email: '', company: '', message: '' });
    setShowContactModal(false);
  };

  const handleInputChange = (e) => {
    setContactForm({
      ...contactForm,
      [e.target.name]: e.target.value
    });
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-indigo-600 shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="bg-white/20 p-2 rounded-lg">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <span className="text-white font-bold text-xl">ZeoVerify</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              to="/"
              className={`text-white hover:text-blue-100 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                isActive('/') ? 'bg-white/20' : ''
              }`}
            >
              Home
            </Link>
            <Link
              to="/upload"
              className={`text-white hover:text-blue-100 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                isActive('/upload') ? 'bg-white/20' : ''
              }`}
            >
              Upload Document
            </Link>
            <Link
              to="/result"
              className={`text-white hover:text-blue-100 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                isActive('/result') ? 'bg-white/20' : ''
              }`}
            >
              Results
            </Link>
            <Link
              to="/about"
              className={`text-white hover:text-blue-100 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                isActive('/about') ? 'bg-white/20' : ''
              }`}
            >
              About
            </Link>
            <button 
              onClick={() => setShowContactModal(true)}
              className="bg-white/20 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-white/30 transition-colors duration-200"
            >
              Contact
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-white hover:text-blue-100 focus:outline-none focus:text-blue-100"
            >
              {isOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-blue-700 rounded-lg mt-2">
              <Link
                to="/"
                className={`text-white block px-3 py-2 rounded-md text-base font-medium ${
                  isActive('/') ? 'bg-white/20' : 'hover:bg-white/10'
                }`}
                onClick={() => setIsOpen(false)}
              >
                Home
              </Link>
              <Link
                to="/upload"
                className={`text-white block px-3 py-2 rounded-md text-base font-medium ${
                  isActive('/upload') ? 'bg-white/20' : 'hover:bg-white/10'
                }`}
                onClick={() => setIsOpen(false)}
              >
                Upload Document
              </Link>
              <Link
                to="/result"
                className={`text-white block px-3 py-2 rounded-md text-base font-medium ${
                  isActive('/result') ? 'bg-white/20' : 'hover:bg-white/10'
                }`}
                onClick={() => setIsOpen(false)}
              >
                Results
              </Link>
              <Link
                to="/about"
                className={`text-white block px-3 py-2 rounded-md text-base font-medium ${
                  isActive('/about') ? 'bg-white/20' : 'hover:bg-white/10'
                }`}
                onClick={() => setIsOpen(false)}
              >
                About
              </Link>
              <button 
                onClick={() => {
                  setShowContactModal(true);
                  setIsOpen(false);
                }}
                className="text-white block w-full text-left px-3 py-2 rounded-md text-base font-medium hover:bg-white/10"
              >
                Contact
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Contact Modal */}
      {showContactModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200">
              <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900">Contact Us</h2>
                <button
                  onClick={() => setShowContactModal(false)}
                  className="text-gray-400 hover:text-gray-600 transition-colors duration-200"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
            </div>

            <div className="p-6">
              <form onSubmit={handleContactSubmit} className="space-y-4">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                    Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={contactForm.name}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Your full name"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                    Email *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={contactForm.email}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="your.email@company.com"
                  />
                </div>

                <div>
                  <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-1">
                    Company
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={contactForm.company}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Your company name"
                  />
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
                    Message *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    value={contactForm.message}
                    onChange={handleInputChange}
                    required
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Tell us about your document verification needs..."
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 flex items-center justify-center"
                >
                  <Send className="w-4 h-4 mr-2" />
                  Send Message
                </button>
              </form>

              {/* Contact Info */}
              <div className="mt-8 pt-6 border-t border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Get in Touch</h3>
                <div className="space-y-3">
                  <div className="flex items-center">
                    <Mail className="w-4 h-4 text-blue-600 mr-3" />
                    <span className="text-gray-600">info@zeoverify.com</span>
                  </div>
                  <div className="flex items-center">
                    <Phone className="w-4 h-4 text-blue-600 mr-3" />
                    <span className="text-gray-600">+1 (555) 123-4567</span>
                  </div>
                  <div className="flex items-center">
                    <MapPin className="w-4 h-4 text-blue-600 mr-3" />
                    <span className="text-gray-600">San Francisco, CA</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}

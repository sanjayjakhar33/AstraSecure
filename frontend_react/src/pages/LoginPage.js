import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Navigate } from 'react-router-dom';
import { ShieldCheckIcon, EyeIcon, EyeSlashIcon, SparklesIcon } from '@heroicons/react/24/outline';

const LoginPage = () => {
  const { login, isAuthenticated } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  // Redirect if already authenticated
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await login(formData.email, formData.password);
    
    if (!result.success) {
      setError(result.error || 'Login failed');
    }
    
    setLoading(false);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center luxury-backdrop py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, rgba(255,255,255,0.15) 1px, transparent 0)`,
          backgroundSize: '50px 50px'
        }}></div>
      </div>
      
      {/* Floating Elements */}
      <div className="absolute top-20 left-20 w-32 h-32 bg-gradient-to-r from-luxury-500/20 to-royal-500/20 rounded-full blur-xl animate-float"></div>
      <div className="absolute bottom-20 right-20 w-48 h-48 bg-gradient-to-r from-emerald-500/20 to-gold-500/20 rounded-full blur-xl animate-float" style={{animationDelay: '2s'}}></div>
      <div className="absolute top-1/2 left-10 w-24 h-24 bg-gradient-to-r from-royal-500/20 to-luxury-500/20 rounded-full blur-xl animate-float" style={{animationDelay: '4s'}}></div>

      <div className="max-w-md w-full space-y-8 relative z-10">
        {/* Login Card */}
        <div className="card-luxury p-8 animate-slide-in">
          {/* Header */}
          <div className="text-center space-y-4 mb-8">
            <div className="mx-auto flex justify-center relative">
              <div className="w-20 h-20 bg-gradient-to-br from-luxury-500 to-luxury-700 rounded-2xl flex items-center justify-center shadow-luxury-lg relative">
                <ShieldCheckIcon className="w-12 h-12 text-white" />
                <div className="absolute -top-2 -right-2 w-6 h-6">
                  <SparklesIcon className="w-6 h-6 text-gold-400 animate-pulse" />
                </div>
              </div>
            </div>
            <div>
              <h2 className="text-4xl font-bold text-gradient mb-2">
                AstraSecure
              </h2>
              <h3 className="text-xl font-semibold text-slate-700 mb-2">
                Welcome Back
              </h3>
              <p className="text-slate-600 leading-relaxed">
                Secure your digital infrastructure with AI-driven cybersecurity auditing
              </p>
            </div>
          </div>

          {/* Login Form */}
          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-gradient-to-r from-red-50 to-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-xl shadow-md animate-slide-in">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <p className="font-medium">{error}</p>
                  </div>
                </div>
              </div>
            )}

            <div className="space-y-5">
              <div>
                <label htmlFor="email" className="block text-sm font-semibold text-slate-700 mb-2">
                  Email Address
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-white border-2 border-slate-200 text-slate-900 rounded-xl focus:outline-none focus:ring-2 focus:ring-luxury-500 focus:border-luxury-500 transition-all duration-300 hover:border-luxury-300"
                  placeholder="Enter your email address"
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-semibold text-slate-700 mb-2">
                  Password
                </label>
                <div className="relative">
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    autoComplete="current-password"
                    required
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full px-4 py-3 pr-12 bg-white border-2 border-slate-200 text-slate-900 rounded-xl focus:outline-none focus:ring-2 focus:ring-luxury-500 focus:border-luxury-500 transition-all duration-300 hover:border-luxury-300"
                    placeholder="Enter your password"
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-4 flex items-center"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeSlashIcon className="h-5 w-5 text-slate-400 hover:text-slate-600 transition-colors" />
                    ) : (
                      <EyeIcon className="h-5 w-5 text-slate-400 hover:text-slate-600 transition-colors" />
                    )}
                  </button>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 text-luxury-600 focus:ring-luxury-500 border-slate-300 rounded transition-colors"
                />
                <label htmlFor="remember-me" className="ml-3 block text-sm font-medium text-slate-700">
                  Remember me
                </label>
              </div>

              <div className="text-sm">
                <button type="button" className="font-semibold text-luxury-600 hover:text-luxury-700 transition-colors bg-transparent border-none cursor-pointer">
                  Forgot password?
                </button>
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="btn-luxury w-full py-4 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                {loading ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="luxury-spinner"></div>
                    <span>Signing in...</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center space-x-2">
                    <span>Sign In</span>
                    <ShieldCheckIcon className="w-5 h-5" />
                  </div>
                )}
              </button>
            </div>

            <div className="text-center pt-4">
              <p className="text-sm text-slate-600">
                Don't have an account?{' '}
                <button type="button" className="font-semibold text-luxury-600 hover:text-luxury-700 transition-colors bg-transparent border-none cursor-pointer">
                  Contact your administrator
                </button>
              </p>
            </div>
          </form>

          {/* Security Features */}
          <div className="mt-8 pt-8 border-t border-slate-200/50">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="space-y-2">
                <div className="w-8 h-8 bg-emerald-100 rounded-lg flex items-center justify-center mx-auto">
                  <div className="w-3 h-3 bg-emerald-500 rounded-full"></div>
                </div>
                <p className="text-xs font-medium text-slate-600">Secure Login</p>
              </div>
              <div className="space-y-2">
                <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center mx-auto">
                  <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                </div>
                <p className="text-xs font-medium text-slate-600">Encrypted</p>
              </div>
              <div className="space-y-2">
                <div className="w-8 h-8 bg-gold-100 rounded-lg flex items-center justify-center mx-auto">
                  <div className="w-3 h-3 bg-gold-500 rounded-full"></div>
                </div>
                <p className="text-xs font-medium text-slate-600">AI-Powered</p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center">
          <p className="text-sm text-white/70">
            © 2024 AstraSecure. Enterprise-grade cybersecurity solutions.
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
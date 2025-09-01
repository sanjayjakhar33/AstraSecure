import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  HomeIcon, 
  ShieldCheckIcon, 
  ExclamationTriangleIcon,
  DocumentCheckIcon,
  DocumentTextIcon,
  CogIcon,
  ChartBarIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon, gradient: 'from-royal-500 to-royal-700' },
  { name: 'Scan Targets', href: '/scan-targets', icon: ShieldCheckIcon, gradient: 'from-emerald-500 to-emerald-700' },
  { name: 'Vulnerabilities', href: '/vulnerabilities', icon: ExclamationTriangleIcon, gradient: 'from-red-500 to-red-700' },
  { name: 'Compliance', href: '/compliance', icon: DocumentCheckIcon, gradient: 'from-gold-500 to-gold-700' },
  { name: 'Reports', href: '/reports', icon: DocumentTextIcon, gradient: 'from-purple-500 to-purple-700' },
  { name: 'Analytics', href: '/analytics', icon: ChartBarIcon, gradient: 'from-indigo-500 to-indigo-700' },
  { name: 'Settings', href: '/settings', icon: CogIcon, gradient: 'from-slate-500 to-slate-700' },
];

const Sidebar = () => {
  return (
    <div className="w-72 glass border-r border-white/20 relative overflow-hidden">
      {/* Background Gradient Overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-white/10 to-white/5 pointer-events-none"></div>
      
      {/* Logo Section */}
      <div className="relative px-8 py-6 border-b border-white/20">
        <div className="flex items-center space-x-4">
          <div className="relative">
            <div className="w-12 h-12 bg-gradient-to-br from-luxury-500 to-luxury-700 rounded-2xl flex items-center justify-center shadow-glow">
              <ShieldCheckIcon className="w-7 h-7 text-white" />
            </div>
            <div className="absolute -top-1 -right-1 w-4 h-4">
              <SparklesIcon className="w-4 h-4 text-gold-400 animate-pulse" />
            </div>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">AstraSecure</h1>
            <p className="text-sm text-white/70 font-medium">Enterprise Security</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="relative mt-8 px-6">
        <ul className="space-y-3">
          {navigation.map((item, index) => (
            <li key={item.name} className="transform transition-transform duration-200 hover:scale-105">
              <NavLink
                to={item.href}
                className={({ isActive }) =>
                  `group flex items-center px-4 py-3 text-sm font-semibold rounded-xl transition-all duration-300 relative overflow-hidden ${
                    isActive
                      ? 'bg-gradient-to-r from-white/20 to-white/10 text-white border border-white/30 shadow-luxury'
                      : 'text-white/80 hover:bg-white/10 hover:text-white hover:shadow-md'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    {/* Background Gradient for Active State */}
                    {isActive && (
                      <div className={`absolute inset-0 bg-gradient-to-r ${item.gradient} opacity-20 rounded-xl`}></div>
                    )}
                    
                    {/* Icon with Gradient Background */}
                    <div className={`relative p-2 rounded-lg mr-4 ${
                      isActive 
                        ? `bg-gradient-to-r ${item.gradient} shadow-lg` 
                        : 'bg-white/10 group-hover:bg-white/20'
                    } transition-all duration-300`}>
                      <item.icon className="w-5 h-5 text-white" />
                    </div>
                    
                    {/* Navigation Text */}
                    <span className="relative z-10 font-medium tracking-wide">{item.name}</span>
                    
                    {/* Active Indicator */}
                    {isActive && (
                      <div className="absolute right-3 w-2 h-2 bg-white rounded-full shadow-glow animate-pulse"></div>
                    )}
                    
                    {/* Hover Effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
                  </>
                )}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* Quick Stats */}
      <div className="relative mt-8 mx-6 p-4 bg-gradient-to-br from-white/10 to-white/5 rounded-xl border border-white/20 backdrop-blur-sm">
        <h3 className="text-sm font-semibold text-white mb-3">Quick Stats</h3>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-xs text-white/70">Active Scans</span>
            <span className="text-sm font-bold text-emerald-400">3</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-xs text-white/70">Critical Issues</span>
            <span className="text-sm font-bold text-red-400">8</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-xs text-white/70">Risk Score</span>
            <span className="text-sm font-bold text-gold-400">73/100</span>
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-white/20 bg-gradient-to-t from-black/20 to-transparent">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center text-white/80">
            <div className="status-indicator mr-3"></div>
            <span className="font-medium">System Operational</span>
          </div>
          <div className="text-white/60 text-xs">v2.1.0</div>
        </div>
        
        {/* Resource Usage */}
        <div className="mt-3 space-y-2">
          <div className="flex items-center justify-between text-xs">
            <span className="text-white/60">CPU Usage</span>
            <span className="text-emerald-400 font-mono">23%</span>
          </div>
          <div className="w-full bg-white/10 rounded-full h-1">
            <div className="bg-gradient-to-r from-emerald-400 to-emerald-600 h-1 rounded-full" style={{width: '23%'}}></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
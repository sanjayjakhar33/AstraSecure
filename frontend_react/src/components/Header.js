import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { 
  BellIcon, 
  MagnifyingGlassIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  UserIcon,
  ChevronDownIcon
} from '@heroicons/react/24/outline';

const Header = () => {
  const { user, logout } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [notifications] = useState([
    { id: 1, title: 'Critical vulnerability detected', type: 'error', time: '2m ago' },
    { id: 2, title: 'Scan completed successfully', type: 'success', time: '5m ago' },
    { id: 3, title: 'New compliance report available', type: 'info', time: '1h ago' },
  ]);

  return (
    <header className="glass border-b border-white/20 relative z-10">
      <div className="flex items-center justify-between px-8 py-4">
        {/* Left Section - Search */}
        <div className="flex-1 max-w-lg">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-5 w-5 text-white/60" />
            </div>
            <input
              type="text"
              placeholder="Search vulnerabilities, targets, reports..."
              className="input-luxury pl-12 pr-4 w-full"
            />
            <div className="absolute inset-y-0 right-0 pr-4 flex items-center">
              <kbd className="px-2 py-1 text-xs font-semibold text-white/60 bg-white/10 border border-white/20 rounded-md">
                ⌘K
              </kbd>
            </div>
          </div>
        </div>

        {/* Center Section - Page Title */}
        <div className="flex-1 text-center">
          <h1 className="text-2xl font-bold text-gradient">
            Security Command Center
          </h1>
          <p className="text-sm text-white/70 mt-1">Real-time threat monitoring & analysis</p>
        </div>

        {/* Right Section - Actions */}
        <div className="flex-1 flex items-center justify-end space-x-4">
          {/* Notifications */}
          <div className="relative">
            <button className="relative p-3 text-white/80 hover:text-white transition-colors duration-200 hover:bg-white/10 rounded-xl group">
              <BellIcon className="w-6 h-6" />
              {/* Notification Badge */}
              <div className="absolute -top-1 -right-1 w-5 h-5 bg-gradient-to-r from-red-500 to-red-600 text-white text-xs font-bold rounded-full flex items-center justify-center shadow-glow animate-pulse">
                3
              </div>
              
              {/* Notification Dropdown */}
              <div className="absolute right-0 mt-2 w-80 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 transform translate-y-2 group-hover:translate-y-0">
                <div className="bg-white/95 backdrop-blur-xl rounded-2xl shadow-luxury-xl border border-white/20 overflow-hidden">
                  <div className="px-6 py-4 border-b border-gray-200/50">
                    <h3 className="text-lg font-semibold text-gray-900">Notifications</h3>
                  </div>
                  <div className="max-h-80 overflow-y-auto">
                    {notifications.map((notif) => (
                      <div key={notif.id} className="px-6 py-4 hover:bg-gray-50/50 transition-colors duration-200 border-b border-gray-100/50 last:border-b-0">
                        <div className="flex items-start space-x-3">
                          <div className={`w-3 h-3 rounded-full mt-2 ${
                            notif.type === 'error' ? 'bg-red-500' :
                            notif.type === 'success' ? 'bg-emerald-500' : 'bg-blue-500'
                          }`}></div>
                          <div className="flex-1">
                            <p className="text-sm font-medium text-gray-900">{notif.title}</p>
                            <p className="text-xs text-gray-500 mt-1">{notif.time}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="px-6 py-3 bg-gray-50/50">
                    <button className="w-full text-sm font-medium text-luxury-600 hover:text-luxury-700 transition-colors">
                      View all notifications
                    </button>
                  </div>
                </div>
              </div>
            </button>
          </div>

          {/* Quick Actions */}
          <button className="p-3 text-white/80 hover:text-white transition-colors duration-200 hover:bg-white/10 rounded-xl">
            <Cog6ToothIcon className="w-6 h-6" />
          </button>

          {/* User Menu */}
          <div className="relative">
            <button 
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-3 p-2 text-white/80 hover:text-white transition-all duration-200 hover:bg-white/10 rounded-xl group"
            >
              <div className="text-right">
                <p className="text-sm font-semibold text-white">{user?.full_name || user?.email}</p>
                <p className="text-xs text-white/60 capitalize font-medium">{user?.role?.replace('_', ' ')}</p>
              </div>
              
              <div className="relative">
                <div className="w-10 h-10 bg-gradient-to-br from-luxury-500 to-luxury-700 rounded-xl flex items-center justify-center shadow-lg group-hover:shadow-glow transform group-hover:scale-105 transition-all duration-200">
                  <UserIcon className="w-6 h-6 text-white" />
                </div>
                <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-emerald-500 border-2 border-white rounded-full"></div>
              </div>
              
              <ChevronDownIcon className={`w-4 h-4 transition-transform duration-200 ${showUserMenu ? 'rotate-180' : ''}`} />
            </button>
            
            {/* User Dropdown */}
            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-56 bg-white/95 backdrop-blur-xl rounded-2xl shadow-luxury-xl border border-white/20 overflow-hidden z-50">
                <div className="px-6 py-4 border-b border-gray-200/50">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-gradient-to-br from-luxury-500 to-luxury-700 rounded-xl flex items-center justify-center">
                      <UserIcon className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">{user?.full_name || user?.email}</p>
                      <p className="text-sm text-gray-500 capitalize">{user?.role?.replace('_', ' ')}</p>
                    </div>
                  </div>
                </div>
                
                <div className="py-2">
                  <button className="w-full px-6 py-3 text-left text-sm text-gray-700 hover:bg-gray-50/50 transition-colors duration-200 flex items-center space-x-3">
                    <UserIcon className="w-4 h-4" />
                    <span>Profile Settings</span>
                  </button>
                  <button className="w-full px-6 py-3 text-left text-sm text-gray-700 hover:bg-gray-50/50 transition-colors duration-200 flex items-center space-x-3">
                    <Cog6ToothIcon className="w-4 h-4" />
                    <span>Preferences</span>
                  </button>
                </div>
                
                <div className="border-t border-gray-200/50 py-2">
                  <button 
                    onClick={logout}
                    className="w-full px-6 py-3 text-left text-sm text-red-600 hover:bg-red-50/50 transition-colors duration-200 flex items-center space-x-3"
                  >
                    <ArrowRightOnRectangleIcon className="w-4 h-4" />
                    <span>Sign out</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Subtle gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-luxury-500/5 via-transparent to-royal-500/5 pointer-events-none"></div>
    </header>
  );
};

export default Header;
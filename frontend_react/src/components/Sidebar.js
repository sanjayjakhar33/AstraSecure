import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  HomeIcon, 
  ShieldCheckIcon, 
  ExclamationTriangleIcon,
  DocumentCheckIcon,
  DocumentTextIcon,
  CogIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Scan Targets', href: '/scan-targets', icon: ShieldCheckIcon },
  { name: 'Vulnerabilities', href: '/vulnerabilities', icon: ExclamationTriangleIcon },
  { name: 'Compliance', href: '/compliance', icon: DocumentCheckIcon },
  { name: 'Reports', href: '/reports', icon: DocumentTextIcon },
  { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
];

const Sidebar = () => {
  return (
    <div className="w-64 bg-white shadow-sm border-r border-gray-200">
      {/* Logo */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <ShieldCheckIcon className="w-5 h-5 text-white" />
          </div>
          <span className="ml-3 text-xl font-bold text-gray-900">AstraSecure</span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="mt-8 px-4">
        <ul className="space-y-2">
          {navigation.map((item) => (
            <li key={item.name}>
              <NavLink
                to={item.href}
                className={({ isActive }) =>
                  `flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                    isActive
                      ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-700'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }`
                }
              >
                <item.icon className="w-5 h-5 mr-3" />
                {item.name}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* Bottom section */}
      <div className="absolute bottom-0 w-64 p-4 border-t border-gray-200">
        <div className="flex items-center text-sm text-gray-600">
          <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
          System Status: Operational
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
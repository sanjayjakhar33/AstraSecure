import React from 'react';
import { 
  ShieldCheckIcon, 
  ExclamationTriangleIcon,
  ChartBarIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

const DashboardPage = () => {
  // Mock data - in real app this would come from API
  const stats = {
    totalTargets: 24,
    activeVulns: 127,
    criticalVulns: 8,
    riskScore: 73,
    complianceScore: 85,
    lastScan: '2 hours ago'
  };

  const recentVulns = [
    {
      id: 1,
      title: 'SQL Injection Vulnerability',
      severity: 'critical',
      target: 'web-app-1.example.com',
      discovered: '2 hours ago'
    },
    {
      id: 2,
      title: 'Unencrypted HTTP Service',
      severity: 'medium',
      target: '192.168.1.100',
      discovered: '4 hours ago'
    },
    {
      id: 3,
      title: 'Outdated SSL Certificate',
      severity: 'high',
      target: 'api.example.com',
      discovered: '6 hours ago'
    }
  ];

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Security Dashboard</h1>
        <p className="text-gray-600 mt-2">
          Monitor your organization's security posture and vulnerability status
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Risk Score */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-md bg-red-100">
              <ExclamationTriangleIcon className="w-6 h-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Risk Score</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.riskScore}/100</p>
            </div>
          </div>
        </div>

        {/* Active Vulnerabilities */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-md bg-orange-100">
              <ShieldCheckIcon className="w-6 h-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Vulnerabilities</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.activeVulns}</p>
            </div>
          </div>
        </div>

        {/* Compliance Score */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-md bg-green-100">
              <ChartBarIcon className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Compliance Score</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.complianceScore}%</p>
            </div>
          </div>
        </div>

        {/* Scan Targets */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-md bg-blue-100">
              <ClockIcon className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Scan Targets</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.totalTargets}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Vulnerabilities */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Recent Vulnerabilities</h3>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {recentVulns.map((vuln) => (
                <div key={vuln.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900">{vuln.title}</h4>
                    <p className="text-sm text-gray-600">{vuln.target}</p>
                    <p className="text-xs text-gray-500">{vuln.discovered}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSeverityColor(vuln.severity)}`}>
                    {vuln.severity.toUpperCase()}
                  </span>
                </div>
              ))}
            </div>
            <div className="mt-4">
              <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                View all vulnerabilities →
              </button>
            </div>
          </div>
        </div>

        {/* Security Trends */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Security Trends</h3>
          </div>
          <div className="p-6">
            <div className="text-center text-gray-500 py-12">
              <ChartBarIcon className="w-12 h-12 mx-auto mb-4 text-gray-400" />
              <p>Security trend charts will be displayed here</p>
              <p className="text-sm">Integration with Chart.js coming soon</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
            <ShieldCheckIcon className="w-6 h-6 text-blue-600 mb-2" />
            <h4 className="font-medium text-gray-900">Start New Scan</h4>
            <p className="text-sm text-gray-600">Initiate a security scan on your targets</p>
          </button>
          
          <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
            <ExclamationTriangleIcon className="w-6 h-6 text-orange-600 mb-2" />
            <h4 className="font-medium text-gray-900">Review Vulnerabilities</h4>
            <p className="text-sm text-gray-600">Assess and prioritize security findings</p>
          </button>
          
          <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
            <ChartBarIcon className="w-6 h-6 text-green-600 mb-2" />
            <h4 className="font-medium text-gray-900">Generate Report</h4>
            <p className="text-sm text-gray-600">Create compliance and security reports</p>
          </button>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
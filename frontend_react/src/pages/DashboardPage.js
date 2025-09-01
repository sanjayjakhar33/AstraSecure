import React from 'react';
import { 
  ShieldCheckIcon, 
  ExclamationTriangleIcon,
  ChartBarIcon,
  ClockIcon,
  FireIcon,
  TrophyIcon,
  BoltIcon,
  EyeIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon
} from '@heroicons/react/24/outline';

const DashboardPage = () => {
  // Mock data - in real app this would come from API
  const stats = {
    totalTargets: 24,
    activeVulns: 127,
    criticalVulns: 8,
    riskScore: 73,
    complianceScore: 85,
    lastScan: '2 hours ago',
    scanningNow: 3,
    resolvedToday: 12
  };

  const recentVulns = [
    {
      id: 1,
      title: 'SQL Injection Vulnerability',
      severity: 'critical',
      target: 'web-app-1.example.com',
      discovered: '2 hours ago',
      cvss: '9.8'
    },
    {
      id: 2,
      title: 'Unencrypted HTTP Service',
      severity: 'medium',
      target: '192.168.1.100',
      discovered: '4 hours ago',
      cvss: '6.1'
    },
    {
      id: 3,
      title: 'Outdated SSL Certificate',
      severity: 'high',
      target: 'api.example.com',
      discovered: '6 hours ago',
      cvss: '7.4'
    },
    {
      id: 4,
      title: 'Weak Password Policy',
      severity: 'medium',
      target: 'auth.example.com',
      discovered: '8 hours ago',
      cvss: '5.3'
    }
  ];

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'severity-critical';
      case 'high': return 'severity-high';
      case 'medium': return 'severity-medium';
      case 'low': return 'severity-low';
      default: return 'severity-info';
    }
  };

  const StatCard = ({ title, value, subtitle, icon: Icon, gradient, trend, trendValue }) => (
    <div className="card-luxury p-6 group hover:shadow-luxury-lg transition-all duration-500 transform hover:-translate-y-1">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <div className={`p-3 rounded-xl bg-gradient-to-r ${gradient} shadow-lg`}>
              <Icon className="w-6 h-6 text-white" />
            </div>
            {trend && (
              <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-semibold ${
                trend === 'up' ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'
              }`}>
                {trend === 'up' ? (
                  <ArrowTrendingUpIcon className="w-3 h-3" />
                ) : (
                  <ArrowTrendingDownIcon className="w-3 h-3" />
                )}
                <span>{trendValue}</span>
              </div>
            )}
          </div>
          <h3 className="text-sm font-semibold text-slate-600 mb-1">{title}</h3>
          <p className="text-3xl font-bold text-slate-900 mb-1">{value}</p>
          {subtitle && <p className="text-xs text-slate-500 font-medium">{subtitle}</p>}
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Page Header */}
      <div className="text-center space-y-4">
        <h1 className="text-5xl font-bold text-gradient">Security Command Center</h1>
        <p className="text-lg text-white/80 max-w-2xl mx-auto leading-relaxed">
          Real-time monitoring and comprehensive analysis of your organization's security posture
        </p>
        <div className="flex justify-center space-x-4">
          <div className="flex items-center space-x-2 text-white/70">
            <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium">Live Monitoring Active</span>
          </div>
          <div className="text-white/50">•</div>
          <div className="text-white/70 text-sm font-medium">Last updated: {stats.lastScan}</div>
        </div>
      </div>

      {/* Quick Action Bar */}
      <div className="flex justify-center">
        <div className="flex space-x-4">
          <button className="btn-royal">
            <BoltIcon className="w-5 h-5 mr-2" />
            Start Emergency Scan
          </button>
          <button className="btn-emerald">
            <EyeIcon className="w-5 h-5 mr-2" />
            Live Dashboard
          </button>
          <button className="btn-gold">
            <TrophyIcon className="w-5 h-5 mr-2" />
            Generate Report
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Risk Score"
          value={`${stats.riskScore}/100`}
          subtitle="Medium Risk Level"
          icon={ExclamationTriangleIcon}
          gradient="from-red-500 to-red-700"
          trend="down"
          trendValue="5%"
        />
        
        <StatCard
          title="Active Vulnerabilities"
          value={stats.activeVulns}
          subtitle={`${stats.criticalVulns} Critical Issues`}
          icon={ShieldCheckIcon}
          gradient="from-orange-500 to-orange-700"
          trend="up"
          trendValue="12%"
        />
        
        <StatCard
          title="Compliance Score"
          value={`${stats.complianceScore}%`}
          subtitle="SOC2 & ISO27001"
          icon={TrophyIcon}
          gradient="from-emerald-500 to-emerald-700"
          trend="up"
          trendValue="3%"
        />
        
        <StatCard
          title="Scan Targets"
          value={stats.totalTargets}
          subtitle={`${stats.scanningNow} Currently Scanning`}
          icon={ClockIcon}
          gradient="from-blue-500 to-blue-700"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Recent Vulnerabilities - Takes 2 columns */}
        <div className="xl:col-span-2">
          <div className="card-luxury">
            <div className="px-8 py-6 border-b border-slate-200/50">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-slate-900">Critical Vulnerabilities</h3>
                  <p className="text-slate-600 mt-1">Immediate attention required</p>
                </div>
                <div className="flex items-center space-x-2">
                  <FireIcon className="w-5 h-5 text-red-500" />
                  <span className="text-sm font-semibold text-red-600">{stats.criticalVulns} Critical</span>
                </div>
              </div>
            </div>
            <div className="p-8">
              <div className="space-y-4">
                {recentVulns.map((vuln, index) => (
                  <div key={vuln.id} className={`group p-6 border-2 border-slate-200/50 rounded-xl hover:border-luxury-300 transition-all duration-300 hover:shadow-lg transform hover:-translate-y-1 ${
                    index === 0 ? 'bg-red-50/50 border-red-200' : ''
                  }`}>
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h4 className="font-semibold text-slate-900 group-hover:text-luxury-700 transition-colors">
                            {vuln.title}
                          </h4>
                          <span className={`px-3 py-1 text-xs font-bold rounded-full ${getSeverityColor(vuln.severity)}`}>
                            {vuln.severity.toUpperCase()}
                          </span>
                        </div>
                        <div className="flex items-center space-x-4 text-sm text-slate-600">
                          <span className="flex items-center space-x-1">
                            <span className="font-medium">Target:</span>
                            <span className="font-mono text-slate-800">{vuln.target}</span>
                          </span>
                          <span>•</span>
                          <span className="flex items-center space-x-1">
                            <span className="font-medium">CVSS:</span>
                            <span className="font-bold text-red-600">{vuln.cvss}</span>
                          </span>
                          <span>•</span>
                          <span>{vuln.discovered}</span>
                        </div>
                      </div>
                      <button className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 px-4 py-2 bg-luxury-500 text-white text-sm font-medium rounded-lg hover:bg-luxury-600">
                        Investigate
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-6 pt-6 border-t border-slate-200/50">
                <button className="w-full py-3 text-luxury-600 hover:text-luxury-700 font-semibold text-center hover:bg-luxury-50 rounded-xl transition-all duration-200">
                  View All Vulnerabilities ({stats.activeVulns}) →
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Side Panel - Quick Actions & Stats */}
        <div className="space-y-6">
          {/* Security Trends */}
          <div className="card-luxury">
            <div className="px-6 py-4 border-b border-slate-200/50">
              <h3 className="text-lg font-bold text-slate-900">Security Trends</h3>
            </div>
            <div className="p-6">
              <div className="space-y-6">
                <div className="text-center py-8">
                  <div className="w-16 h-16 bg-gradient-to-br from-luxury-500 to-luxury-700 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-luxury">
                    <ChartBarIcon className="w-8 h-8 text-white" />
                  </div>
                  <p className="text-slate-600 mb-2">Advanced Analytics</p>
                  <p className="text-sm text-slate-500">Premium charts and insights coming soon</p>
                </div>
                
                {/* Mini Stats */}
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
                    <span className="text-sm font-medium text-slate-700">Resolved Today</span>
                    <span className="text-lg font-bold text-emerald-600">{stats.resolvedToday}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
                    <span className="text-sm font-medium text-slate-700">New This Week</span>
                    <span className="text-lg font-bold text-red-600">34</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
                    <span className="text-sm font-medium text-slate-700">Average Fix Time</span>
                    <span className="text-lg font-bold text-blue-600">2.3h</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="card-luxury">
            <div className="px-6 py-4 border-b border-slate-200/50">
              <h3 className="text-lg font-bold text-slate-900">Quick Actions</h3>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                <button className="w-full p-4 text-left bg-gradient-to-r from-royal-50 to-royal-100 hover:from-royal-100 hover:to-royal-200 border border-royal-200 rounded-xl transition-all duration-300 group">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-royal-500 rounded-lg">
                      <ShieldCheckIcon className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-slate-900 group-hover:text-royal-700">Start New Scan</h4>
                      <p className="text-sm text-slate-600">Initiate comprehensive security assessment</p>
                    </div>
                  </div>
                </button>
                
                <button className="w-full p-4 text-left bg-gradient-to-r from-orange-50 to-orange-100 hover:from-orange-100 hover:to-orange-200 border border-orange-200 rounded-xl transition-all duration-300 group">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-orange-500 rounded-lg">
                      <ExclamationTriangleIcon className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-slate-900 group-hover:text-orange-700">Review Critical</h4>
                      <p className="text-sm text-slate-600">Assess high-priority security findings</p>
                    </div>
                  </div>
                </button>
                
                <button className="w-full p-4 text-left bg-gradient-to-r from-emerald-50 to-emerald-100 hover:from-emerald-100 hover:to-emerald-200 border border-emerald-200 rounded-xl transition-all duration-300 group">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-emerald-500 rounded-lg">
                      <ChartBarIcon className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-slate-900 group-hover:text-emerald-700">Generate Report</h4>
                      <p className="text-sm text-slate-600">Create compliance and security reports</p>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
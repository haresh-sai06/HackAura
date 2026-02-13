'use client';

import React, { useState } from 'react';
import { 
  TeamCard, 
  NotificationCard, 
  AnalyticsCard, 
  EmergencyCallCard,
  TeamMemberCard 
} from '@/components/ProfessionalCards';
import { 
  Users, 
  Bell, 
  BarChart3, 
  Phone, 
  AlertTriangle,
  TrendingUp,
  Clock,
  Activity,
  UserCheck
} from 'lucide-react';

export default function ProfessionalCardsPage() {
  const [activeTab, setActiveTab] = useState('teams');

  // Mock teams data
  const teams = [
    {
      id: '1',
      name: 'Medical Response Team',
      specialization: 'medical',
      total_members: 8,
      active_members: 6,
      available_members: 4,
      active_calls: 2
    },
    {
      id: '2',
      name: 'Fire Response Team',
      specialization: 'fire',
      total_members: 12,
      active_members: 10,
      available_members: 7,
      active_calls: 3
    },
    {
      id: '3',
      name: 'Police Response Team',
      specialization: 'police',
      total_members: 15,
      active_members: 12,
      available_members: 8,
      active_calls: 4
    },
    {
      id: '4',
      name: 'General Response Team',
      specialization: 'general',
      total_members: 10,
      active_members: 8,
      available_members: 6,
      active_calls: 1
    }
  ];

  // Mock notifications data
  const notifications = [
    {
      id: '1',
      title: 'Emergency Call Assigned',
      message: 'Medical emergency call has been assigned to Dr. Smith. Patient experiencing chest pain and difficulty breathing.',
      priority: 'urgent',
      created_at: new Date().toISOString(),
      status: 'delivered'
    },
    {
      id: '2',
      title: 'Team Member Offline',
      message: 'John Doe has gone offline. Last active: 5 minutes ago.',
      priority: 'medium',
      created_at: new Date(Date.now() - 300000).toISOString(),
      status: 'read'
    },
    {
      id: '3',
      title: 'High Call Volume Alert',
      message: 'Call volume is 25% above normal. Consider adding more team members to handle the increased load.',
      priority: 'high',
      created_at: new Date(Date.now() - 600000).toISOString(),
      status: 'sent'
    },
    {
      id: '4',
      title: 'Performance Alert',
      message: 'Average response time is 45s, which is above the threshold of 30s. Team performance needs attention.',
      priority: 'high',
      created_at: new Date(Date.now() - 900000).toISOString(),
      status: 'pending'
    }
  ];

  // Mock emergency calls data
  const emergencyCalls = [
    {
      id: '1',
      emergency_type: 'medical',
      priority: 'high',
      caller_location: '123 Main St, City',
      status: 'in_progress',
      created_at: new Date(Date.now() - 180000).toISOString(),
      escalation_level: 1
    },
    {
      id: '2',
      emergency_type: 'fire',
      priority: 'critical',
      caller_location: '456 Oak Ave, Town',
      status: 'acknowledged',
      created_at: new Date(Date.now() - 300000).toISOString(),
      escalation_level: 2
    },
    {
      id: '3',
      emergency_type: 'police',
      priority: 'high',
      caller_location: '789 Pine Rd, Village',
      status: 'pending',
      created_at: new Date(Date.now() - 120000).toISOString(),
      escalation_level: 1
    }
  ];

  // Mock team members data
  const teamMembers = [
    {
      id: '1',
      name: 'Dr. Sarah Smith',
      role: 'Medical Specialist',
      status: 'active',
      current_calls: 1,
      total_calls_handled: 45,
      avg_response_time: 12,
      rating: 4.8,
      skills: ['medical', 'emergency', 'trauma']
    },
    {
      id: '2',
      name: 'John Doe',
      role: 'Firefighter',
      status: 'busy',
      current_calls: 2,
      total_calls_handled: 67,
      avg_response_time: 8,
      rating: 4.6,
      skills: ['fire', 'rescue', 'hazmat']
    },
    {
      id: '3',
      name: 'Officer Mike Johnson',
      role: 'Police Officer',
      status: 'active',
      current_calls: 0,
      total_calls_handled: 89,
      avg_response_time: 15,
      rating: 4.7,
      skills: ['police', 'investigation', 'crisis']
    },
    {
      id: '4',
      name: 'Emily Chen',
      role: 'Emergency Dispatcher',
      status: 'on_break',
      current_calls: 0,
      total_calls_handled: 156,
      avg_response_time: 6,
      rating: 4.9,
      skills: ['dispatch', 'communication', 'coordination']
    }
  ];

  // Analytics metrics
  const analyticsMetrics = [
    {
      title: 'Total Calls Today',
      value: '247',
      change: 12,
      icon: <Phone className="w-6 h-6 text-blue-600" />,
      color: 'bg-blue-100'
    },
    {
      title: 'Active Emergencies',
      value: '8',
      change: -5,
      icon: <AlertTriangle className="w-6 h-6 text-red-600" />,
      color: 'bg-red-100'
    },
    {
      title: 'Available Team Members',
      value: '19',
      change: 3,
      icon: <Users className="w-6 h-6 text-green-600" />,
      color: 'bg-green-100'
    },
    {
      title: 'Avg Response Time',
      value: '15s',
      change: -8,
      icon: <Clock className="w-6 h-6 text-purple-600" />,
      color: 'bg-purple-100'
    },
    {
      title: 'Call Completion Rate',
      value: '94%',
      change: 2,
      icon: <TrendingUp className="w-6 h-6 text-green-600" />,
      color: 'bg-green-100'
    },
    {
      title: 'Team Efficiency',
      value: '87%',
      change: 5,
      icon: <Activity className="w-6 h-6 text-orange-600" />,
      color: 'bg-orange-100'
    }
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'teams':
        return (
          <div className="space-y-8">
            {/* Teams Section */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Response Teams</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {teams.map((team) => (
                  <TeamCard key={team.id} team={team} />
                ))}
              </div>
            </div>

            {/* Team Members Section */}
            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-6">Team Members</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {teamMembers.map((member) => (
                  <TeamMemberCard key={member.id} member={member} />
                ))}
              </div>
            </div>
          </div>
        );

      case 'notifications':
        return (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Notifications</h2>
              <div className="flex gap-3">
                <button className="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors">
                  Mark All Read
                </button>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                  Settings
                </button>
              </div>
            </div>
            
            <div className="space-y-4">
              {notifications.map((notification) => (
                <NotificationCard key={notification.id} notification={notification} />
              ))}
            </div>
          </div>
        );

      case 'analytics':
        return (
          <div className="space-y-8">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h2>
              <div className="flex gap-3">
                <select className="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg">
                  <option>Last 7 Days</option>
                  <option>Last 30 Days</option>
                  <option>Last 3 Months</option>
                </select>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                  Export Report
                </button>
              </div>
            </div>
            
            {/* Analytics Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
              {analyticsMetrics.map((metric, index) => (
                <AnalyticsCard key={index} metric={metric} />
              ))}
            </div>

            {/* Emergency Calls */}
            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-6">Active Emergency Calls</h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {emergencyCalls.map((emergency) => (
                  <EmergencyCallCard key={emergency.id} emergency={emergency} />
                ))}
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Professional White Cards
          </h1>
          <p className="text-gray-600">
            Clean white content cards for teams, notifications, and analytics
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="border-b border-gray-200 mb-8">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'teams', label: 'Teams & Members', icon: <Users className="w-4 h-4" /> },
              { id: 'notifications', label: 'Notifications', icon: <Bell className="w-4 h-4" /> },
              { id: 'analytics', label: 'Analytics', icon: <BarChart3 className="w-4 h-4" /> }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } transition-colors`}
              >
                {tab.icon}
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        {renderContent()}
      </div>
    </div>
  );
}

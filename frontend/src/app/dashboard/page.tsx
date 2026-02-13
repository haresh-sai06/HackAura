'use client';

import { useState, useEffect } from 'react';
import { BarChart3, Phone, Users } from 'lucide-react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Navigation } from '@/components/layout/Navigation';
import { OverviewSection } from '@/components/dashboard/OverviewSection';
import { CallsSection } from '@/components/dashboard/CallsSection';
import { AnalyticsSection } from '@/components/dashboard/AnalyticsSection';
import { ClientOnly } from '@/components/ui/client-only';
import { useEmergencyStore } from '@/store/emergencyStore';
import { EmergencyCall, CallAnalytics as CallAnalyticsType, CallStatus, EmergencyType, Severity } from '@/types/emergency';
import { emergencyApi } from '@/utils/api';
import { useWebSocket } from '@/utils/websocket';

export default function Dashboard() {
  const [selectedView, setSelectedView] = useState<'overview' | 'calls' | 'analytics'>('overview');
  const [analytics, setAnalytics] = useState<CallAnalyticsType | null>(null);
  
  const {
    calls,
    selectedCall,
    setCalls,
    setSelectedCall,
    addCall,
    updateCall,
    setLoading,
    setError,
  } = useEmergencyStore();

  const { connect, disconnect, onNewCall, onCallUpdate } = useWebSocket();

  // Navigation items
  const navigationItems = [
    {
      id: 'overview' as const,
      name: 'Overview',
      href: '/dashboard',
      icon: BarChart3,
      current: selectedView === 'overview',
    },
    {
      id: 'calls' as const,
      name: 'Emergency Calls',
      href: '/calls',
      icon: Phone,
      current: selectedView === 'calls',
      badge: calls.filter(call => 
        call.status === CallStatus.PENDING || call.status === CallStatus.IN_PROGRESS
      ).length,
    },
    {
      id: 'analytics' as const,
      name: 'Analytics',
      href: '/analytics',
      icon: BarChart3,
      current: selectedView === 'analytics',
    },
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // Use mock data for development when backend isn't available
        try {
          const [callsData, analyticsData] = await Promise.all([
            emergencyApi.getCalls(),
            emergencyApi.getAnalytics(),
          ]);
          setCalls(callsData);
          setAnalytics(analyticsData);
        } catch (networkError) {
          console.warn('Backend not available, using mock data:', networkError);
          // Use mock data for development
          const mockCalls: EmergencyCall[] = [
            {
              id: '1',
              callerName: 'John Doe',
              phoneNumber: '+1234567890',
              location: {
                address: '123 Main St, City, State',
                latitude: 40.7128,
                longitude: -74.0060,
              },
              emergencyType: 'medical' as any,
              severity: 'high' as any,
              status: 'pending' as any,
              description: 'Patient experiencing chest pain and difficulty breathing',
              timestamp: new Date(),
              assignedUnit: undefined,
              notes: [],
            },
            {
              id: '2',
              callerName: 'Jane Smith',
              phoneNumber: '+0987654321',
              location: {
                address: '456 Oak Ave, City, State',
                latitude: 40.7580,
                longitude: -73.9855,
              },
              emergencyType: 'fire' as any,
              severity: 'critical' as any,
              status: 'in_progress' as any,
              description: 'Kitchen fire reported, smoke visible',
              timestamp: new Date(Date.now() - 300000),
              assignedUnit: 'UNIT-001',
              notes: ['Fire department dispatched'],
            },
          ];
          
          const mockAnalytics: CallAnalyticsType = {
            totalCalls: 2,
            callsByType: {
              medical: 1,
              fire: 1,
              police: 0,
              accident: 0,
              natural_disaster: 0,
              other: 0,
            },
            callsBySeverity: {
              low: 0,
              medium: 0,
              high: 1,
              critical: 1,
            },
            callsByStatus: {
              pending: 1,
              in_progress: 1,
              dispatched: 0,
              resolved: 0,
              cancelled: 0,
            },
            averageResponseTime: 4.2,
            resolvedCalls: 0,
            pendingCalls: 1,
          };
          
          setCalls(mockCalls);
          setAnalytics(mockAnalytics);
        }
      } catch (error) {
        console.error('Failed to fetch data:', error);
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Setup WebSocket connection
    const token = localStorage.getItem('auth_token');
    if (token) {
      connect(token);
      
      // Listen for real-time updates
      onNewCall((call: EmergencyCall) => {
        addCall(call);
      });
      
      onCallUpdate((call: EmergencyCall) => {
        updateCall(call.id, call);
      });
    }

    return () => {
      disconnect();
    };
  }, []);

  const handleSelectCall = (call: EmergencyCall) => {
    setSelectedCall(call);
    setSelectedView('calls');
  };

  const handleAssignCall = async (callId: string) => {
    try {
      const updatedCall = await emergencyApi.updateCall(callId, {
        status: CallStatus.DISPATCHED,
        assignedUnit: 'UNIT-001',
      });
      updateCall(callId, updatedCall);
    } catch (error) {
      console.error('Failed to assign call:', error);
      setError('Failed to assign unit to call');
    }
  };

  const handleRefresh = async () => {
    console.log('Refresh button clicked');
    try {
      setLoading(true);
      console.log('Fetching fresh data...');
      
      // Try to fetch from backend first
      try {
        const [callsData, analyticsData] = await Promise.all([
          emergencyApi.getCalls(),
          emergencyApi.getAnalytics(),
        ]);
        console.log('Data fetched successfully from backend:', { callsData, analyticsData });
        setCalls(callsData);
        setAnalytics(analyticsData);
        setError(null);
      } catch (networkError) {
        console.warn('Backend not available, using mock data for refresh:', networkError);
        
        // Show a brief notification about using mock data
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-amber-100 dark:bg-amber-900 text-amber-800 dark:text-amber-200 px-4 py-2 rounded-lg shadow-lg z-50 border border-amber-300 dark:border-amber-700';
        notification.innerHTML = `
          <div class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
            </svg>
            <span class="text-sm font-medium">Using demo data - Backend not available</span>
          </div>
        `;
        document.body.appendChild(notification);
        
        // Remove notification after 3 seconds
        setTimeout(() => {
          if (document.body.contains(notification)) {
            document.body.removeChild(notification);
          }
        }, 3000);
        
        // Use mock data for development when backend isn't available
        const mockCalls: EmergencyCall[] = [
          {
            id: Date.now().toString(),
            callerName: 'Refreshed User',
            phoneNumber: '+1234567890',
            location: {
              address: '123 Refreshed St, City, State',
              latitude: 40.7128,
              longitude: -74.0060,
            },
            emergencyType: EmergencyType.MEDICAL,
            severity: Severity.HIGH,
            status: CallStatus.PENDING,
            description: 'Refreshed data - Patient experiencing chest pain and difficulty breathing',
            timestamp: new Date(),
            assignedUnit: undefined,
            notes: [],
          },
          ...calls.slice(0, 4).map((call, index) => ({
            ...call,
            timestamp: new Date(Date.now() - index * 60000), // Different timestamps
          })),
        ];
        
        const mockAnalytics = {
          totalCalls: mockCalls.length,
          activeCalls: mockCalls.filter(call => 
            call.status === CallStatus.PENDING || call.status === CallStatus.IN_PROGRESS
          ).length,
          resolvedCalls: mockCalls.filter(call => call.status === CallStatus.RESOLVED).length,
          pendingCalls: mockCalls.filter(call => call.status === CallStatus.PENDING).length,
          averageResponseTime: 4.2,
          callsByType: {
            [EmergencyType.MEDICAL]: mockCalls.filter(call => call.emergencyType === EmergencyType.MEDICAL).length,
            [EmergencyType.FIRE]: mockCalls.filter(call => call.emergencyType === EmergencyType.FIRE).length,
            [EmergencyType.POLICE]: mockCalls.filter(call => call.emergencyType === EmergencyType.POLICE).length,
            [EmergencyType.ACCIDENT]: mockCalls.filter(call => call.emergencyType === EmergencyType.ACCIDENT).length,
            [EmergencyType.NATURAL_DISASTER]: mockCalls.filter(call => call.emergencyType === EmergencyType.NATURAL_DISASTER).length,
            [EmergencyType.OTHER]: mockCalls.filter(call => call.emergencyType === EmergencyType.OTHER).length,
          },
          callsBySeverity: {
            [Severity.LOW]: mockCalls.filter(call => call.severity === Severity.LOW).length,
            [Severity.MEDIUM]: mockCalls.filter(call => call.severity === Severity.MEDIUM).length,
            [Severity.HIGH]: mockCalls.filter(call => call.severity === Severity.HIGH).length,
            [Severity.CRITICAL]: mockCalls.filter(call => call.severity === Severity.CRITICAL).length,
          },
          callsByStatus: {
            [CallStatus.PENDING]: mockCalls.filter(call => call.status === CallStatus.PENDING).length,
            [CallStatus.IN_PROGRESS]: mockCalls.filter(call => call.status === CallStatus.IN_PROGRESS).length,
            [CallStatus.DISPATCHED]: mockCalls.filter(call => call.status === CallStatus.DISPATCHED).length,
            [CallStatus.RESOLVED]: mockCalls.filter(call => call.status === CallStatus.RESOLVED).length,
            [CallStatus.CANCELLED]: mockCalls.filter(call => call.status === CallStatus.CANCELLED).length,
          },
        };
        
        setCalls(mockCalls);
        setAnalytics(mockAnalytics);
        setError(null); // Clear any previous errors
      }
    } catch (error) {
      console.error('Unexpected error during refresh:', error);
      setError('Failed to refresh dashboard data');
    } finally {
      setLoading(false);
      console.log('Refresh completed');
    }
  };

  const renderMainContent = () => {
    switch (selectedView) {
      case 'overview':
        return (
          <OverviewSection
            calls={calls}
            onSelectCall={handleSelectCall}
            onAssignCall={handleAssignCall}
            onRefresh={handleRefresh}
          />
        );
      
      case 'calls':
        return (
          <CallsSection
            calls={calls}
            selectedCall={selectedCall}
            onSelectCall={setSelectedCall}
            onAssignCall={handleAssignCall}
            onRefresh={handleRefresh}
            onUpdateCall={updateCall}
          />
        );
      
      case 'analytics':
        return <AnalyticsSection analytics={analytics} />;
      
      default:
        return null;
    }
  };

  return (
    <ClientOnly fallback={<div className="flex h-screen items-center justify-center">Loading...</div>}>
      <DashboardLayout>
        {/* Navigation */}
        <Navigation
          items={navigationItems}
          currentView={selectedView}
          onViewChange={(view: 'overview' | 'calls' | 'analytics') => setSelectedView(view)}
        />

        {/* Main Content */}
        {renderMainContent()}
      </DashboardLayout>
    </ClientOnly>
  );
}

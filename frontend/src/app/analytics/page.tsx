'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { BarChart3, TrendingUp, Users, Clock, AlertTriangle, RefreshCw, Wifi, WifiOff } from 'lucide-react';
import { CallAnalytics } from '@/types/emergency';
import { useRealTimeAnalytics } from '@/hooks/useRealTimeAnalytics';

export default function AnalyticsPage() {
  const [selectedPeriod, setSelectedPeriod] = useState('7d');

  // Use real-time analytics hook
  const { 
    analytics, 
    loading, 
    error, 
    lastUpdated, 
    isConnected, 
    refresh 
  } = useRealTimeAnalytics(30000); // Update every 30 seconds

  // Get actual connection status (isConnected is a function)
  const connectionStatus = isConnected();

  // Mock data fallback
  const mockAnalytics: CallAnalytics = {
    totalCalls: 156,
    callsByStatus: {
      pending: 12,
      in_progress: 8,
      dispatched: 24,
      resolved: 144,
      cancelled: 0,
    },
    callsByType: {
      medical: 45,
      fire: 28,
      police: 67,
      accident: 12,
      natural_disaster: 3,
      other: 1,
    },
    callsBySeverity: {
      low: 23,
      medium: 67,
      high: 54,
      critical: 12,
    },
    averageResponseTime: 4.2,
    resolvedCalls: 144,
    pendingCalls: 12,
  };

  const currentAnalytics = analytics || mockAnalytics;
  
  // Debug: Show which data source is being used
  console.log('Using analytics data:', analytics ? 'REAL DATA' : 'MOCK DATA');
  console.log('Current analytics data:', currentAnalytics);
  console.log('WebSocket connected:', connectionStatus);
  console.log('Last updated:', lastUpdated);

  // Additional mock data for charts (fallback)
  const mockChartData = {
    callsByHour: [
      { hour: 0, calls: 0 },
      { hour: 1, calls: 0 },
      { hour: 2, calls: 0 },
      { hour: 3, calls: 0 },
      { hour: 4, calls: 0 },
      { hour: 5, calls: 0 },
      { hour: 6, calls: 0 },
      { hour: 7, calls: 0 },
      { hour: 8, calls: 0 },
      { hour: 9, calls: 0 },
      { hour: 10, calls: 0 },
      { hour: 11, calls: 0 },
      { hour: 12, calls: 0 },
      { hour: 13, calls: 0 },
      { hour: 14, calls: 0 },
      { hour: 15, calls: 0 },
      { hour: 16, calls: 0 },
      { hour: 17, calls: 0 },
      { hour: 18, calls: 0 },
      { hour: 19, calls: 0 },
      { hour: 20, calls: 0 },
      { hour: 21, calls: 0 },
      { hour: 22, calls: 0 },
      { hour: 23, calls: 0 },
    ],
    callsByDay: [
      { day: 'Mon', calls: 0 },
      { day: 'Tue', calls: 0 },
      { day: 'Wed', calls: 0 },
      { day: 'Thu', calls: 0 },
      { day: 'Fri', calls: 0 },
      { day: 'Sat', calls: 0 },
      { day: 'Sun', calls: 0 },
    ],
  };

  // Use real-time chart data if available, otherwise use mock data
  const chartData = analytics ? {
    callsByHour: currentAnalytics.callsByHour || mockChartData.callsByHour,
    callsByDay: currentAnalytics.callsByDay || mockChartData.callsByDay,
  } : mockChartData;

  const severityColors = {
    low: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    critical: 'bg-red-100 text-red-800',
  };

  const typeColors = {
    medical: 'bg-red-100 text-red-800',
    fire: 'bg-orange-100 text-orange-800',
    police: 'bg-blue-100 text-blue-800',
    accident: 'bg-yellow-100 text-yellow-800',
    mental_health: 'bg-purple-100 text-purple-800',
    other: 'bg-gray-100 text-gray-800',
  };

  // Handle missing type colors gracefully
  const getTypeColor = (type: string) => {
    return typeColors[type as keyof typeof typeColors] || 'bg-gray-100 text-gray-800';
  };

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        {/* Error Display */}
        {error && (
          <div className="bg-red-100 dark:bg-red-900 border border-red-300 dark:border-red-700 text-red-800 dark:text-red-200 px-4 py-3 rounded-lg">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="text-3xl font-bold text-dark dark:text-light">Analytics Dashboard</h1>
            <div className="flex items-center gap-2">
              <Badge className={analytics ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"}>
                {analytics ? "Live Data" : "Mock Data"}
              </Badge>
              <Badge className={connectionStatus ? "bg-blue-100 text-blue-800" : "bg-gray-100 text-gray-800"}>
                {connectionStatus ? <Wifi className="h-3 w-3 mr-1" /> : <WifiOff className="h-3 w-3 mr-1" />}
                {connectionStatus ? "Real-time" : "Offline"}
              </Badge>
              {lastUpdated && (
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  Last updated: {lastUpdated.toLocaleTimeString()}
                </span>
              )}
            </div>
          </div>
          <div className="flex gap-2">
            {['24h', '7d', '30d', '90d'].map((period) => (
              <button
                key={period}
                onClick={() => setSelectedPeriod(period)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  selectedPeriod === period
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                }`}
              >
                {period === '24h' ? '24 Hours' : period === '7d' ? '7 Days' : period === '30d' ? '30 Days' : '90 Days'}
              </button>
            ))}
            <button
              onClick={refresh}
              disabled={loading}
              className="px-4 py-2 rounded-lg font-medium transition-colors bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 hover:bg-blue-200 dark:hover:bg-blue-800 disabled:opacity-50"
            >
              <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="text-blue-600 dark:text-blue-300 flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Total Calls
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-dark dark:text-light">
                {loading ? '...' : currentAnalytics.totalCalls}
              </div>
              <CardDescription className="text-dark-secondary dark:text-light-secondary">
                {analytics ? 'Real-time data' : 'Sample data'}
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="text-green-600 dark:text-green-300 flex items-center gap-2">
                <Users className="h-5 w-5" />
                Active Calls
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-dark dark:text-light">
                {loading ? '...' : currentAnalytics.pendingCalls}
              </div>
              <CardDescription className="text-dark-secondary dark:text-light-secondary">
                {analytics ? 'Currently pending' : 'Sample data'}
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="text-amber-600 dark:text-amber-300 flex items-center gap-2">
                <Clock className="h-5 w-5" />
                Avg Response Time
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-dark dark:text-light">
                {loading ? '...' : currentAnalytics.averageResponseTime?.toFixed(1)} min
              </div>
              <CardDescription className="text-dark-secondary dark:text-light-secondary">
                {analytics ? 'Real-time average' : 'Sample data'}
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="text-red-600 dark:text-red-300 flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                Resolved Cases
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-dark dark:text-light">
                {loading ? '...' : currentAnalytics.resolvedCalls}
              </div>
              <CardDescription className="text-dark-secondary dark:text-light-secondary">
                {analytics ? 'Successfully handled' : 'Sample data'}
              </CardDescription>
            </CardContent>
          </Card>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Calls by Type */}
          <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="text-white">Calls by Emergency Type</CardTitle>
              <CardDescription className="text-dark-secondary dark:text-light-secondary">Distribution of emergency calls by type</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(currentAnalytics.callsByType).map(([type, count]) => (
                  <div key={type} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Badge className={`${getTypeColor(type)} px-3 py-1 text-xs font-semibold`}>
                        {type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ width: `${(count / currentAnalytics.totalCalls) * 100}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100 w-8 text-right">
                        {count}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Calls by Severity */}
          <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="text-white">Calls by Severity</CardTitle>
              <CardDescription className="text-dark-secondary dark:text-light-secondary">Distribution of emergency calls by severity level</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(currentAnalytics.callsBySeverity).map(([severity, count]) => (
                  <div key={severity} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Badge className={`${severityColors[severity as keyof typeof severityColors]} px-3 py-1 text-xs font-semibold`}>
                        {severity.toUpperCase()}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-green-600 h-2 rounded-full"
                          style={{ width: `${(count / currentAnalytics.totalCalls) * 100}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100 w-8 text-right">
                        {count}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Hourly Distribution */}
        <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle className="text-white">Hourly Call Distribution</CardTitle>
            <CardDescription className="text-dark-secondary dark:text-light-secondary">Number of calls by hour of day</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-end justify-between gap-1">
              {chartData.callsByHour.map((hour: any, index: number) => (
                <div
                  key={hour.hour}
                  className="flex-1 bg-blue-600 rounded-t hover:bg-blue-700 transition-all duration-300 ease-out relative group cursor-pointer transform hover:scale-y-105"
                  style={{ height: `${hour.calls > 0 ? (hour.calls / Math.max(...chartData.callsByHour.map((h: any) => h.calls), 1)) * 100 : 2}%` }}
                >
                  <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                    {hour.hour}:00 - {hour.calls} calls
                  </div>
                </div>
              ))}
            </div>
            <div className="flex justify-between mt-2 text-xs text-dark-secondary dark:text-light-secondary">
              <span>00:00</span>
              <span>06:00</span>
              <span>12:00</span>
              <span>18:00</span>
              <span>23:00</span>
            </div>
          </CardContent>
        </Card>

        {/* Weekly Distribution */}
        <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle className="text-white">Weekly Call Distribution</CardTitle>
            <CardDescription className="text-dark-secondary dark:text-light-secondary">Number of calls by day of week</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-48 flex items-end justify-between gap-2">
              {chartData.callsByDay.map((day: any, index: number) => (
                <div
                  key={day.day}
                  className="flex-1 flex flex-col items-center gap-2"
                >
                  <div
                    className="w-full bg-green-600 rounded-t hover:bg-green-700 transition-all duration-300 ease-out relative group cursor-pointer transform hover:scale-y-105"
                    style={{ height: `${day.calls > 0 ? (day.calls / Math.max(...chartData.callsByDay.map((d: any) => d.calls), 1)) * 100 : 2}%` }}
                  >
                    <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                      {day.day} - {day.calls} calls
                    </div>
                  </div>
                  <span className="text-xs text-dark-secondary dark:text-light-secondary font-medium">
                    {day.day}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}

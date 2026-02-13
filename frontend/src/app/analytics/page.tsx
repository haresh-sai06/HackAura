'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { BarChart3, TrendingUp, Users, Clock, AlertTriangle } from 'lucide-react';

export default function AnalyticsPage() {
  const [selectedPeriod, setSelectedPeriod] = useState('7d');

  // Mock analytics data
  const analytics = {
    totalCalls: 156,
    activeCalls: 12,
    resolvedCalls: 144,
    averageResponseTime: 4.2,
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
    callsByHour: [
      { hour: 0, calls: 3 },
      { hour: 1, calls: 2 },
      { hour: 2, calls: 1 },
      { hour: 3, calls: 2 },
      { hour: 4, calls: 4 },
      { hour: 5, calls: 6 },
      { hour: 6, calls: 8 },
      { hour: 7, calls: 12 },
      { hour: 8, calls: 15 },
      { hour: 9, calls: 14 },
      { hour: 10, calls: 13 },
      { hour: 11, calls: 11 },
      { hour: 12, calls: 9 },
      { hour: 13, calls: 10 },
      { hour: 14, calls: 12 },
      { hour: 15, calls: 14 },
      { hour: 16, calls: 16 },
      { hour: 17, calls: 13 },
      { hour: 18, calls: 11 },
      { hour: 19, calls: 9 },
      { hour: 20, calls: 7 },
      { hour: 21, calls: 5 },
      { hour: 22, calls: 4 },
      { hour: 23, calls: 3 },
    ],
    callsByDay: [
      { day: 'Mon', calls: 18 },
      { day: 'Tue', calls: 24 },
      { day: 'Wed', calls: 22 },
      { day: 'Thu', calls: 31 },
      { day: 'Fri', calls: 28 },
      { day: 'Sat', calls: 19 },
      { day: 'Sun', calls: 14 },
    ],
  };

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
    natural_disaster: 'bg-purple-100 text-purple-800',
    other: 'bg-gray-100 text-gray-800',
  };

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Analytics Dashboard</h1>
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
              <div className="text-3xl font-bold text-gray-900 dark:text-gray-100">{analytics.totalCalls}</div>
              <CardDescription className="text-gray-600 dark:text-gray-400">
                +12% from last period
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
              <div className="text-3xl font-bold text-gray-900 dark:text-gray-100">{analytics.activeCalls}</div>
              <CardDescription className="text-gray-600 dark:text-gray-400">
                Currently in progress
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
              <div className="text-3xl font-bold text-gray-900 dark:text-gray-100">{analytics.averageResponseTime} min</div>
              <CardDescription className="text-gray-600 dark:text-gray-400">
                -0.3 from average
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="text-red-600 dark:text-red-300 flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                Critical Cases
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900 dark:text-gray-100">{analytics.callsBySeverity.critical}</div>
              <CardDescription className="text-gray-600 dark:text-gray-400">
                Requires immediate attention
              </CardDescription>
            </CardContent>
          </Card>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Calls by Type */}
          <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="text-gray-900 dark:text-gray-100">Calls by Emergency Type</CardTitle>
              <CardDescription className="text-gray-600 dark:text-gray-400">Distribution of emergency calls by type</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(analytics.callsByType).map(([type, count]) => (
                  <div key={type} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Badge className={`${typeColors[type as keyof typeof typeColors]} px-3 py-1 text-xs font-semibold`}>
                        {type.replace('_', ' ').toUpperCase()}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ width: `${(count / analytics.totalCalls) * 100}%` }}
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
              <CardTitle className="text-gray-900 dark:text-gray-100">Calls by Severity</CardTitle>
              <CardDescription className="text-gray-600 dark:text-gray-400">Distribution of emergency calls by severity level</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(analytics.callsBySeverity).map(([severity, count]) => (
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
                          style={{ width: `${(count / analytics.totalCalls) * 100}%` }}
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
            <CardTitle className="text-gray-900 dark:text-gray-100">Hourly Call Distribution</CardTitle>
            <CardDescription className="text-gray-600 dark:text-gray-400">Number of calls by hour of day</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-end justify-between gap-1">
              {analytics.callsByHour.map((hour) => (
                <div
                  key={hour.hour}
                  className="flex-1 bg-blue-600 rounded-t hover:bg-blue-700 transition-all duration-300 ease-out relative group cursor-pointer transform hover:scale-y-105"
                  style={{ height: `${(hour.calls / 20) * 100}%` }}
                >
                  <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                    {hour.hour}:00 - {hour.calls} calls
                  </div>
                </div>
              ))}
            </div>
            <div className="flex justify-between mt-2 text-xs text-gray-600 dark:text-gray-400">
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
            <CardTitle className="text-gray-900 dark:text-gray-100">Weekly Call Distribution</CardTitle>
            <CardDescription className="text-gray-600 dark:text-gray-400">Number of calls by day of week</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-48 flex items-end justify-between gap-2">
              {analytics.callsByDay.map((day) => (
                <div
                  key={day.day}
                  className="flex-1 flex flex-col items-center gap-2"
                >
                  <div
                    className="w-full bg-green-600 rounded-t hover:bg-green-700 transition-all duration-300 ease-out relative group cursor-pointer transform hover:scale-y-105"
                    style={{ height: `${(day.calls / 35) * 100}%` }}
                  >
                    <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                      {day.day} - {day.calls} calls
                    </div>
                  </div>
                  <span className="text-xs text-gray-600 dark:text-gray-400 font-medium">
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

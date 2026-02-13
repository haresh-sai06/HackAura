'use client';

import { useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  Area,
  AreaChart,
} from 'recharts';
import type { CallAnalytics } from '@/types/emergency';
import { EmergencyType, Severity, CallStatus } from '@/types/emergency';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, TrendingDown, Clock, Users, AlertTriangle } from 'lucide-react';

interface CallAnalyticsProps {
  analytics: CallAnalytics;
  className?: string;
}

const COLORS = {
  [EmergencyType.MEDICAL]: '#ef4444',
  [EmergencyType.FIRE]: '#f97316',
  [EmergencyType.POLICE]: '#3b82f6',
  [EmergencyType.ACCIDENT]: '#eab308',
  [EmergencyType.NATURAL_DISASTER]: '#a855f7',
  [EmergencyType.OTHER]: '#6b7280',
};

const SEVERITY_COLORS = {
  [Severity.LOW]: '#22c55e',
  [Severity.MEDIUM]: '#eab308',
  [Severity.HIGH]: '#f97316',
  [Severity.CRITICAL]: '#ef4444',
};

const STATUS_COLORS = {
  [CallStatus.PENDING]: '#6b7280',
  [CallStatus.IN_PROGRESS]: '#3b82f6',
  [CallStatus.DISPATCHED]: '#a855f7',
  [CallStatus.RESOLVED]: '#22c55e',
  [CallStatus.CANCELLED]: '#ef4444',
};

export function CallAnalytics({ analytics, className }: CallAnalyticsProps) {
  const [timeRange, setTimeRange] = useState('7d');

  // Prepare data for charts
  const emergencyTypeData = Object.entries(analytics.callsByType).map(([type, count]) => ({
    name: type.replace('_', ' ').toUpperCase(),
    value: count,
    fill: COLORS[type as EmergencyType],
  }));

  const severityData = Object.entries(analytics.callsBySeverity).map(([severity, count]) => ({
    name: severity.toUpperCase(),
    value: count,
    fill: SEVERITY_COLORS[severity as Severity],
  }));

  const statusData = Object.entries(analytics.callsByStatus).map(([status, count]) => ({
    name: status.replace('_', ' ').toUpperCase(),
    value: count,
    fill: STATUS_COLORS[status as CallStatus],
  }));

  // Mock time series data for response times
  const responseTimeData = [
    { time: '00:00', responseTime: 4.2, calls: 12 },
    { time: '04:00', responseTime: 5.1, calls: 8 },
    { time: '08:00', responseTime: 3.8, calls: 25 },
    { time: '12:00', responseTime: 4.5, calls: 18 },
    { time: '16:00', responseTime: 3.9, calls: 22 },
    { time: '20:00', responseTime: 4.7, calls: 15 },
  ];

  const resolutionRate = analytics.totalCalls > 0 
    ? Math.round((analytics.resolvedCalls / analytics.totalCalls) * 100)
    : 0;

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Call Analytics</h2>
          <p className="text-muted-foreground">Emergency response metrics and trends</p>
        </div>
        <Select value={timeRange} onValueChange={setTimeRange}>
          <SelectTrigger className="w-32">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="24h">Last 24h</SelectItem>
            <SelectItem value="7d">Last 7 days</SelectItem>
            <SelectItem value="30d">Last 30 days</SelectItem>
            <SelectItem value="90d">Last 90 days</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Calls</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.totalCalls}</div>
            <p className="text-xs text-muted-foreground">
              {analytics.pendingCalls} pending
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Response Time</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.averageResponseTime.toFixed(1)} min</div>
            <p className="text-xs text-muted-foreground">
              <TrendingDown className="inline h-3 w-3" />
              -0.3 from average
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Resolution Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{resolutionRate}%</div>
            <p className="text-xs text-muted-foreground">
              {analytics.resolvedCalls} resolved
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical Cases</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.callsBySeverity[Severity.CRITICAL]}</div>
            <p className="text-xs text-muted-foreground">
              Requires immediate attention
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Emergency Types Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Emergency Types Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={emergencyTypeData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {emergencyTypeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Severity Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Severity Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={severityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8">
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Call Status */}
        <Card>
          <CardHeader>
            <CardTitle>Call Status Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={statusData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8">
                  {statusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Response Time Trends */}
        <Card>
          <CardHeader>
            <CardTitle>Response Time Trends</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={responseTimeData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="responseTime"
                  stroke="#3b82f6"
                  fill="#3b82f6"
                  fillOpacity={0.3}
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Stats */}
      <Card>
        <CardHeader>
          <CardTitle>Detailed Statistics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h4 className="font-medium mb-3">By Emergency Type</h4>
              <div className="space-y-2">
                {Object.entries(analytics.callsByType).map(([type, count]) => (
                  <div key={type} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: COLORS[type as EmergencyType] }}
                      />
                      <span className="text-sm">{type.replace('_', ' ').toUpperCase()}</span>
                    </div>
                    <Badge variant="secondary">{count}</Badge>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-medium mb-3">By Severity</h4>
              <div className="space-y-2">
                {Object.entries(analytics.callsBySeverity).map(([severity, count]) => (
                  <div key={severity} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: SEVERITY_COLORS[severity as Severity] }}
                      />
                      <span className="text-sm">{severity.toUpperCase()}</span>
                    </div>
                    <Badge variant="secondary">{count}</Badge>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-medium mb-3">By Status</h4>
              <div className="space-y-2">
                {Object.entries(analytics.callsByStatus).map(([status, count]) => (
                  <div key={status} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: STATUS_COLORS[status as CallStatus] }}
                      />
                      <span className="text-sm">{status.replace('_', ' ').toUpperCase()}</span>
                    </div>
                    <Badge variant="secondary">{count}</Badge>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

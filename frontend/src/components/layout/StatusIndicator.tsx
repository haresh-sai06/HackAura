'use client';

import { Phone, Clock, Users, AlertTriangle } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface StatusIndicatorProps {
  className?: string;
}

export function StatusIndicator({ className }: StatusIndicatorProps) {
  const stats = [
    {
      title: 'Active Calls',
      value: '12',
      change: '+2 from last hour',
      icon: Phone,
      color: 'text-blue-600 dark:text-blue-300',
      bgColor: 'bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900 dark:to-blue-800',
      iconBg: 'bg-blue-500 dark:bg-blue-600',
      borderColor: 'border-blue-200 dark:border-blue-700',
    },
    {
      title: 'Avg Response Time',
      value: '4.2 min',
      change: '-0.3 from average',
      icon: Clock,
      color: 'text-green-600 dark:text-green-300',
      bgColor: 'bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900 dark:to-green-800',
      iconBg: 'bg-green-500 dark:bg-green-600',
      borderColor: 'border-green-200 dark:border-green-700',
    },
    {
      title: 'Available Units',
      value: '8',
      change: '3 units busy',
      icon: Users,
      color: 'text-amber-600 dark:text-amber-300',
      bgColor: 'bg-gradient-to-br from-amber-50 to-amber-100 dark:from-amber-900 dark:to-amber-800',
      iconBg: 'bg-amber-500 dark:bg-amber-600',
      borderColor: 'border-amber-200 dark:border-amber-700',
    },
    {
      title: 'Critical Cases',
      value: '2',
      change: 'Requires immediate attention',
      icon: AlertTriangle,
      color: 'text-red-600 dark:text-red-300',
      bgColor: 'bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900 dark:to-red-800',
      iconBg: 'bg-red-500 dark:bg-red-600',
      borderColor: 'border-red-200 dark:border-red-700',
    },
  ];

  return (
    <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 ${className}`}>
      {stats.map((stat) => {
        const Icon = stat.icon;
        return (
          <Card key={stat.title} className={`p-6 ${stat.bgColor} ${stat.borderColor} border shadow-lg hover:shadow-xl transition-all duration-300 relative overflow-hidden group`}>
            {/* Subtle pattern overlay */}
            <div className="absolute inset-0 bg-white dark:bg-black opacity-0 group-hover:opacity-5 transition-opacity"></div>
            
            <div className="flex items-start justify-between relative z-10">
              <div className="flex-1">
                <p className={`text-sm font-semibold ${stat.color} uppercase tracking-wide mb-2`}>
                  {stat.title}
                </p>
                <p className={`text-3xl font-bold ${stat.color === 'text-red-600 dark:text-red-300' ? 'text-red-700 dark:text-red-200' : stat.color} mb-1`}>
                  {stat.value}
                </p>
                <div className="flex items-center gap-2">
                  <div className={`h-1 w-8 ${stat.iconBg} rounded-full`}></div>
                  <p className={`text-xs ${stat.color} font-medium`}>
                    {stat.change}
                  </p>
                </div>
              </div>
              <div className={`p-4 rounded-2xl ${stat.iconBg} shadow-lg transform group-hover:scale-110 transition-transform duration-300`}>
                <Icon className="h-6 w-6 text-white" />
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
}

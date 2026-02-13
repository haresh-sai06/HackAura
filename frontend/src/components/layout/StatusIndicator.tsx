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
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      title: 'Avg Response Time',
      value: '4.2 min',
      change: '-0.3 from average',
      icon: Clock,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      title: 'Available Units',
      value: '8',
      change: '3 units busy',
      icon: Users,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
    },
    {
      title: 'Critical Cases',
      value: '2',
      change: 'Requires immediate attention',
      icon: AlertTriangle,
      color: 'text-red-600',
      bgColor: 'bg-red-50',
    },
  ];

  return (
    <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 ${className}`}>
      {stats.map((stat) => {
        const Icon = stat.icon;
        return (
          <Card key={stat.title} className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  {stat.title}
                </p>
                <p className="text-2xl font-bold">{stat.value}</p>
                <p className="text-xs text-muted-foreground mt-1">
                  {stat.change}
                </p>
              </div>
              <div className={`p-3 rounded-full ${stat.bgColor}`}>
                <Icon className={`h-6 w-6 ${stat.color}`} />
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
}

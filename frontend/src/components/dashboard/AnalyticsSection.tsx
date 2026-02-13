'use client';

import { CallAnalytics } from '@/components/analytics/CallAnalytics';
import type { CallAnalytics as CallAnalyticsType } from '@/types/emergency';

interface AnalyticsSectionProps {
  analytics: CallAnalyticsType | null;
  loading?: boolean;
}

export function AnalyticsSection({ analytics, loading }: AnalyticsSectionProps) {
  if (loading) {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-white mb-4">Analytics</h2>
          <p className="text-white">Emergency response metrics and trends</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="bg-muted/50 rounded-lg p-6 animate-pulse">
              <div className="h-4 bg-muted rounded w-3/4 mb-2"></div>
              <div className="h-8 bg-muted rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-white mb-4">Analytics</h2>
          <p className="text-white">Emergency response metrics and trends</p>
        </div>
        <div className="bg-muted/50 rounded-lg p-8 text-center">
          <p className="text-white">No analytics data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white mb-4">Analytics</h2>
        <p className="text-white">Emergency response metrics and trends</p>
      </div>
      <CallAnalytics analytics={analytics} />
    </div>
  );
}

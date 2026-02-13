'use client';

import { StatusIndicator } from '@/components/layout/StatusIndicator';
import { CallList } from '@/components/calls/CallList';
import { EmergencyCall } from '@/types/emergency';

interface OverviewSectionProps {
  calls: EmergencyCall[];
  onSelectCall: (call: EmergencyCall) => void;
  onAssignCall: (callId: string) => void;
  onRefresh: () => void;
  loading?: boolean;
}

export function OverviewSection({ 
  calls, 
  onSelectCall, 
  onAssignCall, 
  onRefresh, 
  loading 
}: OverviewSectionProps) {
  return (
    <div className="space-y-8 animate-slide-in">
      {/* Status Cards */}
      <div className="animate-fade-in">
        <StatusIndicator calls={calls} />
      </div>
      
      {/* Recent Calls */}
      <div className="animate-slide-in" style={{ animationDelay: '0.1s' }}>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-dark dark:text-light">Recent Emergency Calls</h2>
          <div className="text-sm text-dark-secondary dark:text-light-secondary">
            Latest {Math.min(5, calls.length)} of {calls.length} total
          </div>
        </div>
        <CallList
          calls={calls.slice(0, 5)}
          onSelectCall={onSelectCall}
          onAssignCall={onAssignCall}
          onRefresh={onRefresh}
          loading={loading}
        />
      </div>
    </div>
  );
}

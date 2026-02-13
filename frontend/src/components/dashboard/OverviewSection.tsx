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
    <div className="space-y-6">
      {/* Status Cards */}
      <StatusIndicator calls={calls} />
      
      {/* Recent Calls */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Recent Emergency Calls</h2>
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

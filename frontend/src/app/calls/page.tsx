'use client';

import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { CallList } from '@/components/calls/CallList';
import { EmergencyCall } from '@/types/emergency';
import { emergencyApi } from '@/utils/api';
import { CallStatus, EmergencyType, Severity } from '@/types/emergency';

export default function EmergencyCallsPage() {
  const [calls, setCalls] = useState<EmergencyCall[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedCall, setSelectedCall] = useState<EmergencyCall | null>(null);

  // Fetch calls from backend
  const fetchCalls = async () => {
    setLoading(true);
    try {
      const callsData = await emergencyApi.getCalls();
      setCalls(callsData);
    } catch (error) {
      console.error('Failed to fetch calls:', error);
      // Fallback to empty array if backend is not available
      setCalls([]);
    } finally {
      setLoading(false);
    }
  };

  // Initial fetch
  useEffect(() => {
    fetchCalls();
  }, []);

  const handleSelectCall = (call: EmergencyCall) => {
    setSelectedCall(call);
  };

  const handleAssignCall = async (callId: string) => {
    try {
      const updatedCall = await emergencyApi.updateCall(callId, {
        status: CallStatus.DISPATCHED,
        assignedUnit: 'UNIT-001'
      });
      setCalls(calls.map(c => c.id === callId ? updatedCall : c));
    } catch (error) {
      console.error('Failed to assign call:', error);
    }
  };

  const handleRefresh = async () => {
    await fetchCalls();
  };

  return (
    <DashboardLayout>
      <div className="p-6">
        <CallList
          calls={calls}
          loading={loading}
          onSelectCall={handleSelectCall}
          onAssignCall={handleAssignCall}
          onRefresh={handleRefresh}
        />
      </div>
    </DashboardLayout>
  );
}

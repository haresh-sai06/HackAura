'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { CallList } from '@/components/calls/CallList';
import { EmergencyCall } from '@/types/emergency';
import { useEmergencyStore } from '@/store/emergencyStore';
import { emergencyApi } from '@/utils/api';
import { CallStatus, EmergencyType, Severity } from '@/types/emergency';

// Mock data for demonstration
const mockCalls: EmergencyCall[] = [
  {
    id: '1',
    callerName: 'John Doe',
    phoneNumber: '+1234567890',
    location: {
      address: '123 Main St, New York, NY',
      latitude: 40.7128,
      longitude: -74.0060,
    },
    emergencyType: EmergencyType.MEDICAL,
    severity: Severity.HIGH,
    status: CallStatus.PENDING,
    description: 'Patient experiencing chest pain and difficulty breathing',
    timestamp: new Date(Date.now() - 300000),
    assignedUnit: undefined,
    notes: [],
  },
  {
    id: '2',
    callerName: 'Jane Smith',
    phoneNumber: '+0987654321',
    location: {
      address: '456 Oak Ave, Los Angeles, CA',
      latitude: 34.0522,
      longitude: -118.2437,
    },
    emergencyType: EmergencyType.FIRE,
    severity: Severity.CRITICAL,
    status: CallStatus.IN_PROGRESS,
    description: 'Building fire on 5th floor, multiple people trapped',
    timestamp: new Date(Date.now() - 600000),
    assignedUnit: 'UNIT-001',
    notes: ['Fire department dispatched', 'Evacuation in progress'],
  },
  {
    id: '3',
    callerName: 'Mike Johnson',
    phoneNumber: '+1122334455',
    location: {
      address: '789 Pine Rd, Chicago, IL',
      latitude: 41.8781,
      longitude: -87.6298,
    },
    emergencyType: EmergencyType.POLICE,
    severity: Severity.MEDIUM,
    status: CallStatus.DISPATCHED,
    description: 'Reported burglary in progress',
    timestamp: new Date(Date.now() - 900000),
    assignedUnit: 'UNIT-002',
    notes: ['Police units en route'],
  },
  {
    id: '4',
    callerName: 'Sarah Williams',
    phoneNumber: '+5544332211',
    location: {
      address: '321 Elm St, Houston, TX',
      latitude: 29.7604,
      longitude: -95.3698,
    },
    emergencyType: EmergencyType.ACCIDENT,
    severity: Severity.LOW,
    status: CallStatus.RESOLVED,
    description: 'Minor car accident, no injuries reported',
    timestamp: new Date(Date.now() - 1200000),
    assignedUnit: 'UNIT-003',
    notes: ['Tow truck dispatched', 'Scene cleared'],
  },
  {
    id: '5',
    callerName: 'Robert Brown',
    phoneNumber: '+6677889900',
    location: {
      address: '654 Maple Dr, Phoenix, AZ',
      latitude: 33.4484,
      longitude: -112.0740,
    },
    emergencyType: EmergencyType.NATURAL_DISASTER,
    severity: Severity.HIGH,
    status: CallStatus.PENDING,
    description: 'Flash flooding reported, multiple streets affected',
    timestamp: new Date(Date.now() - 1500000),
    assignedUnit: undefined,
    notes: [],
  },
];

export default function EmergencyCallsPage() {
  const [calls, setCalls] = useState<EmergencyCall[]>(mockCalls);
  const [loading, setLoading] = useState(false);
  const [selectedCall, setSelectedCall] = useState<EmergencyCall | null>(null);

  const handleSelectCall = (call: EmergencyCall) => {
    setSelectedCall(call);
  };

  const handleAssignCall = async (callId: string) => {
    try {
      const updatedCall = { ...calls.find(c => c.id === callId)!, 
        status: CallStatus.DISPATCHED, 
        assignedUnit: 'UNIT-001' 
      };
      setCalls(calls.map(c => c.id === callId ? updatedCall : c));
    } catch (error) {
      console.error('Failed to assign call:', error);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      const newCall: EmergencyCall = {
        id: Date.now().toString(),
        callerName: 'New Emergency',
        phoneNumber: '+9998887777',
        location: {
          address: '999 Emergency St, City, State',
          latitude: 40.7128,
          longitude: -74.0060,
        },
        emergencyType: EmergencyType.MEDICAL,
        severity: Severity.HIGH,
        status: CallStatus.PENDING,
        description: 'New emergency call received',
        timestamp: new Date(),
        assignedUnit: undefined,
        notes: [],
      };
      setCalls([newCall, ...calls.slice(0, 4)]);
    } catch (error) {
      console.error('Failed to refresh calls:', error);
    } finally {
      setLoading(false);
    }
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

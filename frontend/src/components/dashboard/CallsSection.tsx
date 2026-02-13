'use client';

import { CallList } from '@/components/calls/CallList';
import { CallDetails } from '@/components/calls/CallDetails';
import { EmergencyCall } from '@/types/emergency';

interface CallsSectionProps {
  calls: EmergencyCall[];
  selectedCall: EmergencyCall | null;
  onSelectCall: (call: EmergencyCall) => void;
  onAssignCall: (callId: string) => void;
  onRefresh: () => void;
  onUpdateCall: (id: string, updates: Partial<EmergencyCall>) => void;
  loading?: boolean;
}

export function CallsSection({ 
  calls, 
  selectedCall, 
  onSelectCall, 
  onAssignCall, 
  onRefresh, 
  onUpdateCall,
  loading 
}: CallsSectionProps) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Calls List */}
      <div className="lg:col-span-2">
        <div className="mb-4">
          <h2 className="text-2xl font-bold">Emergency Calls</h2>
          <p className="text-muted-foreground">
            Manage and track all emergency calls
          </p>
        </div>
        <CallList
          calls={calls}
          onSelectCall={onSelectCall}
          onAssignCall={onAssignCall}
          onRefresh={onRefresh}
          loading={loading}
        />
      </div>
      
      {/* Call Details */}
      <div className="lg:col-span-1">
        {selectedCall ? (
          <CallDetails
            call={selectedCall}
            onUpdate={onUpdateCall}
          />
        ) : (
          <div className="bg-muted/50 rounded-lg p-8 text-center">
            <div className="text-muted-foreground">
              <svg
                className="mx-auto h-12 w-12 mb-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
                />
              </svg>
              <p className="font-medium">No call selected</p>
              <p className="text-sm mt-1">Select a call from the list to view details</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

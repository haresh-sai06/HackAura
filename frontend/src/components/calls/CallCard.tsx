'use client';

import { format } from 'date-fns';
import { Phone, MapPin, Clock, AlertTriangle } from 'lucide-react';
import { EmergencyCall, EmergencyType, Severity, CallStatus } from '@/types/emergency';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

interface CallCardProps {
  call: EmergencyCall;
  onSelect?: (call: EmergencyCall) => void;
  onAssign?: (callId: string) => void;
  className?: string;
}

const emergencyTypeColors = {
  [EmergencyType.MEDICAL]: 'bg-red-100 text-red-700 border-red-200 dark:bg-red-900 dark:text-red-200 dark:border-red-700',
  [EmergencyType.FIRE]: 'bg-orange-100 text-orange-700 border-orange-200 dark:bg-orange-900 dark:text-orange-200 dark:border-orange-700',
  [EmergencyType.POLICE]: 'bg-blue-100 text-blue-700 border-blue-200 dark:bg-blue-900 dark:text-blue-200 dark:border-blue-700',
  [EmergencyType.ACCIDENT]: 'bg-yellow-100 text-yellow-700 border-yellow-200 dark:bg-yellow-900 dark:text-yellow-200 dark:border-yellow-700',
  [EmergencyType.NATURAL_DISASTER]: 'bg-purple-100 text-purple-700 border-purple-200 dark:bg-purple-900 dark:text-purple-200 dark:border-purple-700',
  [EmergencyType.OTHER]: 'bg-gray-100 text-gray-700 border-gray-200 dark:bg-gray-900 dark:text-gray-200 dark:border-gray-700',
};

const severityColors = {
  [Severity.LOW]: 'bg-green-100 text-green-800 border-green-300 dark:bg-green-900 dark:text-green-200 dark:border-green-700',
  [Severity.MEDIUM]: 'bg-yellow-100 text-yellow-800 border-yellow-300 dark:bg-yellow-900 dark:text-yellow-200 dark:border-yellow-700',
  [Severity.HIGH]: 'bg-orange-100 text-orange-800 border-orange-300 dark:bg-orange-900 dark:text-orange-200 dark:border-orange-700',
  [Severity.CRITICAL]: 'bg-red-100 text-red-800 border-red-300 dark:bg-red-900 dark:text-red-200 dark:border-red-700 animate-pulse',
};

const statusColors = {
  [CallStatus.PENDING]: 'bg-gray-100 text-gray-800 border-gray-300 dark:bg-gray-800 dark:text-gray-200 dark:border-gray-600',
  [CallStatus.IN_PROGRESS]: 'bg-blue-100 text-blue-800 border-blue-300 dark:bg-blue-800 dark:text-blue-200 dark:border-blue-600',
  [CallStatus.DISPATCHED]: 'bg-purple-100 text-purple-800 border-purple-300 dark:bg-purple-800 dark:text-purple-200 dark:border-purple-600',
  [CallStatus.RESOLVED]: 'bg-green-100 text-green-800 border-green-300 dark:bg-green-800 dark:text-green-200 dark:border-green-600',
  [CallStatus.CANCELLED]: 'bg-red-100 text-red-800 border-red-300 dark:bg-red-800 dark:text-red-200 dark:border-red-600',
};

export function CallCard({ call, onSelect, onAssign, className }: CallCardProps) {
  const handleSelect = () => {
    onSelect?.(call);
  };

  const handleAssign = (e: React.MouseEvent) => {
    e.stopPropagation();
    onAssign?.(call.id);
  };

  return (
    <Card 
      className={`cursor-pointer hover:shadow-xl transition-all duration-300 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 ${className} group`}
      onClick={handleSelect}
    >
      <CardHeader className="pb-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                <Phone className="h-4 w-4 text-blue-600 dark:text-blue-300" />
              </div>
              <div>
                <span className="font-semibold text-gray-900 dark:text-gray-100 text-lg">{call.callerName}</span>
                <span className="text-sm text-gray-600 dark:text-gray-400 ml-2">{call.phoneNumber}</span>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-2 mb-3">
              <Badge className={`${emergencyTypeColors[call.emergencyType]} px-3 py-1 text-xs font-semibold`}>
                {call.emergencyType.replace('_', ' ').toUpperCase()}
              </Badge>
              <Badge className={`${severityColors[call.severity]} px-3 py-1 text-xs font-semibold`}>
                {call.severity.toUpperCase()}
              </Badge>
              <Badge className={`${statusColors[call.status]} px-3 py-1 text-xs font-semibold`}>
                {call.status.replace('_', ' ').toUpperCase()}
              </Badge>
            </div>
          </div>
          
          {call.severity === Severity.CRITICAL && (
            <div className="p-2 bg-red-100 dark:bg-red-900 rounded-full animate-pulse">
              <AlertTriangle className="h-5 w-5 text-red-600 dark:text-red-300" />
            </div>
          )}
        </div>
      </CardHeader>
      
      <CardContent className="pt-0">
        <div className="space-y-4">
          {/* Location */}
          <div className="flex items-start gap-3">
            <div className="p-2 bg-gray-100 dark:bg-gray-700 rounded-lg mt-1">
              <MapPin className="h-4 w-4 text-gray-600 dark:text-gray-400" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900 dark:text-gray-100">Location</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{call.location.address}</p>
            </div>
          </div>
          
          {/* Time */}
          <div className="flex items-start gap-3">
            <div className="p-2 bg-gray-100 dark:bg-gray-700 rounded-lg mt-1">
              <Clock className="h-4 w-4 text-gray-600 dark:text-gray-400" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900 dark:text-gray-100">Time</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{format(new Date(call.timestamp), 'MMM d, yyyy HH:mm')}</p>
            </div>
          </div>
          
          {/* Description */}
          {call.description && (
            <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg">
              <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-3">
                {call.description}
              </p>
            </div>
          )}
          
          {/* Actions */}
          <div className="flex items-center gap-3 pt-2">
            {call.status === CallStatus.PENDING && (
              <Button 
                size="sm" 
                onClick={handleAssign}
                className="bg-blue-600 hover:bg-blue-700 text-white font-medium"
              >
                Assign Unit
              </Button>
            )}
            {call.status === CallStatus.IN_PROGRESS && (
              <Button 
                size="sm" 
                variant="outline"
                className="border-blue-300 dark:border-blue-600 text-blue-600 dark:text-blue-300 hover:bg-blue-50 dark:hover:bg-blue-900 font-medium"
              >
                View Details
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

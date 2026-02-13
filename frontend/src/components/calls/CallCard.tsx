'use client';

import { format } from 'date-fns';
import { useState, useEffect } from 'react';
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
  [EmergencyType.MEDICAL]: 'bg-gradient-to-r from-red-50 to-red-100 text-red-700 border-red-200 dark:from-red-900/50 dark:to-red-800 dark:text-red-200 dark:border-red-700',
  [EmergencyType.FIRE]: 'bg-gradient-to-r from-orange-50 to-orange-100 text-orange-700 border-orange-200 dark:from-orange-900/50 dark:to-orange-800 dark:text-orange-200 dark:border-orange-700',
  [EmergencyType.POLICE]: 'bg-gradient-to-r from-blue-50 to-blue-100 text-blue-700 border-blue-200 dark:from-blue-900/50 dark:to-blue-800 dark:text-blue-200 dark:border-blue-700',
  [EmergencyType.ACCIDENT]: 'bg-gradient-to-r from-yellow-50 to-yellow-100 text-yellow-700 border-yellow-200 dark:from-yellow-900/50 dark:to-yellow-800 dark:text-yellow-200 dark:border-yellow-700',
  [EmergencyType.NATURAL_DISASTER]: 'bg-gradient-to-r from-purple-50 to-purple-100 text-purple-700 border-purple-200 dark:from-purple-900/50 dark:to-purple-800 dark:text-purple-200 dark:border-purple-700',
  [EmergencyType.OTHER]: 'bg-gradient-to-r from-gray-50 to-gray-100 text-gray-700 border-gray-200 dark:from-gray-900/50 dark:to-gray-800 dark:text-gray-200 dark:border-gray-700',
};

const severityColors = {
  [Severity.LOW]: 'bg-gradient-to-r from-green-50 to-green-100 text-green-800 border-green-300 dark:from-green-900/50 dark:to-green-800 dark:text-green-200 dark:border-green-700',
  [Severity.MEDIUM]: 'bg-gradient-to-r from-yellow-50 to-yellow-100 text-yellow-800 border-yellow-300 dark:from-yellow-900/50 dark:to-yellow-800 dark:text-yellow-200 dark:border-yellow-700',
  [Severity.HIGH]: 'bg-gradient-to-r from-orange-50 to-orange-100 text-orange-800 border-orange-300 dark:from-orange-900/50 dark:to-orange-800 dark:text-orange-200 dark:border-orange-700',
  [Severity.CRITICAL]: 'bg-gradient-to-r from-red-50 to-red-100 text-red-800 border-red-300 dark:from-red-900/50 dark:to-red-800 dark:text-red-200 dark:border-red-700 animate-pulse shadow-md',
};

const statusColors = {
  [CallStatus.PENDING]: 'bg-gradient-to-r from-gray-50 to-gray-100 text-gray-800 border-gray-300 dark:from-gray-800/50 dark:to-gray-700 dark:text-gray-200 dark:border-gray-600',
  [CallStatus.IN_PROGRESS]: 'bg-gradient-to-r from-blue-50 to-blue-100 text-blue-800 border-blue-300 dark:from-blue-900/50 dark:to-blue-800 dark:text-blue-200 dark:border-blue-600',
  [CallStatus.DISPATCHED]: 'bg-gradient-to-r from-purple-50 to-purple-100 text-purple-800 border-purple-300 dark:from-purple-900/50 dark:to-purple-800 dark:text-purple-200 dark:border-purple-600',
  [CallStatus.RESOLVED]: 'bg-gradient-to-r from-green-50 to-green-100 text-green-800 border-green-300 dark:from-green-900/50 dark:to-green-800 dark:text-green-200 dark:border-green-600',
  [CallStatus.CANCELLED]: 'bg-gradient-to-r from-red-50 to-red-100 text-red-800 border-red-300 dark:from-red-900/50 dark:to-red-800 dark:text-red-200 dark:border-red-600',
};

export function CallCard({ call, onSelect, onAssign, className }: CallCardProps) {
  const [formattedTime, setFormattedTime] = useState<string>('');
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    // Format the date only on the client side
    const timestamp = call.timestamp || call.created_at;
    if (timestamp) {
      const formatted = format(new Date(timestamp), 'MMM d, yyyy HH:mm');
      setFormattedTime(formatted);
    }
  }, [call.timestamp, call.created_at]);

  const handleSelect = () => {
    onSelect?.(call);
  };

  const handleAssign = (e: React.MouseEvent) => {
    e.stopPropagation();
    onAssign?.(call.id.toString());
  };

  return (
    <Card 
      className={`cursor-pointer hover:shadow-2xl transition-all duration-300 glass-effect bg-white/80 dark:bg-gray-800/80 border border-gray-200/50 dark:border-gray-700/50 hover:border-blue-300 dark:hover:border-blue-600 hover:scale-[1.02] ${className} group`}
      onClick={handleSelect}
    >
      <CardHeader className="pb-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-4 mb-4">
              <div className="p-3 bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900 dark:to-blue-800 rounded-xl shadow-md group-hover:shadow-lg transition-all duration-300 group-hover:scale-105">
                <Phone className="h-5 w-5 text-blue-600 dark:text-blue-300" />
              </div>
              <div>
                <span className="font-bold text-gray-900 dark:text-gray-100 text-xl">
                  {call.callerName || 'Unknown Caller'}
                </span>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {call.phoneNumber || call.from_number || 'Unknown Number'}
                  </span>
                </div>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-2 mb-4">
              <Badge className={`${emergencyTypeColors[call.emergencyType] || 'bg-gradient-to-r from-gray-50 to-gray-100 text-gray-700'} px-4 py-2 text-xs font-bold shadow-sm`}>
                {call.emergencyType ? call.emergencyType.replace('_', ' ').toUpperCase() : 'UNKNOWN'}
              </Badge>
              <Badge className={`${severityColors[call.severity] || 'bg-gradient-to-r from-gray-50 to-gray-100 text-gray-700'} px-4 py-2 text-xs font-bold shadow-sm`}>
                {call.severity ? call.severity.toUpperCase() : (call.severity_level || 'UNKNOWN')}
              </Badge>
              <Badge className={`${statusColors[call.status] || 'bg-gradient-to-r from-gray-50 to-gray-100 text-gray-700'} px-4 py-2 text-xs font-bold shadow-sm`}>
                {call.status ? call.status.replace('_', ' ').toUpperCase() : 'UNKNOWN'}
              </Badge>
            </div>
          </div>
          
          {(call.severity === Severity.CRITICAL || call.severity_level === 'Level 1') && (
            <div className="p-3 bg-gradient-to-br from-red-100 to-red-200 dark:from-red-900 dark:to-red-800 rounded-full animate-pulse shadow-lg group-hover:shadow-xl transition-all duration-300 group-hover:scale-110">
              <AlertTriangle className="h-6 w-6 text-red-600 dark:text-red-300" />
            </div>
          )}
        </div>
      </CardHeader>
      
      <CardContent className="pt-0">
        <div className="space-y-6">
          {/* Location */}
          <div className="flex items-start gap-4">
            <div className="p-3 bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-600 rounded-xl shadow-sm group-hover:shadow-md transition-all duration-300">
              <MapPin className="h-5 w-5 text-gray-600 dark:text-gray-400" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-bold text-gray-900 dark:text-gray-100 mb-1">Location</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {call.location?.address || call.location_address || 'Location not specified'}
              </p>
            </div>
          </div>
          
          {/* Time */}
          <div className="flex items-start gap-4">
            <div className="p-3 bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-600 rounded-xl shadow-sm group-hover:shadow-md transition-all duration-300">
              <Clock className="h-5 w-5 text-gray-600 dark:text-gray-400" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-bold text-gray-900 dark:text-gray-100 mb-1">Time</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {isClient ? formattedTime : 'Loading...'}
              </p>
            </div>
          </div>
          
          {/* Description */}
          {(call.description || call.transcript) && (
            <div className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900/50 dark:to-gray-800 p-4 rounded-xl border border-gray-200/50 dark:border-gray-700/50">
              <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-3 leading-relaxed">
                {call.description || call.transcript}
              </p>
            </div>
          )}
          
          {/* Actions */}
          <div className="flex items-center gap-3 pt-4 border-t border-gray-200/50 dark:border-gray-700/50">
            {(call.status === CallStatus.PENDING || (call.status as string) === 'pending') && (
              <Button 
                size="sm" 
                onClick={handleAssign}
                className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold shadow-md hover:shadow-lg transform hover:scale-105"
              >
                Assign Unit
              </Button>
            )}
            {(call.status === CallStatus.IN_PROGRESS || (call.status as string) === 'in_progress') && (
              <Button 
                size="sm" 
                variant="outline"
                className="border-blue-300 dark:border-blue-600 text-blue-600 dark:text-blue-300 hover:bg-blue-50 dark:hover:bg-blue-900 font-bold shadow-sm hover:shadow-md transform hover:scale-105"
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

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
  [EmergencyType.MEDICAL]: 'bg-red-50 text-red-700 border-red-200',
  [EmergencyType.FIRE]: 'bg-orange-50 text-orange-700 border-orange-200',
  [EmergencyType.POLICE]: 'bg-blue-50 text-blue-700 border-blue-200',
  [EmergencyType.ACCIDENT]: 'bg-yellow-50 text-yellow-700 border-yellow-200',
  [EmergencyType.NATURAL_DISASTER]: 'bg-purple-50 text-purple-700 border-purple-200',
  [EmergencyType.OTHER]: 'bg-gray-50 text-gray-700 border-gray-200',
};

const severityColors = {
  [Severity.LOW]: 'bg-green-100 text-green-800',
  [Severity.MEDIUM]: 'bg-yellow-100 text-yellow-800',
  [Severity.HIGH]: 'bg-orange-100 text-orange-800',
  [Severity.CRITICAL]: 'bg-red-100 text-red-800',
};

const statusColors = {
  [CallStatus.PENDING]: 'bg-gray-100 text-gray-800',
  [CallStatus.IN_PROGRESS]: 'bg-blue-100 text-blue-800',
  [CallStatus.DISPATCHED]: 'bg-purple-100 text-purple-800',
  [CallStatus.RESOLVED]: 'bg-green-100 text-green-800',
  [CallStatus.CANCELLED]: 'bg-red-100 text-red-800',
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
      className={`cursor-pointer hover:shadow-md transition-shadow ${className}`}
      onClick={handleSelect}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <Phone className="h-4 w-4 text-muted-foreground" />
              <span className="font-medium">{call.callerName}</span>
              <span className="text-sm text-muted-foreground">{call.phoneNumber}</span>
            </div>
            <div className="flex items-center gap-2">
              <Badge className={emergencyTypeColors[call.emergencyType]}>
                {call.emergencyType.replace('_', ' ').toUpperCase()}
              </Badge>
              <Badge className={severityColors[call.severity]}>
                {call.severity.toUpperCase()}
              </Badge>
              <Badge className={statusColors[call.status]}>
                {call.status.replace('_', ' ').toUpperCase()}
              </Badge>
            </div>
          </div>
          {call.severity === Severity.CRITICAL && (
            <AlertTriangle className="h-5 w-5 text-red-500 animate-pulse" />
          )}
        </div>
      </CardHeader>
      
      <CardContent className="pt-0">
        <div className="space-y-3">
          {/* Location */}
          <div className="flex items-center gap-2 text-sm">
            <MapPin className="h-4 w-4 text-muted-foreground" />
            <span className="truncate">{call.location.address}</span>
          </div>
          
          {/* Time */}
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Clock className="h-4 w-4" />
            <span>{format(new Date(call.timestamp), 'MMM d, yyyy HH:mm')}</span>
          </div>
          
          {/* Description */}
          {call.description && (
            <p className="text-sm text-muted-foreground line-clamp-2">
              {call.description}
            </p>
          )}
          
          {/* Actions */}
          <div className="flex items-center gap-2 pt-2">
            {call.status === CallStatus.PENDING && (
              <Button size="sm" onClick={handleAssign}>
                Assign Unit
              </Button>
            )}
            {call.status === CallStatus.IN_PROGRESS && (
              <Button size="sm" variant="outline">
                View Details
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

'use client';

import { useState } from 'react';
import { format } from 'date-fns';
import { EmergencyCall, CallStatus, EmergencyType } from '@/types/emergency';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  Phone, 
  MapPin, 
  Clock, 
  User, 
  AlertTriangle, 
  Play, 
  Pause, 
  Download,
  Edit,
  Save,
  X
} from 'lucide-react';

interface CallDetailsProps {
  call: EmergencyCall;
  onUpdate?: (id: string, updates: Partial<EmergencyCall>) => void;
  onAssignUnit?: (callId: string, unitId: string) => void;
  className?: string;
}

export function CallDetails({ call, onUpdate, onAssignUnit, className }: CallDetailsProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedCall, setEditedCall] = useState(call);
  const [newNote, setNewNote] = useState('');
  const [selectedUnit, setSelectedUnit] = useState('');

  const emergencyTypeColors = {
    [EmergencyType.MEDICAL]: 'bg-red-50 text-red-700 border-red-200',
    [EmergencyType.FIRE]: 'bg-orange-50 text-orange-700 border-orange-200',
    [EmergencyType.POLICE]: 'bg-blue-50 text-blue-700 border-blue-200',
    [EmergencyType.ACCIDENT]: 'bg-yellow-50 text-yellow-700 border-yellow-200',
    [EmergencyType.NATURAL_DISASTER]: 'bg-purple-50 text-purple-700 border-purple-200',
    [EmergencyType.OTHER]: 'bg-gray-50 text-gray-700 border-gray-200',
  };

  const handleSave = () => {
    onUpdate?.(call.id, editedCall);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedCall(call);
    setIsEditing(false);
  };

  const handleAddNote = () => {
    if (newNote.trim()) {
      const updatedNotes = [...(editedCall.notes || []), newNote.trim()];
      setEditedCall({ ...editedCall, notes: updatedNotes });
      setNewNote('');
    }
  };

  const handleStatusChange = (status: CallStatus) => {
    setEditedCall({ ...editedCall, status });
  };

  const handleAssignUnit = () => {
    if (selectedUnit) {
      onAssignUnit?.(call.id, selectedUnit);
      setSelectedUnit('');
    }
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <CardTitle className="flex items-center gap-3">
                <Phone className="h-5 w-5" />
                Emergency Call Details
              </CardTitle>
              <p className="text-muted-foreground mt-1">
                Call ID: {call.id}
              </p>
            </div>
            <div className="flex items-center gap-2">
              {isEditing ? (
                <>
                  <Button size="sm" onClick={handleSave}>
                    <Save className="h-4 w-4 mr-1" />
                    Save
                  </Button>
                  <Button size="sm" variant="outline" onClick={handleCancel}>
                    <X className="h-4 w-4 mr-1" />
                    Cancel
                  </Button>
                </>
              ) : (
                <Button size="sm" variant="outline" onClick={() => setIsEditing(true)}>
                  <Edit className="h-4 w-4 mr-1" />
                  Edit
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Main Information */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Caller Information */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Caller Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium text-muted-foreground">Name</label>
              {isEditing ? (
                <Input
                  value={editedCall.callerName}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEditedCall({ ...editedCall, callerName: e.target.value })}
                />
              ) : (
                <p className="font-medium">{call.callerName}</p>
              )}
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Phone Number</label>
              {isEditing ? (
                <Input
                  value={editedCall.phoneNumber}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEditedCall({ ...editedCall, phoneNumber: e.target.value })}
                />
              ) : (
                <p className="font-medium">{call.phoneNumber}</p>
              )}
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Emergency Type</label>
              <div className="mt-1">
                <Badge className={emergencyTypeColors[call.emergencyType]}>
                  {call.emergencyType.replace('_', ' ').toUpperCase()}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Location Information */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Location</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium text-muted-foreground">Address</label>
              {isEditing ? (
                <Input
                  value={editedCall.location.address}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEditedCall({ 
                    ...editedCall, 
                    location: { ...editedCall.location, address: e.target.value }
                  })}
                />
              ) : (
                <p className="font-medium">{call.location.address}</p>
              )}
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">Latitude</label>
                <p className="font-medium">{call.location.latitude}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Longitude</label>
                <p className="font-medium">{call.location.longitude}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Call Details */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Call Details</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-muted-foreground">Description</label>
            {isEditing ? (
              <Textarea
                value={editedCall.description}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setEditedCall({ ...editedCall, description: e.target.value })}
                rows={3}
              />
            ) : (
              <p className="mt-1">{call.description}</p>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium text-muted-foreground">Status</label>
              <div className="mt-1">
                {isEditing ? (
                  <Select value={editedCall.status} onValueChange={(value: CallStatus) => handleStatusChange(value)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value={CallStatus.PENDING}>Pending</SelectItem>
                      <SelectItem value={CallStatus.IN_PROGRESS}>In Progress</SelectItem>
                      <SelectItem value={CallStatus.DISPATCHED}>Dispatched</SelectItem>
                      <SelectItem value={CallStatus.RESOLVED}>Resolved</SelectItem>
                      <SelectItem value={CallStatus.CANCELLED}>Cancelled</SelectItem>
                    </SelectContent>
                  </Select>
                ) : (
                  <Badge variant="outline">{call.status.replace('_', ' ').toUpperCase()}</Badge>
                )}
              </div>
            </div>
            
            <div>
              <label className="text-sm font-medium text-muted-foreground">Severity</label>
              <div className="mt-1">
                <Badge variant={call.severity === 'critical' ? 'destructive' : 'secondary'}>
                  {call.severity.toUpperCase()}
                </Badge>
              </div>
            </div>
            
            <div>
              <label className="text-sm font-medium text-muted-foreground">Call Time</label>
              <p className="font-medium mt-1">
                {format(new Date(call.timestamp), 'MMM d, yyyy HH:mm:ss')}
              </p>
            </div>
          </div>

          {call.assignedUnit && (
            <div>
              <label className="text-sm font-medium text-muted-foreground">Assigned Unit</label>
              <p className="font-medium mt-1">{call.assignedUnit}</p>
            </div>
          )}

          {call.estimatedArrival && (
            <div>
              <label className="text-sm font-medium text-muted-foreground">Estimated Arrival</label>
              <p className="font-medium mt-1">
                {format(new Date(call.estimatedArrival), 'MMM d, yyyy HH:mm')}
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Actions */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Actions</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-wrap gap-2">
            {call.audioRecording && (
              <div className="flex items-center gap-2">
                <Button size="sm" variant="outline">
                  <Play className="h-4 w-4 mr-1" />
                  Play Recording
                </Button>
                <Button size="sm" variant="outline">
                  <Download className="h-4 w-4 mr-1" />
                  Download
                </Button>
              </div>
            )}
            
            <div className="flex items-center gap-2">
              <Input
                placeholder="Enter unit ID"
                value={selectedUnit}
                onChange={(e) => setSelectedUnit(e.target.value)}
                className="w-32"
              />
              <Button size="sm" onClick={handleAssignUnit} disabled={!selectedUnit}>
                Assign Unit
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notes */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Notes</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Add new note */}
          <div className="flex gap-2">
            <Input
              placeholder="Add a note..."
              value={newNote}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setNewNote(e.target.value)}
              onKeyPress={(e: React.KeyboardEvent) => e.key === 'Enter' && handleAddNote()}
            />
            <Button onClick={handleAddNote} disabled={!newNote.trim()}>
              Add Note
            </Button>
          </div>

          {/* Existing notes */}
          {call.notes && call.notes.length > 0 ? (
            <div className="space-y-2">
              {call.notes.map((note, index) => (
                <div key={index} className="p-3 bg-muted rounded-lg">
                  <p className="text-sm">{note}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-muted-foreground text-sm">No notes yet</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

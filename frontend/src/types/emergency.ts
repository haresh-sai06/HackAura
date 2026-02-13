export interface EmergencyCall {
  id: string | number;
  callerName?: string;
  phoneNumber?: string;
  from_number?: string;
  to_number?: string;
  location?: {
    address: string;
    latitude: number;
    longitude: number;
  };
  location_address?: string;
  location_latitude?: number;
  location_longitude?: number;
  emergencyType: EmergencyType;
  severity: Severity;
  severity_level?: string;
  status: CallStatus;
  description?: string;
  transcript?: string;
  timestamp: Date | string;
  created_at?: Date | string;
  updated_at?: Date | string;
  estimatedArrival?: Date;
  assignedUnit?: string;
  assigned_service?: string;
  priority?: number;
  confidence?: number;
  risk_indicators?: string[];
  summary?: string;
  processing_time_ms?: number;
  metadata?: any;
  callDuration?: number;
  audioRecording?: string;
  notes?: string[];
}

export enum EmergencyType {
  MEDICAL = 'medical',
  FIRE = 'fire',
  POLICE = 'police',
  ACCIDENT = 'accident',
  NATURAL_DISASTER = 'natural_disaster',
  OTHER = 'other'
}

export enum Severity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum CallStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  DISPATCHED = 'dispatched',
  RESOLVED = 'resolved',
  CANCELLED = 'cancelled'
}

export interface CallFilter {
  status?: CallStatus[];
  severity?: Severity[];
  emergencyType?: EmergencyType[];
  dateRange?: {
    start: Date;
    end: Date;
  };
}

export interface CallAnalytics {
  totalCalls: number;
  callsByType: Record<EmergencyType, number>;
  callsBySeverity: Record<Severity, number>;
  callsByStatus: Record<CallStatus, number>;
  averageResponseTime: number;
  resolvedCalls: number;
  pendingCalls: number;
  callsByHour?: Array<{ hour: number; calls: number }>;
  callsByDay?: Array<{ day: string; calls: number }>;
  lastUpdated?: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  department?: string;
  isOnline: boolean;
}

export enum UserRole {
  DISPATCHER = 'dispatcher',
  RESPONDER = 'responder',
  SUPERVISOR = 'supervisor',
  ADMIN = 'admin'
}

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  callId?: string;
}

export enum NotificationType {
  NEW_CALL = 'new_call',
  CALL_UPDATED = 'call_updated',
  CALL_ASSIGNED = 'call_assigned',
  CALL_RESOLVED = 'call_resolved',
  SYSTEM_ALERT = 'system_alert'
}

export interface WebSocketMessage {
  type: WebSocketMessageType;
  payload: unknown;
  timestamp: Date;
}

export enum WebSocketMessageType {
  NEW_CALL = 'new_call',
  CALL_UPDATE = 'call_update',
  USER_STATUS = 'user_status',
  NOTIFICATION = 'notification',
  SYSTEM_UPDATE = 'system_update'
}

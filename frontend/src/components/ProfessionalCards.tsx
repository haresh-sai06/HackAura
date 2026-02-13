import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  Users, 
  Bell, 
  BarChart3, 
  Phone, 
  AlertTriangle, 
  TrendingUp,
  Clock,
  CheckCircle,
  XCircle,
  UserCheck,
  Mail,
  MessageSquare
} from 'lucide-react';

interface TeamCardProps {
  team: {
    id: string;
    name: string;
    specialization: string;
    total_members: number;
    active_members: number;
    available_members: number;
    active_calls: number;
  };
}

interface NotificationCardProps {
  notification: {
    id: string;
    title: string;
    message: string;
    priority: string;
    created_at: string;
    status: string;
  };
}

interface AnalyticsCardProps {
  metric: {
    title: string;
    value: string | number;
    change?: number;
    icon: React.ReactNode;
    color: string;
  };
}

// White Team Card Component
export const TeamCard: React.FC<TeamCardProps> = ({ team }) => {
  const getSpecializationColor = (specialization: string) => {
    const colors: { [key: string]: string } = {
      medical: 'bg-green-100 text-green-800',
      fire: 'bg-red-100 text-red-800',
      police: 'bg-blue-100 text-blue-800',
      general: 'bg-gray-100 text-gray-800'
    };
    return colors[specialization] || 'bg-gray-100 text-gray-800';
  };

  return (
    <Card className="bg-white border-gray-200 shadow-sm hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <Users className="w-5 h-5 text-blue-600" />
            {team.name}
          </CardTitle>
          <Badge className={getSpecializationColor(team.specialization)}>
            {team.specialization}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">{team.total_members}</div>
            <div className="text-sm text-gray-600">Total Members</div>
          </div>
          <div className="text-center p-3 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">{team.available_members}</div>
            <div className="text-sm text-gray-600">Available</div>
          </div>
        </div>
        
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Active Members</span>
            <span className="text-sm font-medium text-gray-900">{team.active_members}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Active Calls</span>
            <span className="text-sm font-medium text-gray-900">{team.active_calls}</span>
          </div>
        </div>
        
        <Button 
          variant="outline" 
          className="w-full bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
        >
          View Team Details
        </Button>
      </CardContent>
    </Card>
  );
};

// White Notification Card Component
export const NotificationCard: React.FC<NotificationCardProps> = ({ notification }) => {
  const getPriorityColor = (priority: string) => {
    const colors: { [key: string]: string } = {
      urgent: 'bg-red-100 text-red-800 border-red-200',
      high: 'bg-orange-100 text-orange-800 border-orange-200',
      medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      low: 'bg-blue-100 text-blue-800 border-blue-200'
    };
    return colors[priority] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'read':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'delivered':
        return <Mail className="w-4 h-4 text-blue-600" />;
      case 'sent':
        return <MessageSquare className="w-4 h-4 text-gray-600" />;
      default:
        return <Clock className="w-4 h-4 text-gray-400" />;
    }
  };

  return (
    <Card className="bg-white border-gray-200 shadow-sm hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2">
            <Bell className="w-5 h-5 text-gray-600" />
            <h3 className="font-semibold text-gray-900">{notification.title}</h3>
          </div>
          <div className="flex items-center gap-2">
            {getStatusIcon(notification.status)}
            <Badge className={getPriorityColor(notification.priority)}>
              {notification.priority}
            </Badge>
          </div>
        </div>
        
        <p className="text-gray-700 text-sm mb-3 leading-relaxed">
          {notification.message}
        </p>
        
        <div className="flex justify-between items-center">
          <span className="text-xs text-gray-500">
            {new Date(notification.created_at).toLocaleString()}
          </span>
          <div className="flex gap-2">
            <Button 
              variant="ghost" 
              size="sm"
              className="text-gray-600 hover:text-gray-900 hover:bg-gray-100"
            >
              Dismiss
            </Button>
            {notification.status !== 'read' && (
              <Button 
                variant="ghost" 
                size="sm"
                className="text-blue-600 hover:text-blue-800 hover:bg-blue-50"
              >
                Mark Read
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// White Analytics Card Component
export const AnalyticsCard: React.FC<AnalyticsCardProps> = ({ metric }) => {
  const getChangeColor = (change: number | undefined) => {
    if (!change) return 'text-gray-500';
    return change > 0 ? 'text-green-600' : 'text-red-600';
  };

  const getChangeIcon = (change: number | undefined) => {
    if (!change) return null;
    return change > 0 ? (
      <TrendingUp className="w-4 h-4" />
    ) : (
      <TrendingUp className="w-4 h-4 rotate-180" />
    );
  };

  return (
    <Card className="bg-white border-gray-200 shadow-sm hover:shadow-md transition-shadow">
      <CardContent className="p-6">
        <div className="flex items-center justify-between mb-4">
          <div className={`p-3 rounded-lg ${metric.color}`}>
            {metric.icon}
          </div>
          {metric.change !== undefined && (
            <div className={`flex items-center gap-1 ${getChangeColor(metric.change)}`}>
              {getChangeIcon(metric.change)}
              <span className="text-sm font-medium">
                {Math.abs(metric.change)}%
              </span>
            </div>
          )}
        </div>
        
        <div>
          <div className="text-2xl font-bold text-gray-900 mb-1">
            {metric.value}
          </div>
          <div className="text-sm text-gray-600">
            {metric.title}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// White Emergency Call Card Component
interface EmergencyCallCardProps {
  emergency: {
    id: string;
    emergency_type: string;
    priority: string;
    caller_location?: string;
    status: string;
    created_at: string;
    escalation_level: number;
  };
}

export const EmergencyCallCard: React.FC<EmergencyCallCardProps> = ({ emergency }) => {
  const getEmergencyTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      medical: 'bg-green-100 text-green-800 border-green-200',
      fire: 'bg-red-100 text-red-800 border-red-200',
      police: 'bg-blue-100 text-blue-800 border-blue-200',
      accident: 'bg-orange-100 text-orange-800 border-orange-200',
      other: 'bg-gray-100 text-gray-800 border-gray-200'
    };
    return colors[type] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getPriorityColor = (priority: string) => {
    const colors: { [key: string]: string } = {
      critical: 'bg-red-600 text-white',
      high: 'bg-red-100 text-red-800 border-red-200',
      medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      low: 'bg-blue-100 text-blue-800 border-blue-200'
    };
    return colors[priority] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  return (
    <Card className="bg-white border-gray-200 shadow-sm hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-red-600" />
            Emergency Call
          </CardTitle>
          <div className="flex items-center gap-2">
            <Badge className={getEmergencyTypeColor(emergency.emergency_type)}>
              {emergency.emergency_type}
            </Badge>
            <Badge className={getPriorityColor(emergency.priority)}>
              {emergency.priority}
            </Badge>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Status</span>
            <Badge variant="outline" className="text-gray-700 border-gray-300">
              {emergency.status}
            </Badge>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Escalation Level</span>
            <span className="text-sm font-medium text-gray-900">
              Level {emergency.escalation_level}
            </span>
          </div>
          {emergency.caller_location && (
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Location</span>
              <span className="text-sm font-medium text-gray-900">
                {emergency.caller_location}
              </span>
            </div>
          )}
        </div>
        
        <div className="text-xs text-gray-500">
          Created: {new Date(emergency.created_at).toLocaleString()}
        </div>
        
        <div className="flex gap-2">
          <Button 
            variant="outline" 
            size="sm"
            className="bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
          >
            View Details
          </Button>
          <Button 
            variant="outline" 
            size="sm"
            className="bg-red-50 border-red-200 text-red-700 hover:bg-red-100"
          >
            Take Action
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

// Team Member Card Component
interface TeamMemberCardProps {
  member: {
    id: string;
    name: string;
    role: string;
    status: string;
    current_calls: number;
    total_calls_handled: number;
    avg_response_time: number;
    rating: number;
    skills: string[];
  };
}

export const TeamMemberCard: React.FC<TeamMemberCardProps> = ({ member }) => {
  const getStatusColor = (status: string) => {
    const colors: { [key: string]: string } = {
      active: 'bg-green-100 text-green-800',
      busy: 'bg-red-100 text-red-800',
      offline: 'bg-gray-100 text-gray-800',
      on_break: 'bg-yellow-100 text-yellow-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <Card className="bg-white border-gray-200 shadow-sm hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <UserCheck className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">{member.name}</h3>
              <p className="text-sm text-gray-600">{member.role}</p>
            </div>
          </div>
          <Badge className={getStatusColor(member.status)}>
            {member.status}
          </Badge>
        </div>
        
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className="text-center p-2 bg-gray-50 rounded">
            <div className="text-lg font-bold text-gray-900">{member.current_calls}</div>
            <div className="text-xs text-gray-600">Current Calls</div>
          </div>
          <div className="text-center p-2 bg-blue-50 rounded">
            <div className="text-lg font-bold text-blue-600">{member.total_calls_handled}</div>
            <div className="text-xs text-gray-600">Total Handled</div>
          </div>
        </div>
        
        <div className="space-y-2 mb-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Avg Response Time</span>
            <span className="text-sm font-medium text-gray-900">
              {member.avg_response_time}s
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Rating</span>
            <div className="flex items-center gap-1">
              <span className="text-sm font-medium text-gray-900">
                {member.rating.toFixed(1)}
              </span>
              <div className="flex">
                {[...Array(5)].map((_, i) => (
                  <div
                    key={i}
                    className={`w-3 h-3 rounded-full ${
                      i < Math.floor(member.rating)
                        ? 'bg-yellow-400'
                        : 'bg-gray-300'
                    }`}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
        
        {member.skills.length > 0 && (
          <div className="mb-4">
            <div className="text-sm text-gray-600 mb-2">Skills</div>
            <div className="flex flex-wrap gap-1">
              {member.skills.map((skill, index) => (
                <Badge
                  key={index}
                  variant="outline"
                  className="text-xs bg-blue-50 text-blue-700 border-blue-200"
                >
                  {skill}
                </Badge>
              ))}
            </div>
          </div>
        )}
        
        <Button 
          variant="outline" 
          className="w-full bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
        >
          Assign Call
        </Button>
      </CardContent>
    </Card>
  );
};

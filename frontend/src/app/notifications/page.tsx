'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  Bell, 
  Check, 
  X, 
  AlertTriangle, 
  Phone, 
  Users, 
  Activity,
  Search,
  Filter,
  Clock
} from 'lucide-react';

// Mock notifications data
const notifications = [
  {
    id: '1',
    type: 'new_call',
    title: 'New Emergency Call',
    message: 'Medical emergency reported at 123 Main St - Patient experiencing chest pain',
    timestamp: new Date(Date.now() - 300000),
    read: false,
    callId: 'call-123',
    priority: 'high',
  },
  {
    id: '2',
    type: 'call_assigned',
    title: 'Call Assigned',
    message: 'You have been assigned to emergency call #456',
    timestamp: new Date(Date.now() - 600000),
    read: false,
    callId: 'call-456',
    priority: 'medium',
  },
  {
    id: '3',
    type: 'call_updated',
    title: 'Call Status Updated',
    message: 'Emergency call #789 status changed to "Resolved"',
    timestamp: new Date(Date.now() - 900000),
    read: true,
    callId: 'call-789',
    priority: 'low',
  },
  {
    id: '4',
    type: 'system_alert',
    title: 'System Alert',
    message: 'Emergency response time exceeding targets in District 3',
    timestamp: new Date(Date.now() - 1200000),
    read: true,
    priority: 'high',
  },
  {
    id: '5',
    type: 'call_resolved',
    title: 'Call Resolved',
    message: 'Fire emergency at Oak Avenue has been successfully resolved',
    timestamp: new Date(Date.now() - 1500000),
    read: true,
    callId: 'call-321',
    priority: 'medium',
  },
  {
    id: '6',
    type: 'new_call',
    title: 'New Emergency Call',
    message: 'Multiple vehicle accident reported on Highway 101',
    timestamp: new Date(Date.now() - 1800000),
    read: false,
    callId: 'call-654',
    priority: 'critical',
  },
];

const typeIcons = {
  new_call: Phone,
  call_assigned: Users,
  call_updated: Activity,
  call_resolved: Check,
  system_alert: AlertTriangle,
};

const typeColors = {
  new_call: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  call_assigned: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  call_updated: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  call_resolved: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  system_alert: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
};

const priorityColors = {
  low: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
  medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  high: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
  critical: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 animate-pulse',
};

export default function NotificationsPage() {
  const [notificationsList, setNotificationsList] = useState(notifications);
  const [searchTerm, setSearchTerm] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');
  const [priorityFilter, setPriorityFilter] = useState('all');
  const [readFilter, setReadFilter] = useState('all');

  const filteredNotifications = notificationsList.filter(notification => {
    const matchesSearch = 
      notification.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      notification.message.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesType = typeFilter === 'all' || notification.type === typeFilter;
    const matchesPriority = priorityFilter === 'all' || notification.priority === priorityFilter;
    const matchesRead = readFilter === 'all' || 
      (readFilter === 'read' && notification.read) || 
      (readFilter === 'unread' && !notification.read);

    return matchesSearch && matchesType && matchesPriority && matchesRead;
  });

  const unreadCount = notificationsList.filter(n => !n.read).length;

  const markAsRead = (id: string) => {
    setNotificationsList(notificationsList.map(n => 
      n.id === id ? { ...n, read: true } : n
    ));
  };

  const markAllAsRead = () => {
    setNotificationsList(notificationsList.map(n => ({ ...n, read: true })));
  };

  const deleteNotification = (id: string) => {
    setNotificationsList(notificationsList.filter(n => n.id !== id));
  };

  const formatTimeAgo = (date: Date) => {
    const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
    
    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
    return `${Math.floor(seconds / 86400)} days ago`;
  };

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Notifications</h1>
            {unreadCount > 0 && (
              <Badge className="bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 px-3 py-1">
                {unreadCount} unread
              </Badge>
            )}
          </div>
          <div className="flex gap-2">
            <Button 
              variant="outline" 
              onClick={markAllAsRead}
              disabled={unreadCount === 0}
            >
              Mark All Read
            </Button>
            <Button variant="outline">
              Settings
            </Button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900 dark:to-blue-800 border-blue-200 dark:border-blue-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-blue-600 dark:text-blue-300 flex items-center gap-2">
                <Bell className="h-5 w-5" />
                Total
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-700 dark:text-blue-200">{notificationsList.length}</div>
              <CardDescription className="text-blue-600 dark:text-blue-400">
                All notifications
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900 dark:to-red-800 border-red-200 dark:border-red-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-red-600 dark:text-red-300 flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                Unread
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-red-700 dark:text-red-200">{unreadCount}</div>
              <CardDescription className="text-red-600 dark:text-red-400">
                Require attention
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900 dark:to-orange-800 border-orange-200 dark:border-orange-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-orange-600 dark:text-orange-300 flex items-center gap-2">
                <Phone className="h-5 w-5" />
                Calls
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-700 dark:text-orange-200">
                {notificationsList.filter(n => n.type.includes('call')).length}
              </div>
              <CardDescription className="text-orange-600 dark:text-orange-400">
                Call-related
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900 dark:to-purple-800 border-purple-200 dark:border-purple-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-purple-600 dark:text-purple-300 flex items-center gap-2">
                <Activity className="h-5 w-5" />
                System
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-purple-700 dark:text-purple-200">
                {notificationsList.filter(n => n.type === 'system_alert').length}
              </div>
              <CardDescription className="text-purple-600 dark:text-purple-400">
                System alerts
              </CardDescription>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Filter className="h-5 w-5" />
              Filters
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
                <Input
                  placeholder="Search notifications..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              
              <Select value={typeFilter} onValueChange={setTypeFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Types</SelectItem>
                  <SelectItem value="new_call">New Call</SelectItem>
                  <SelectItem value="call_assigned">Call Assigned</SelectItem>
                  <SelectItem value="call_updated">Call Updated</SelectItem>
                  <SelectItem value="call_resolved">Call Resolved</SelectItem>
                  <SelectItem value="system_alert">System Alert</SelectItem>
                </SelectContent>
              </Select>

              <Select value={priorityFilter} onValueChange={setPriorityFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by priority" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Priorities</SelectItem>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                </SelectContent>
              </Select>

              <Select value={readFilter} onValueChange={setReadFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="read">Read</SelectItem>
                  <SelectItem value="unread">Unread</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Notifications List */}
        <div className="space-y-4">
          {filteredNotifications.map((notification) => {
            const Icon = typeIcons[notification.type as keyof typeof typeIcons];
            return (
              <Card 
                key={notification.id} 
                className={`transition-all hover:shadow-md ${
                  !notification.read ? 'border-l-4 border-l-blue-500' : ''
                }`}
              >
                <CardContent className="p-6">
                  <div className="flex items-start gap-4">
                    <div className={`p-3 rounded-full ${
                      typeColors[notification.type as keyof typeof typeColors]
                    }`}>
                      <Icon className="h-5 w-5" />
                    </div>
                    
                    <div className="flex-1 space-y-2">
                      <div className="flex items-start justify-between">
                        <div className="space-y-1">
                          <h3 className="font-semibold text-gray-900 dark:text-gray-100">
                            {notification.title}
                          </h3>
                          <p className="text-gray-600 dark:text-gray-400">
                            {notification.message}
                          </p>
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge className={`${
                            priorityColors[notification.priority as keyof typeof priorityColors]
                          } px-2 py-1 text-xs font-semibold`}>
                            {notification.priority.toUpperCase()}
                          </Badge>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => deleteNotification(notification.id)}
                            className="text-gray-400 hover:text-red-600"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
                          <Clock className="h-4 w-4" />
                          {formatTimeAgo(notification.timestamp)}
                        </div>
                        
                        {!notification.read && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => markAsRead(notification.id)}
                            className="text-blue-600 border-blue-300 hover:bg-blue-50 dark:text-blue-400 dark:border-blue-600 dark:hover:bg-blue-900"
                          >
                            <Check className="h-4 w-4 mr-1" />
                            Mark Read
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </DashboardLayout>
  );
}

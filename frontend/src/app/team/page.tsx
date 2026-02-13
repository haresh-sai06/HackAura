'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Search, Filter, Users, MapPin, Phone, Mail, Shield, Activity } from 'lucide-react';

// Mock team data
const teamMembers = [
  {
    id: '1',
    name: 'John Anderson',
    email: 'john.anderson@emergency.gov',
    role: 'Dispatcher',
    department: 'Emergency Operations',
    isOnline: true,
    location: 'Central Command',
    phone: '+1-555-0101',
    avatar: '/avatars/john.jpg',
    status: 'Available',
    activeCalls: 2,
    totalCalls: 156,
    responseTime: 3.2,
    lastActive: new Date(Date.now() - 300000),
  },
  {
    id: '2',
    name: 'Sarah Mitchell',
    email: 'sarah.mitchell@emergency.gov',
    role: 'Responder',
    department: 'Medical Unit',
    isOnline: true,
    location: 'Field Unit A',
    phone: '+1-555-0102',
    avatar: '/avatars/sarah.jpg',
    status: 'On Call',
    activeCalls: 1,
    totalCalls: 142,
    responseTime: 4.1,
    lastActive: new Date(Date.now() - 120000),
  },
  {
    id: '3',
    name: 'Michael Chen',
    email: 'michael.chen@emergency.gov',
    role: 'Responder',
    department: 'Fire Department',
    isOnline: false,
    location: 'Fire Station 3',
    phone: '+1-555-0103',
    avatar: '/avatars/michael.jpg',
    status: 'Off Duty',
    activeCalls: 0,
    totalCalls: 98,
    responseTime: 3.8,
    lastActive: new Date(Date.now() - 3600000),
  },
  {
    id: '4',
    name: 'Emily Rodriguez',
    email: 'emily.rodriguez@emergency.gov',
    role: 'Supervisor',
    department: 'Emergency Operations',
    isOnline: true,
    location: 'Central Command',
    phone: '+1-555-0104',
    avatar: '/avatars/emily.jpg',
    status: 'Available',
    activeCalls: 0,
    totalCalls: 203,
    responseTime: 2.9,
    lastActive: new Date(Date.now() - 60000),
  },
  {
    id: '5',
    name: 'David Thompson',
    email: 'david.thompson@emergency.gov',
    role: 'Responder',
    department: 'Police Unit',
    isOnline: true,
    location: 'Patrol Area B',
    phone: '+1-555-0105',
    avatar: '/avatars/david.jpg',
    status: 'Busy',
    activeCalls: 3,
    totalCalls: 187,
    responseTime: 3.5,
    lastActive: new Date(Date.now() - 180000),
  },
  {
    id: '6',
    name: 'Lisa Park',
    email: 'lisa.park@emergency.gov',
    role: 'Dispatcher',
    department: 'Emergency Operations',
    isOnline: true,
    location: 'Central Command',
    phone: '+1-555-0106',
    avatar: '/avatars/lisa.jpg',
    status: 'Available',
    activeCalls: 1,
    totalCalls: 134,
    responseTime: 4.3,
    lastActive: new Date(Date.now() - 90000),
  },
];

const roleColors = {
  'Dispatcher': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  'Responder': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  'Supervisor': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
  'Admin': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
};

const statusColors = {
  'Available': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  'On Call': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  'Busy': 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
  'Off Duty': 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
};

export default function TeamPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  const [departmentFilter, setDepartmentFilter] = useState('all');

  const filteredTeam = teamMembers.filter(member => {
    const matchesSearch = 
      member.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      member.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      member.role.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesRole = roleFilter === 'all' || member.role === roleFilter;
    const matchesStatus = statusFilter === 'all' || member.status === statusFilter;
    const matchesDepartment = departmentFilter === 'all' || member.department === departmentFilter;

    return matchesSearch && matchesRole && matchesStatus && matchesDepartment;
  });

  const onlineCount = teamMembers.filter(m => m.isOnline).length;
  const availableCount = teamMembers.filter(m => m.status === 'Available').length;
  const busyCount = teamMembers.filter(m => m.status === 'Busy' || m.status === 'On Call').length;

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Team Management</h1>
          <Button className="bg-blue-600 hover:bg-blue-700 text-white">
            Add Team Member
          </Button>
        </div>

        {/* Team Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900 dark:to-green-800 border-green-200 dark:border-green-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-green-600 dark:text-green-300 flex items-center gap-2">
                <Users className="h-5 w-5" />
                Online Team Members
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-700 dark:text-green-200">{onlineCount}</div>
              <CardDescription className="text-green-600 dark:text-green-400">
                of {teamMembers.length} total members
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900 dark:to-blue-800 border-blue-200 dark:border-blue-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-blue-600 dark:text-blue-300 flex items-center gap-2">
                <Activity className="h-5 w-5" />
                Available
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-700 dark:text-blue-200">{availableCount}</div>
              <CardDescription className="text-blue-600 dark:text-blue-400">
                Ready for assignment
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900 dark:to-orange-800 border-orange-200 dark:border-orange-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-orange-600 dark:text-orange-300 flex items-center gap-2">
                <Phone className="h-5 w-5" />
                Busy / On Call
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-700 dark:text-orange-200">{busyCount}</div>
              <CardDescription className="text-orange-600 dark:text-orange-400">
                Currently engaged
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
                  placeholder="Search team members..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              
              <Select value={roleFilter} onValueChange={setRoleFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by role" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Roles</SelectItem>
                  <SelectItem value="Dispatcher">Dispatcher</SelectItem>
                  <SelectItem value="Responder">Responder</SelectItem>
                  <SelectItem value="Supervisor">Supervisor</SelectItem>
                  <SelectItem value="Admin">Admin</SelectItem>
                </SelectContent>
              </Select>

              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Statuses</SelectItem>
                  <SelectItem value="Available">Available</SelectItem>
                  <SelectItem value="On Call">On Call</SelectItem>
                  <SelectItem value="Busy">Busy</SelectItem>
                  <SelectItem value="Off Duty">Off Duty</SelectItem>
                </SelectContent>
              </Select>

              <Select value={departmentFilter} onValueChange={setDepartmentFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by department" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Departments</SelectItem>
                  <SelectItem value="Emergency Operations">Emergency Operations</SelectItem>
                  <SelectItem value="Medical Unit">Medical Unit</SelectItem>
                  <SelectItem value="Fire Department">Fire Department</SelectItem>
                  <SelectItem value="Police Unit">Police Unit</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Team Members Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTeam.map((member) => (
            <Card key={member.id} className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-4">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="relative">
                      <Avatar className="h-12 w-12">
                        <AvatarImage src={member.avatar} alt={member.name} />
                        <AvatarFallback>
                          {member.name.split(' ').map(n => n[0]).join('')}
                        </AvatarFallback>
                      </Avatar>
                      <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white dark:border-gray-800 ${
                        member.isOnline ? 'bg-green-500' : 'bg-gray-400'
                      }`} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-gray-100">{member.name}</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">{member.email}</p>
                    </div>
                  </div>
                  <Badge className={`${roleColors[member.role as keyof typeof roleColors]} px-3 py-1 text-xs font-semibold`}>
                    {member.role}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-2">
                  <Badge className={`${statusColors[member.status as keyof typeof statusColors]} px-3 py-1 text-xs font-semibold`}>
                    {member.status}
                  </Badge>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {member.isOnline ? '🟢 Online' : '🔴 Offline'}
                  </span>
                </div>

                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                    <MapPin className="h-4 w-4" />
                    <span>{member.location}</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                    <Phone className="h-4 w-4" />
                    <span>{member.phone}</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                    <Shield className="h-4 w-4" />
                    <span>{member.department}</span>
                  </div>
                </div>

                <div className="pt-2 border-t border-gray-200 dark:border-gray-700">
                  <div className="grid grid-cols-3 gap-2 text-center">
                    <div>
                      <div className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                        {member.activeCalls}
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Active</div>
                    </div>
                    <div>
                      <div className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                        {member.totalCalls}
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Total</div>
                    </div>
                    <div>
                      <div className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                        {member.responseTime}m
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Avg Time</div>
                    </div>
                  </div>
                </div>

                <div className="flex gap-2">
                  <Button size="sm" variant="outline" className="flex-1">
                    View Profile
                  </Button>
                  <Button size="sm" className="flex-1">
                    Contact
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
}

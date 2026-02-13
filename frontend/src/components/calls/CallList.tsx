'use client';

import { useState } from 'react';
import { EmergencyCall, CallStatus, Severity, EmergencyType } from '@/types/emergency';
import { CallCard } from './CallCard';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Search, Filter, RefreshCw } from 'lucide-react';
import '@/styles/filters.css';

interface CallListProps {
  calls: EmergencyCall[];
  loading?: boolean;
  onSelectCall?: (call: EmergencyCall) => void;
  onAssignCall?: (callId: string) => void;
  onRefresh?: () => void;
}

export function CallList({ 
  calls, 
  loading = false, 
  onSelectCall, 
  onAssignCall, 
  onRefresh 
}: CallListProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<CallStatus | 'all'>('all');
  const [severityFilter, setSeverityFilter] = useState<Severity | 'all'>('all');
  const [typeFilter, setTypeFilter] = useState<EmergencyType | 'all'>('all');

  const filteredCalls = calls.filter(call => {
    const matchesSearch = 
      call.callerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      call.phoneNumber.includes(searchTerm) ||
      call.location.address.toLowerCase().includes(searchTerm.toLowerCase()) ||
      call.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || call.status === statusFilter;
    const matchesSeverity = severityFilter === 'all' || call.severity === severityFilter;
    const matchesType = typeFilter === 'all' || call.emergencyType === typeFilter;

    return matchesSearch && matchesStatus && matchesSeverity && matchesType;
  });

  const activeCallsCount = calls.filter(call => 
    call.status === CallStatus.PENDING || call.status === CallStatus.IN_PROGRESS
  ).length;

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-3xl font-bold text-white">Emergency Calls</h2>
          <p className="text-gray-300 dark:text-gray-400 mt-1">
            <span className="font-semibold text-white">{activeCallsCount}</span> active calls • 
            <span className="font-semibold text-white">{calls.length}</span> total
          </p>
        </div>
        <Button 
          onClick={onRefresh} 
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 h-10"
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          {loading ? 'Refreshing...' : 'Refresh'}
        </Button>
      </div>

      {/* Filters */}
      <div className="filters-card bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
        <h3 className="text-lg font-semibold text-white mb-4">Filters</h3>
        
        {/* Search */}
        <div className="relative mb-4">
          <Search className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-white" />
          <Input
            placeholder="Search calls by name, phone, location, or description..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="filters-card pl-12 h-11 bg-gray-50 dark:bg-gray-900 border-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-400 focus:ring-blue-500 dark:focus:ring-blue-400 text-white placeholder:text-gray-400"
          />
        </div>

        {/* Filter dropdowns */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <Select value={statusFilter} onValueChange={(value: string) => setStatusFilter(value as CallStatus | 'all')}>
            <SelectTrigger className="filters-card h-11 bg-gray-50 dark:bg-gray-900 border-gray-300 dark:border-gray-600 text-white">
              <SelectValue placeholder="Filter by status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Statuses</SelectItem>
              <SelectItem value={CallStatus.PENDING}>Pending</SelectItem>
              <SelectItem value={CallStatus.IN_PROGRESS}>In Progress</SelectItem>
              <SelectItem value={CallStatus.DISPATCHED}>Dispatched</SelectItem>
              <SelectItem value={CallStatus.RESOLVED}>Resolved</SelectItem>
              <SelectItem value={CallStatus.CANCELLED}>Cancelled</SelectItem>
            </SelectContent>
          </Select>

          <Select value={severityFilter} onValueChange={(value: string) => setSeverityFilter(value as Severity | 'all')}>
            <SelectTrigger className="filters-card h-11 bg-gray-50 dark:bg-gray-900 border-gray-300 dark:border-gray-600 text-white">
              <SelectValue placeholder="Filter by severity" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Severities</SelectItem>
              <SelectItem value={Severity.LOW}>Low</SelectItem>
              <SelectItem value={Severity.MEDIUM}>Medium</SelectItem>
              <SelectItem value={Severity.HIGH}>High</SelectItem>
              <SelectItem value={Severity.CRITICAL}>Critical</SelectItem>
            </SelectContent>
          </Select>

          <Select value={typeFilter} onValueChange={(value: string) => setTypeFilter(value as EmergencyType | 'all')}>
            <SelectTrigger className="filters-card h-11 bg-gray-50 dark:bg-gray-900 border-gray-300 dark:border-gray-600 text-white">
              <SelectValue placeholder="Filter by type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Types</SelectItem>
              <SelectItem value={EmergencyType.MEDICAL}>Medical</SelectItem>
              <SelectItem value={EmergencyType.FIRE}>Fire</SelectItem>
              <SelectItem value={EmergencyType.POLICE}>Police</SelectItem>
              <SelectItem value={EmergencyType.ACCIDENT}>Accident</SelectItem>
              <SelectItem value={EmergencyType.NATURAL_DISASTER}>Natural Disaster</SelectItem>
              <SelectItem value={EmergencyType.OTHER}>Other</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Active filters */}
        {(statusFilter !== 'all' || severityFilter !== 'all' || typeFilter !== 'all' || searchTerm) && (
          <div className="flex items-center gap-2 p-3 bg-blue-50 dark:bg-blue-900 rounded-lg">
            <span className="text-sm font-medium text-white">Active filters:</span>
            {statusFilter !== 'all' && (
              <Badge variant="secondary" className="bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-200 border-blue-300 dark:border-blue-600">
                Status: {statusFilter}
              </Badge>
            )}
            {severityFilter !== 'all' && (
              <Badge variant="secondary" className="bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-200 border-blue-300 dark:border-blue-600">
                Severity: {severityFilter}
              </Badge>
            )}
            {typeFilter !== 'all' && (
              <Badge variant="secondary" className="bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-200 border-blue-300 dark:border-blue-600">
                Type: {typeFilter}
              </Badge>
            )}
            {searchTerm && (
              <Badge variant="secondary" className="bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-200 border-blue-300 dark:border-blue-600">
                Search: {searchTerm}
              </Badge>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                setSearchTerm('');
                setStatusFilter('all');
                setSeverityFilter('all');
                setTypeFilter('all');
              }}
              className="text-white hover:text-gray-200 dark:text-white dark:hover:text-gray-200"
            >
              Clear all
            </Button>
          </div>
        )}
      </div>

      {/* Call list */}
      <div className="space-y-3">
        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
            <p className="text-muted-foreground mt-2">Loading calls...</p>
          </div>
        ) : filteredCalls.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-muted-foreground">
              {calls.length === 0 ? 'No emergency calls yet' : 'No calls match your filters'}
            </p>
          </div>
        ) : (
          <div className="grid gap-3">
            {filteredCalls.map((call) => (
              <CallCard
                key={call.id}
                call={call}
                onSelect={onSelectCall}
                onAssign={onAssignCall}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

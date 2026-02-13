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
      (call.callerName || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (call.phoneNumber || call.from_number || '').includes(searchTerm) ||
      (call.location?.address || call.location_address || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (call.description || call.transcript || '').toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || call.status === statusFilter;
    const matchesSeverity = severityFilter === 'all' || call.severity === severityFilter;
    const matchesType = typeFilter === 'all' || call.emergencyType === typeFilter;

    return matchesSearch && matchesStatus && matchesSeverity && matchesType;
  });

  const activeCallsCount = calls.filter(call => 
    call.status === CallStatus.PENDING || call.status === CallStatus.IN_PROGRESS
  ).length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="animate-fade-in">
          <h2 className="text-3xl font-bold text-dark dark:text-light mb-2">Emergency Calls</h2>
          <p className="text-dark-secondary dark:text-light-secondary">
            <span className="font-semibold text-blue-600 dark:text-blue-400">{activeCallsCount}</span> active calls • 
            <span className="font-semibold text-dark dark:text-light">{calls.length}</span> total
          </p>
        </div>
        <Button 
          onClick={onRefresh} 
          disabled={loading}
          className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-medium px-6 h-11 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none animate-fade-in"
          style={{ animationDelay: '0.1s' }}
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          {loading ? 'Refreshing...' : 'Refresh'}
        </Button>
      </div>

      {/* Filters */}
      <div className="filters-card glass-effect p-6 rounded-2xl mb-8 relative animate-slide-in" style={{ animationDelay: '0.2s' }}>
        <h2 className="text-lg font-semibold text-dark dark:text-light mb-6">Filters</h2>
        
        {/* Search */}
        <div className="relative mb-6">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5 pointer-events-none" />
          <Input
            placeholder="Search calls by name, phone, location, or description..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-white/80 dark:bg-slate-800/80 text-black dark:text-white placeholder:text-white border border-gray-300 dark:border-slate-600 rounded-xl py-3 pl-12 pr-4 shadow-sm focus:ring-2 focus:ring-blue-500/50 focus:outline-none focus:border-blue-400 transition-all duration-200"
          />
        </div>

        {/* Filter dropdowns */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 relative z-10">
          <Select value={statusFilter} onValueChange={(value: string) => setStatusFilter(value as CallStatus | 'all')}>
            <SelectTrigger className="w-full bg-white/80 dark:bg-slate-800/80 border border-gray-300 dark:border-slate-600 rounded-xl px-4 py-3 shadow-sm hover:border-blue-400 focus:ring-2 focus:ring-blue-500/50 focus:outline-none transition-all duration-200">
              <SelectValue placeholder="Filter by status" />
            </SelectTrigger>
            <SelectContent className="bg-white/95 dark:bg-slate-800/95 backdrop-blur-xl shadow-xl border border-gray-200 dark:border-slate-600 rounded-xl z-50 mt-2">
              <SelectItem value="all">All Statuses</SelectItem>
              <SelectItem value={CallStatus.PENDING}>Pending</SelectItem>
              <SelectItem value={CallStatus.IN_PROGRESS}>In Progress</SelectItem>
              <SelectItem value={CallStatus.DISPATCHED}>Dispatched</SelectItem>
              <SelectItem value={CallStatus.RESOLVED}>Resolved</SelectItem>
              <SelectItem value={CallStatus.CANCELLED}>Cancelled</SelectItem>
            </SelectContent>
          </Select>

          <Select value={severityFilter} onValueChange={(value: string) => setSeverityFilter(value as Severity | 'all')}>
            <SelectTrigger className="w-full bg-white/80 dark:bg-slate-800/80 border border-gray-300 dark:border-slate-600 rounded-xl px-4 py-3 shadow-sm hover:border-blue-400 focus:ring-2 focus:ring-blue-500/50 focus:outline-none transition-all duration-200">
              <SelectValue placeholder="Filter by severity" />
            </SelectTrigger>
            <SelectContent className="bg-white/95 dark:bg-slate-800/95 backdrop-blur-xl shadow-xl border border-gray-200 dark:border-slate-600 rounded-xl z-50 mt-2">
              <SelectItem value="all">All Severities</SelectItem>
              <SelectItem value={Severity.LOW}>Low</SelectItem>
              <SelectItem value={Severity.MEDIUM}>Medium</SelectItem>
              <SelectItem value={Severity.HIGH}>High</SelectItem>
              <SelectItem value={Severity.CRITICAL}>Critical</SelectItem>
            </SelectContent>
          </Select>

          <Select value={typeFilter} onValueChange={(value: string) => setTypeFilter(value as EmergencyType | 'all')}>
            <SelectTrigger className="w-full bg-white/80 dark:bg-slate-800/80 border border-gray-300 dark:border-slate-600 rounded-xl px-4 py-3 shadow-sm hover:border-blue-400 focus:ring-2 focus:ring-blue-500/50 focus:outline-none transition-all duration-200">
              <SelectValue placeholder="Filter by type" />
            </SelectTrigger>
            <SelectContent className="bg-white/95 dark:bg-slate-800/95 backdrop-blur-xl shadow-xl border border-gray-200 dark:border-slate-600 rounded-xl z-50 mt-2">
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
          <div className="flex items-center gap-2 p-4 bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/50 dark:to-blue-800/50 rounded-xl border border-blue-200 dark:border-blue-700 animate-slide-in">
            <span className="text-sm font-medium text-blue-800 dark:text-blue-200">Active filters:</span>
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
              className="text-blue-600 hover:text-blue-800 dark:text-blue-300 dark:hover:text-blue-100 hover:bg-blue-200/50 dark:hover:bg-blue-700/50 transition-colors-smooth"
            >
              Clear all
            </Button>
          </div>
        )}
      </div>

      {/* Visual Divider */}
      <div className="border-t border-gray-200 dark:border-slate-700 my-8"></div>

      {/* Call list */}
      <div className="space-y-4 animate-slide-in" style={{ animationDelay: '0.3s' }}>
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-muted-foreground text-lg">Loading calls...</p>
          </div>
        ) : filteredCalls.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📞</div>
            <p className="text-muted-foreground text-lg">
              {calls.length === 0 ? 'No emergency calls yet' : 'No calls match your filters'}
            </p>
          </div>
        ) : (
          <div className="grid gap-4">
            {filteredCalls.map((call, index) => (
              <div key={call.id} className="animate-slide-in" style={{ animationDelay: `${0.4 + index * 0.05}s` }}>
                <CallCard
                  call={call}
                  onSelect={onSelectCall}
                  onAssign={onAssignCall}
                />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

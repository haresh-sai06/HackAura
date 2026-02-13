'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { emergencyApi } from '@/utils/api';
import { useWebSocketService } from '@/utils/websocket';

export function useNavigationData() {
  const [activeCallsCount, setActiveCallsCount] = useState(0);
  const [unreadNotificationsCount, setUnreadNotificationsCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { isConnected, onNewCall, onNotification, onCallUpdate } = useWebSocketService();

  // Refs for debouncing and error tracking
  const activeCallsTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const notificationsTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const retryCountRef = useRef(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const maxRetries = 3;

  // Simple debounced state updates using refs
  const debouncedSetActiveCallsCount = (value: number | ((prev: number) => number)) => {
    if (activeCallsTimeoutRef.current) {
      clearTimeout(activeCallsTimeoutRef.current);
    }
    activeCallsTimeoutRef.current = setTimeout(() => {
      setActiveCallsCount(value);
    }, 100); // 100ms debounce
  };

  const debouncedSetUnreadNotificationsCount = (value: number | ((prev: number) => number)) => {
    if (notificationsTimeoutRef.current) {
      clearTimeout(notificationsTimeoutRef.current);
    }
    notificationsTimeoutRef.current = setTimeout(() => {
      setUnreadNotificationsCount(value);
    }, 100); // 100ms debounce
  };

  // Fetch initial data
  const fetchNavigationData = async () => {
    // Don't retry if we've exceeded max retries
    if (retryCountRef.current >= maxRetries) {
      console.warn('Max retries reached for navigation data, using fallback values');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // Get analytics data for active calls count
      const analytics = await emergencyApi.getAnalytics();
      debouncedSetActiveCallsCount(analytics.pendingCalls || 0);
      
      // Reset retry count on success
      retryCountRef.current = 0;
      
      // For notifications, we'll use a mock count for now
      // In a real app, this would come from a notifications API
      debouncedSetUnreadNotificationsCount(0);
      
    } catch (error) {
      retryCountRef.current += 1;
      console.error(`Failed to fetch navigation data (attempt ${retryCountRef.current}/${maxRetries}):`, error);
      setError('Failed to fetch navigation data');
      
      // Set fallback values
      setActiveCallsCount(0);
      setUnreadNotificationsCount(0);
    } finally {
      setLoading(false);
    }
  };

  // Handle real-time updates
  useEffect(() => {
    // Subscribe to new calls
    const handleNewCall = (call: any) => {
      console.log('New call received in navigation:', call);
      // Increment active calls count for new pending calls
      if (call.status === 'pending' || call.status === 'PENDING') {
        debouncedSetActiveCallsCount(prev => prev + 1);
      }
    };

    // Subscribe to notifications
    const handleNotification = (notification: any) => {
      console.log('Notification received in navigation:', notification);
      // Increment unread notifications count
      debouncedSetUnreadNotificationsCount(prev => prev + 1);
    };

    // Subscribe to call updates (to adjust active calls count)
    const handleCallUpdate = (call: any) => {
      console.log('Call update received in navigation:', call);
      // If a call is resolved or cancelled, decrement active calls
      if (call.status === 'resolved' || call.status === 'RESOLVED' || 
          call.status === 'cancelled' || call.status === 'CANCELLED') {
        debouncedSetActiveCallsCount(prev => Math.max(0, prev - 1));
      }
    };

    // Set up event listeners
    onNewCall(handleNewCall);
    onNotification(handleNotification);
    onCallUpdate(handleCallUpdate);

    // Initial fetch
    fetchNavigationData();

    // Set up periodic refresh as fallback
    if (retryCountRef.current < maxRetries) {
      intervalRef.current = setInterval(() => {
        // Only fetch if we haven't exceeded max retries
        if (retryCountRef.current < maxRetries) {
          fetchNavigationData();
        } else {
          console.log('Max retries reached, stopping periodic fetch');
          // Clear the interval to prevent further calls
          if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
          }
        }
      }, 30000); // Refresh every 30 seconds instead of 60
    }

    return () => {
      // Clear the interval if it exists
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      // Clear pending timeouts
      if (activeCallsTimeoutRef.current) {
        clearTimeout(activeCallsTimeoutRef.current);
      }
      if (notificationsTimeoutRef.current) {
        clearTimeout(notificationsTimeoutRef.current);
      }
      // Clean up WebSocket listeners
      const { removeListener } = useWebSocketService();
      removeListener('new_call', handleNewCall);
      removeListener('notification', handleNotification);
      removeListener('call_update', handleCallUpdate);
    };
  }, []); // Empty dependency array - run only once on mount

  return {
    activeCallsCount,
    unreadNotificationsCount,
    loading,
    error,
    isConnected: isConnected(),
    refresh: fetchNavigationData
  };
}

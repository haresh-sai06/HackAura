'use client';

import { useState, useEffect } from 'react';
import { emergencyApi } from '@/utils/api';
import { useWebSocketService } from '@/utils/websocket';

export function useNavigationData() {
  const [activeCallsCount, setActiveCallsCount] = useState(0);
  const [unreadNotificationsCount, setUnreadNotificationsCount] = useState(0);
  const [loading, setLoading] = useState(true);

  const { isConnected, onNewCall, onNotification } = useWebSocketService();

  // Fetch initial data
  const fetchNavigationData = async () => {
    try {
      setLoading(true);
      
      // Get analytics data for active calls count
      const analytics = await emergencyApi.getAnalytics();
      setActiveCallsCount(analytics.pendingCalls || 0);
      
      // For notifications, we'll use a mock count for now
      // In a real app, this would come from a notifications API
      setUnreadNotificationsCount(0);
      
    } catch (error) {
      console.error('Failed to fetch navigation data:', error);
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
        setActiveCallsCount(prev => prev + 1);
      }
    };

    // Subscribe to notifications
    const handleNotification = (notification: any) => {
      console.log('Notification received in navigation:', notification);
      // Increment unread notifications count
      setUnreadNotificationsCount(prev => prev + 1);
    };

    // Subscribe to call updates (to adjust active calls count)
    const handleCallUpdate = (call: any) => {
      console.log('Call update received in navigation:', call);
      // If a call is resolved or cancelled, decrement active calls
      if (call.status === 'resolved' || call.status === 'RESOLVED' || 
          call.status === 'cancelled' || call.status === 'CANCELLED') {
        setActiveCallsCount(prev => Math.max(0, prev - 1));
      }
    };

    // Set up event listeners
    onNewCall(handleNewCall);
    onNotification(handleNotification);

    // Initial fetch
    fetchNavigationData();

    // Set up periodic refresh as fallback
    const interval = setInterval(fetchNavigationData, 30000); // Refresh every 30 seconds

    return () => {
      clearInterval(interval);
    };
  }, [onNewCall, onNotification]);

  return {
    activeCallsCount,
    unreadNotificationsCount,
    loading,
    isConnected: isConnected(),
    refresh: fetchNavigationData
  };
}

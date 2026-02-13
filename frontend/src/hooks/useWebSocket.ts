'use client';

import { useEffect, useRef, useCallback } from 'react';
import { useWebSocket as useWebSocketService } from '@/utils/websocket';
import { useEmergencyStore } from '@/store/emergencyStore';
import { EmergencyCall, Notification } from '@/types/emergency';

interface UseWebSocketOptions {
  autoConnect?: boolean;
  reconnectOnMount?: boolean;
}

export function useWebSocket(options: UseWebSocketOptions = {}) {
  const { autoConnect = true, reconnectOnMount = true } = options;
  
  const {
    addCall,
    updateCall,
    addNotification,
    setCurrentUser,
    setError,
  } = useEmergencyStore();

  const {
    connect,
    disconnect,
    isConnected,
    onNewCall,
    onCallUpdate,
    onNotification,
    onUserStatus,
    onSystemUpdate,
    onAnalyticsUpdate,
    onStatsUpdate,
    removeAllListeners,
  } = useWebSocketService();

  const connectionRef = useRef<boolean>(false);
  const reconnectAttemptsRef = useRef<number>(0);
  const maxReconnectAttempts = 5;

  const handleNewCall = useCallback((call: EmergencyCall) => {
    addCall(call);
    addNotification({
      id: `call-${call.id}-${Date.now()}`,
      type: 'new_call' as any,
      title: 'New Emergency Call',
      message: `${call.callerName} - ${call.emergencyType}`,
      timestamp: new Date(),
      read: false,
      callId: String(call.id),
    });
  }, [addCall, addNotification]);

  const handleCallUpdate = useCallback((call: EmergencyCall) => {
    updateCall(String(call.id), call);
    addNotification({
      id: `update-${call.id}-${Date.now()}`,
      type: 'call_updated' as any,
      title: 'Call Updated',
      message: `Call ${call.id} status changed to ${call.status}`,
      timestamp: new Date(),
      read: false,
      callId: String(call.id),
    });
  }, [updateCall, addNotification]);

  const handleNotification = useCallback((notification: Notification) => {
    addNotification(notification);
  }, [addNotification]);

  const handleUserStatus = useCallback((data: { userId: string; status: boolean }) => {
    // Update user status in store or handle user presence
    console.log('User status update:', data);
  }, []);

  const handleSystemUpdate = useCallback((data: any) => {
    // Handle system-wide updates
    console.log('System update:', data);
  }, []);

  const connectWithRetry = useCallback(async () => {
    if (connectionRef.current) return;

    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        console.warn('No auth token found, skipping WebSocket connection');
        return;
      }

      await connect(token);
      connectionRef.current = true;
      reconnectAttemptsRef.current = 0;

      // Set up event listeners
      onNewCall(handleNewCall);
      onCallUpdate(handleCallUpdate);
      onNotification(handleNotification);
      onUserStatus(handleUserStatus);
      onSystemUpdate(handleSystemUpdate);
      onAnalyticsUpdate((data) => {
        console.log('Analytics update received:', data);
        // Handle analytics updates - could trigger store update
      });
      onStatsUpdate((data) => {
        console.log('Stats update received:', data);
        // Handle stats updates - could trigger store update
      });

      console.log('WebSocket connected successfully');
    } catch (error) {
      console.error('WebSocket connection failed:', error);
      
      if (reconnectAttemptsRef.current < maxReconnectAttempts) {
        reconnectAttemptsRef.current++;
        const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 10000);
        
        setTimeout(() => {
          console.log(`Attempting to reconnect (${reconnectAttemptsRef.current}/${maxReconnectAttempts})`);
          connectWithRetry();
        }, delay);
      } else {
        setError('Failed to establish WebSocket connection after multiple attempts');
      }
    }
  }, [
    connect,
    onNewCall,
    onCallUpdate,
    onNotification,
    onUserStatus,
    onSystemUpdate,
    onAnalyticsUpdate,
    onStatsUpdate,
    handleNewCall,
    handleCallUpdate,
    handleNotification,
    handleUserStatus,
    handleSystemUpdate,
    setError,
  ]);

  const disconnectSocket = useCallback(() => {
    if (!connectionRef.current) return;

    disconnect();
    removeAllListeners();
    connectionRef.current = false;
    reconnectAttemptsRef.current = 0;
    console.log('WebSocket disconnected');
  }, [disconnect, removeAllListeners]);

  // Auto-connect on mount
  useEffect(() => {
    if (autoConnect && reconnectOnMount) {
      connectWithRetry();
    }

    return () => {
      disconnectSocket();
    };
  }, [autoConnect, reconnectOnMount, connectWithRetry, disconnectSocket]);

  // Handle visibility change (reconnect when tab becomes visible)
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible' && !isConnected() && autoConnect) {
        connectWithRetry();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [isConnected, autoConnect, connectWithRetry]);

  // Handle online/offline events
  useEffect(() => {
    const handleOnline = () => {
      if (!isConnected() && autoConnect) {
        connectWithRetry();
      }
    };

    const handleOffline = () => {
      disconnectSocket();
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [isConnected, autoConnect, connectWithRetry, disconnectSocket]);

  return {
    isConnected: isConnected(),
    connect: connectWithRetry,
    disconnect: disconnectSocket,
    reconnectAttempts: reconnectAttemptsRef.current,
  };
}

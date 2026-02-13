'use client';

import { useEffect, useState, useCallback } from 'react';
import { useWebSocketService } from '@/utils/websocket';
import { emergencyApi } from '@/utils/api';
import { CallAnalytics } from '@/types/emergency';

export function useRealTimeAnalytics(refreshInterval: number = 30000) {
  const [analytics, setAnalytics] = useState<CallAnalytics | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const { isConnected, onAnalyticsUpdate, onStatsUpdate } = useWebSocketService();

  // Fetch analytics from API
  const fetchAnalytics = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await emergencyApi.getAnalytics();
      setAnalytics(data);
      setLastUpdated(new Date());
      console.log('Analytics data fetched:', data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch analytics';
      setError(errorMessage);
      console.error('Failed to fetch analytics:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Handle real-time analytics updates via WebSocket
  useEffect(() => {
    const handleAnalyticsUpdate = (data: CallAnalytics) => {
      console.log('Real-time analytics update received:', data);
      setAnalytics(data);
      setLastUpdated(new Date());
      setError(null);
    };

    const handleStatsUpdate = (data: any) => {
      console.log('Real-time stats update received:', data);
      // Update specific stats without full refresh
      if (analytics) {
        setAnalytics(prev => prev ? { ...prev, ...data } : null);
        setLastUpdated(new Date());
      }
    };

    // Subscribe to WebSocket events
    onAnalyticsUpdate(handleAnalyticsUpdate);
    onStatsUpdate(handleStatsUpdate);

    return () => {
      // Cleanup if needed
    };
  }, [onAnalyticsUpdate, onStatsUpdate, analytics]);

  // Initial fetch and periodic refresh
  useEffect(() => {
    fetchAnalytics();

    // Set up periodic polling as fallback
    const interval = setInterval(fetchAnalytics, refreshInterval);

    return () => clearInterval(interval);
  }, [fetchAnalytics, refreshInterval]);

  // Manual refresh function
  const refresh = useCallback(() => {
    fetchAnalytics();
  }, [fetchAnalytics]);

  return {
    analytics,
    loading,
    error,
    lastUpdated,
    isConnected,
    refresh,
  };
}

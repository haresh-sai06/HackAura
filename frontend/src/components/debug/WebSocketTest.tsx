'use client';

import { useState, useEffect } from 'react';
import { useWebSocketService } from '@/utils/websocket';

export function WebSocketTest() {
  const [logs, setLogs] = useState<string[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  
  const { connect, disconnect, onAnalyticsUpdate, onNewCall } = useWebSocketService();

  const addLog = (message: string) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  useEffect(() => {
    const testConnection = async () => {
      try {
        addLog('Attempting to connect to WebSocket...');
        
        const socket = await connect();
        setIsConnected(true);
        addLog('✅ WebSocket connected successfully!');
        
        // Test event listeners
        onAnalyticsUpdate((data) => {
          addLog(`📊 Analytics update received: ${JSON.stringify(data).substring(0, 100)}...`);
        });
        
        onNewCall((data) => {
          addLog(`📞 New call received: ${JSON.stringify(data).substring(0, 100)}...`);
        });
        
        // Test ping
        socket.emit('ping', { test: true });
        addLog('🏓 Ping sent');
        
      } catch (error) {
        addLog(`❌ Connection failed: ${error}`);
        setIsConnected(false);
      }
    };

    testConnection();

    return () => {
      disconnect();
      addLog('🔌 Disconnected');
    };
  }, [connect, disconnect, onAnalyticsUpdate, onNewCall]);

  return (
    <div className="fixed bottom-4 right-4 w-96 h-64 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-lg p-4 z-50">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-bold text-gray-900 dark:text-gray-100">WebSocket Debug</h3>
        <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
      </div>
      <div className="text-xs text-gray-600 dark:text-gray-400 overflow-y-auto h-48 space-y-1">
        {logs.map((log, index) => (
          <div key={index} className="border-b border-gray-200 dark:border-gray-700 pb-1">
            {log}
          </div>
        ))}
      </div>
    </div>
  );
}

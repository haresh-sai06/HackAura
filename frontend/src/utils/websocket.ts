import { io, Socket } from 'socket.io-client';
import { EmergencyCall, Notification } from '@/types/emergency';

class WebSocketService {
  private socket: Socket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  connect(token?: string): Promise<Socket> {
    return new Promise((resolve, reject) => {
      const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'http://localhost:8000';
      
      this.socket = io(wsUrl, {
        auth: token ? { token } : undefined,
        transports: ['websocket', 'polling'],
      });

      this.socket.on('connect', () => {
        console.log('WebSocket connected to HackAura backend');
        this.reconnectAttempts = 0;
        
        // Subscribe to analytics updates
        this.socket?.emit('subscribe_analytics', {});
        this.socket?.emit('subscribe_calls', {});
        
        resolve(this.socket!);
      });

      this.socket.on('connect_error', (error) => {
        console.error('WebSocket connection error:', error);
        this.handleReconnect();
        reject(error);
      });

      this.socket.on('disconnect', (reason) => {
        console.log('WebSocket disconnected:', reason);
        if (reason === 'io server disconnect') {
          // Server disconnected, reconnect manually
          this.socket?.connect();
        }
      });
    });
  }

  private handleReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
      
      setTimeout(() => {
        console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        this.socket?.connect();
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  // Event listeners
  onNewCall(callback: (call: EmergencyCall) => void): void {
    this.socket?.on('new_call', callback);
  }

  onCallUpdate(callback: (call: EmergencyCall) => void): void {
    this.socket?.on('call_update', callback);
  }

  onNotification(callback: (notification: Notification) => void): void {
    this.socket?.on('notification', callback);
  }

  onUserStatus(callback: (data: { userId: string; status: boolean }) => void): void {
    this.socket?.on('user_status', callback);
  }

  onSystemUpdate(callback: (data: any) => void): void {
    this.socket?.on('system_update', callback);
  }

  // Analytics event listeners
  onAnalyticsUpdate(callback: (data: any) => void): void {
    this.socket?.on('analytics_update', callback);
  }

  onStatsUpdate(callback: (data: any) => void): void {
    this.socket?.on('stats_update', callback);
  }

  // Event emitters
  emitCallUpdate(callId: string, updates: Partial<EmergencyCall>): void {
    this.socket?.emit('call_update', { callId, updates });
  }

  emitUserStatus(status: boolean): void {
    this.socket?.emit('user_status', { status });
  }

  emitJoinRoom(room: string): void {
    this.socket?.emit('join_room', room);
  }

  emitLeaveRoom(room: string): void {
    this.socket?.emit('leave_room', room);
  }

  // Remove listeners
  removeAllListeners(): void {
    this.socket?.removeAllListeners();
  }

  removeListener(event: string, listener: (...args: unknown[]) => void): void {
    this.socket?.off(event, listener);
  }

  // Get socket instance
  getSocket(): Socket | null {
    return this.socket;
  }

  // Check connection status
  isConnected(): boolean {
    return this.socket?.connected || false;
  }
}

export const wsService = new WebSocketService();

// Hook for using WebSocket in components
export const useWebSocketService = () => {
  const connect = (token?: string) => wsService.connect(token);
  const disconnect = () => wsService.disconnect();
  const isConnected = () => wsService.isConnected();
  
  return {
    connect,
    disconnect,
    isConnected,
    onNewCall: wsService.onNewCall.bind(wsService),
    onCallUpdate: wsService.onCallUpdate.bind(wsService),
    onNotification: wsService.onNotification.bind(wsService),
    onUserStatus: wsService.onUserStatus.bind(wsService),
    onSystemUpdate: wsService.onSystemUpdate.bind(wsService),
    onAnalyticsUpdate: wsService.onAnalyticsUpdate.bind(wsService),
    onStatsUpdate: wsService.onStatsUpdate.bind(wsService),
    emitCallUpdate: wsService.emitCallUpdate.bind(wsService),
    emitUserStatus: wsService.emitUserStatus.bind(wsService),
    emitJoinRoom: wsService.emitJoinRoom.bind(wsService),
    emitLeaveRoom: wsService.emitLeaveRoom.bind(wsService),
    removeAllListeners: wsService.removeAllListeners.bind(wsService),
    removeListener: wsService.removeListener.bind(wsService),
    getSocket: wsService.getSocket.bind(wsService),
  };
};

// Legacy export for compatibility
export const useWebSocket = useWebSocketService;

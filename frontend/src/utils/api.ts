import axios from 'axios';
import { EmergencyCall, CallAnalytics, CallFilter } from '@/types/emergency';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // Increased timeout to 10 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth token
api.interceptors.request.use((config) => {
  console.log('API Request:', config.method?.toUpperCase(), config.url);
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.config.url, response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', error.config?.url, error.response?.status, error.message);
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const emergencyApi = {
  // Calls
  getCalls: async (filters?: CallFilter): Promise<EmergencyCall[]> => {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value) {
          if (Array.isArray(value)) {
            value.forEach(v => params.append(key, v.toString()));
          } else if (value instanceof Date) {
            params.append(key, value.toISOString());
          } else if (typeof value === 'object' && value.start && value.end) {
            params.append(`${key}_start`, value.start.toISOString());
            params.append(`${key}_end`, value.end.toISOString());
          } else {
            params.append(key, value.toString());
          }
        }
      });
    }
    
    const queryString = params.toString();
    const url = queryString ? `/api/calls?${queryString}` : '/api/calls';
    const response = await api.get(url);
    return response.data;
  },

  getCall: async (id: string): Promise<EmergencyCall> => {
    const response = await api.get(`/api/calls/${id}`);
    return response.data;
  },

  createCall: async (call: Omit<EmergencyCall, 'id' | 'timestamp'>): Promise<EmergencyCall> => {
    const response = await api.post('/api/calls', call);
    return response.data;
  },

  updateCall: async (id: string, updates: Partial<EmergencyCall>): Promise<EmergencyCall> => {
    const response = await api.put(`/api/calls/${id}`, updates);
    return response.data;
  },

  deleteCall: async (id: string): Promise<void> => {
    await api.delete(`/api/calls/${id}`);
  },

  // Analytics
  getAnalytics: async (): Promise<CallAnalytics> => {
    const response = await api.get('/api/analytics');  // Use the comprehensive analytics endpoint
    return response.data;
  },

  // Audio
  uploadAudio: async (callId: string, audioFile: File): Promise<string> => {
    const formData = new FormData();
    formData.append('audio', audioFile);
    
    const response = await api.post(`/api/calls/${callId}/audio`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data.url;
  },

  getAudioUrl: (callId: string): string => {
    return `${API_BASE_URL}/api/calls/${callId}/audio`;
  },
};

export const authApi = {
  login: async (email: string, password: string): Promise<{ token: string; user: unknown }> => {
    const response = await api.post('/api/auth/login', { email, password });
    return response.data;
  },

  logout: async (): Promise<void> => {
    await api.post('/api/auth/logout');
  },

  refreshToken: async (): Promise<{ token: string }> => {
    const response = await api.post('/api/auth/refresh');
    return response.data;
  },

  getCurrentUser: async (): Promise<unknown> => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
};

export const notificationsApi = {
  getNotifications: async (): Promise<unknown[]> => {
    const response = await api.get('/api/notifications');
    return response.data;
  },

  markAsRead: async (id: string): Promise<void> => {
    await api.put(`/api/notifications/${id}/read`);
  },

  markAllAsRead: async (): Promise<void> => {
    await api.put('/api/notifications/read-all');
  },
};

import { create } from 'zustand';
import { EmergencyCall, CallFilter, CallStatus, User, Notification } from '@/types/emergency';

interface EmergencyStore {
  // State
  calls: EmergencyCall[];
  selectedCall: EmergencyCall | null;
  filters: CallFilter;
  currentUser: User | null;
  notifications: Notification[];
  isLoading: boolean;
  error: string | null;

  // Actions
  setCalls: (calls: EmergencyCall[]) => void;
  addCall: (call: EmergencyCall) => void;
  updateCall: (id: string, updates: Partial<EmergencyCall>) => void;
  removeCall: (id: string) => void;
  setSelectedCall: (call: EmergencyCall | null) => void;
  setFilters: (filters: CallFilter) => void;
  setCurrentUser: (user: User | null) => void;
  addNotification: (notification: Notification) => void;
  markNotificationRead: (id: string) => void;
  clearNotifications: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  
  // Computed
  filteredCalls: () => EmergencyCall[];
  unreadNotifications: () => Notification[];
  callsByStatus: (status: CallStatus) => EmergencyCall[];
}

export const useEmergencyStore = create<EmergencyStore>((set, get) => ({
  // Initial state
  calls: [],
  selectedCall: null,
  filters: {},
  currentUser: null,
  notifications: [],
  isLoading: false,
  error: null,

  // Actions
  setCalls: (calls) => set({ calls }),
  
  addCall: (call) => set((state) => ({ 
    calls: [call, ...state.calls] 
  })),
  
  updateCall: (id, updates) => set((state) => ({
    calls: state.calls.map(call => 
      call.id === id ? { ...call, ...updates } : call
    ),
    selectedCall: state.selectedCall?.id === id 
      ? { ...state.selectedCall, ...updates } 
      : state.selectedCall
  })),
  
  removeCall: (id) => set((state) => ({
    calls: state.calls.filter(call => call.id !== id),
    selectedCall: state.selectedCall?.id === id ? null : state.selectedCall
  })),
  
  setSelectedCall: (call) => set({ selectedCall: call }),
  
  setFilters: (filters) => set({ filters }),
  
  setCurrentUser: (user) => set({ currentUser: user }),
  
  addNotification: (notification) => set((state) => ({
    notifications: [notification, ...state.notifications]
  })),
  
  markNotificationRead: (id) => set((state) => ({
    notifications: state.notifications.map(notif => 
      notif.id === id ? { ...notif, read: true } : notif
    )
  })),
  
  clearNotifications: () => set({ notifications: [] }),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  setError: (error) => set({ error }),

  // Computed
  filteredCalls: () => {
    const { calls, filters } = get();
    return calls.filter(call => {
      if (filters.status && !filters.status.includes(call.status)) return false;
      if (filters.severity && !filters.severity.includes(call.severity)) return false;
      if (filters.emergencyType && !filters.emergencyType.includes(call.emergencyType)) return false;
      if (filters.dateRange) {
        const callDate = new Date(call.timestamp);
        if (callDate < filters.dateRange.start || callDate > filters.dateRange.end) return false;
      }
      return true;
    });
  },

  unreadNotifications: () => {
    const { notifications } = get();
    return notifications.filter(notif => !notif.read);
  },

  callsByStatus: (status) => {
    const { calls } = get();
    return calls.filter(call => call.status === status);
  }
}));

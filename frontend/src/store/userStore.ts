import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface UserProfile {
  name: string;
  email: string;
  phone: string;
  department: string;
  role: string;
  location: string;
}

export interface UserSettings {
  notifications: {
    emailNotifications: boolean;
    pushNotifications: boolean;
    smsNotifications: boolean;
    newCallAlerts: boolean;
    callAssignedAlerts: boolean;
    callResolvedAlerts: boolean;
    systemAlerts: boolean;
    weeklyReports: boolean;
  };
  appearance: {
    theme: 'light' | 'dark' | 'system';
    language: string;
    timezone: string;
    dateFormat: string;
    timeFormat: string;
    compactMode: boolean;
  };
  security: {
    twoFactorAuth: boolean;
    sessionTimeout: number;
    passwordExpiry: number;
    loginNotifications: boolean;
    apiAccess: boolean;
  };
  system: {
    apiEndpoint: string;
    websocketEndpoint: string;
    backupFrequency: string;
    logLevel: string;
    maxFileSize: number;
  };
}

interface UserStore {
  // State
  profile: UserProfile;
  settings: UserSettings;
  isLoading: boolean;
  error: string | null;

  // Actions
  updateProfile: (profile: Partial<UserProfile>) => void;
  updateSettings: (category: keyof UserSettings, settings: Partial<UserSettings[keyof UserSettings]>) => void;
  resetProfile: () => void;
  resetSettings: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  
  // Computed
  getDisplayName: () => string;
  getInitials: () => string;
}

const defaultProfile: UserProfile = {
  name: 'John Anderson',
  email: 'john.anderson@emergency.gov',
  phone: '+1-555-0101',
  department: 'Emergency Operations',
  role: 'Dispatcher',
  location: 'Central Command',
};

const defaultSettings: UserSettings = {
  notifications: {
    emailNotifications: true,
    pushNotifications: true,
    smsNotifications: false,
    newCallAlerts: true,
    callAssignedAlerts: true,
    callResolvedAlerts: true,
    systemAlerts: true,
    weeklyReports: false,
  },
  appearance: {
    theme: 'dark',
    language: 'english',
    timezone: 'UTC-5',
    dateFormat: 'MM/DD/YYYY',
    timeFormat: '12h',
    compactMode: false,
  },
  security: {
    twoFactorAuth: true,
    sessionTimeout: 30,
    passwordExpiry: 90,
    loginNotifications: true,
    apiAccess: false,
  },
  system: {
    apiEndpoint: 'http://localhost:8000',
    websocketEndpoint: 'ws://localhost:8000',
    backupFrequency: 'daily',
    logLevel: 'info',
    maxFileSize: 10,
  },
};

export const useUserStore = create<UserStore>()(
  persist(
    (set, get) => ({
      // Initial state
      profile: defaultProfile,
      settings: defaultSettings,
      isLoading: false,
      error: null,

      // Actions
      updateProfile: (profileUpdates) =>
        set((state) => ({
          profile: { ...state.profile, ...profileUpdates },
        })),

      updateSettings: (category, settingsUpdates) =>
        set((state) => ({
          settings: {
            ...state.settings,
            [category]: { ...state.settings[category], ...settingsUpdates },
          },
        })),

      resetProfile: () => set({ profile: defaultProfile }),

      resetSettings: () => set({ settings: defaultSettings }),

      setLoading: (loading) => set({ isLoading: loading }),

      setError: (error) => set({ error }),

      // Computed
      getDisplayName: () => {
        const { profile } = get();
        return profile.name;
      },

      getInitials: () => {
        const { profile } = get();
        return profile.name
          .split(' ')
          .map((word) => word.charAt(0))
          .join('')
          .toUpperCase()
          .slice(0, 2);
      },
    }),
    {
      name: 'hackaura-user-store',
      partialize: (state) => ({
        profile: state.profile,
        settings: state.settings,
      }),
    }
  )
);

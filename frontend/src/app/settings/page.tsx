'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useUserStore } from '@/store/userStore';
import { 
  User, 
  Bell, 
  Shield, 
  Palette, 
  Globe, 
  Database,
  Save,
  RotateCcw,
  Download,
  Upload
} from 'lucide-react';

// Simple Label component since we don't have it
const Label = ({ children, htmlFor, ...props }: React.LabelHTMLAttributes<HTMLLabelElement>) => (
  <label {...props} htmlFor={htmlFor} className={`text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 ${props.className || ''}`}>
    {children}
  </label>
);

// Simple Switch component since we don't have it
const Switch = ({ checked, onCheckedChange, ...props }: { 
  checked?: boolean; 
  onCheckedChange?: (checked: boolean) => void;
  className?: string;
}) => (
  <button
    type="button"
    role="switch"
    aria-checked={checked}
    className={`inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50 ${checked ? 'bg-primary' : 'bg-input'} ${props.className || ''}`}
    data-state={checked ? 'checked' : 'unchecked'}
    onClick={() => onCheckedChange?.(!checked)}
    {...props}
  >
    <span
      className={`pointer-events-none block h-5 w-5 rounded-full bg-background shadow-lg ring-0 transition-transform ${checked ? 'translate-x-5' : 'translate-x-0'}`}
    />
  </button>
);

// Simple Tabs component since we don't have it
const Tabs = ({ children, value, onValueChange, ...props }: {
  children: React.ReactNode;
  value?: string;
  onValueChange?: (value: string) => void;
  className?: string;
}) => {
  const [activeTab, setActiveTab] = useState(value || 'profile');
  
  const handleTabChange = (newValue: string) => {
    setActiveTab(newValue);
    onValueChange?.(newValue);
  };
  
  return (
    <div {...props} className={`w-full ${props.className || ''}`}>
      {React.Children.map(children, (child) => {
        if (React.isValidElement(child)) {
          if (child.type === TabsList) {
            return React.cloneElement(child as React.ReactElement<any>, { activeTab, onTabChange: handleTabChange });
          }
          if (child.type === TabsContent) {
            return React.cloneElement(child as React.ReactElement<any>, { activeTab });
          }
        }
        return child;
      })}
    </div>
  );
};

const TabsList = ({ children, activeTab, onTabChange, ...props }: {
  children: React.ReactNode;
  activeTab?: string;
  onTabChange?: (value: string) => void;
  className?: string;
}) => (
  <div {...props} className={`inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground ${props.className || ''}`}>
    {React.Children.map(children, (child) => {
      if (React.isValidElement(child) && child.type === TabsTrigger) {
        return React.cloneElement(child as React.ReactElement<any>, { 
          isActive: activeTab === (child.props as any).value,
          onClick: () => onTabChange?.((child.props as any).value)
        });
      }
      return child;
    })}
  </div>
);

const TabsTrigger = ({ children, value, isActive, onClick, ...props }: {
  children: React.ReactNode;
  value: string;
  isActive?: boolean;
  onClick?: () => void;
  className?: string;
}) => (
  <button
    type="button"
    {...props}
    onClick={onClick}
    className={`inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ${
      isActive 
        ? 'bg-background text-foreground shadow-sm' 
        : 'text-muted-foreground hover:text-foreground'
    } ${props.className || ''}`}
    data-state={isActive ? 'active' : 'inactive'}
  >
    {children}
  </button>
);

const TabsContent = ({ children, value, activeTab, ...props }: {
  children: React.ReactNode;
  value: string;
  activeTab?: string;
  className?: string;
}) => {
  if (activeTab !== value) return null;
  
  return (
    <div
      {...props}
      className={`mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ${props.className || ''}`}
      data-state={activeTab === value ? 'active' : 'inactive'}
    >
      {children}
    </div>
  );
};

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('profile');
  
  // Use the user store
  const {
    profile,
    settings,
    updateProfile,
    updateSettings,
    resetProfile,
    resetSettings,
    isLoading,
    setLoading,
    error,
    setError
  } = useUserStore();

  const [saving, setSaving] = useState(false);

  const handleSave = async (section: string) => {
    setSaving(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      console.log(`Saving ${section} settings...`);
      // Store is already updated through the updateProfile/updateSettings calls
      // Show success message
    } catch (error) {
      console.error('Failed to save settings:', error);
      setError('Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  const handleReset = (section: string) => {
    if (confirm(`Are you sure you want to reset ${section} settings to defaults?`)) {
      if (section === 'profile') {
        resetProfile();
      } else {
        resetSettings();
      }
      console.log(`Reset ${section} settings to defaults`);
    }
  };

  const handleExport = () => {
    const settingsData = {
      profile,
      settings,
    };
    const blob = new Blob([JSON.stringify(settingsData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'hackaura-settings.json';
    a.click();
  };

  const handleImport = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const settingsData = JSON.parse(e.target?.result as string);
          if (settingsData.profile) {
            updateProfile(settingsData.profile);
          }
          if (settingsData.settings) {
            // Update each settings category
            Object.keys(settingsData.settings).forEach((category) => {
              if (category in settings) {
                updateSettings(category as keyof typeof settings, settingsData.settings[category]);
              }
            });
          }
          console.log('Settings imported successfully');
        } catch (error) {
          console.error('Failed to import settings:', error);
          setError('Failed to import settings');
        }
      };
      reader.readAsText(file);
    }
  };

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-black">Settings</h1>
          <div className="flex gap-2">
            <Button variant="outline" onClick={handleExport}>
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
            <label className="cursor-pointer">
              <Button variant="outline" asChild>
                <span>
                  <Upload className="h-4 w-4 mr-2" />
                  Import
                </span>
              </Button>
              <input type="file" accept=".json" onChange={handleImport} className="hidden" />
            </label>
          </div>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="profile" className="flex items-center gap-2">
              <User className="h-4 w-4" />
              Profile
            </TabsTrigger>
            <TabsTrigger value="notifications" className="flex items-center gap-2">
              <Bell className="h-4 w-4" />
              Notifications
            </TabsTrigger>
            <TabsTrigger value="appearance" className="flex items-center gap-2">
              <Palette className="h-4 w-4" />
              Appearance
            </TabsTrigger>
            <TabsTrigger value="security" className="flex items-center gap-2">
              <Shield className="h-4 w-4" />
              Security
            </TabsTrigger>
            <TabsTrigger value="system" className="flex items-center gap-2">
              <Database className="h-4 w-4" />
              System
            </TabsTrigger>
          </TabsList>

          {/* Profile Settings */}
          <TabsContent value="profile">
            <Card className="bg-white border border-gray-200 hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle>Profile Settings</CardTitle>
                <CardDescription>Manage your personal information and preferences</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="name">Full Name</Label>
                      <Input
                        id="name"
                        value={profile.name}
                        onChange={(e) => updateProfile({ name: e.target.value })}
                      />
                    </div>
                    <div>
                      <Label htmlFor="email">Email Address</Label>
                      <Input
                        id="email"
                        type="email"
                        value={profile.email}
                        onChange={(e) => updateProfile({ email: e.target.value })}
                      />
                    </div>
                    <div>
                      <Label htmlFor="phone">Phone Number</Label>
                      <Input
                        id="phone"
                        value={profile.phone}
                        onChange={(e) => updateProfile({ phone: e.target.value })}
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="department">Department</Label>
                      <Select value={profile.department} onValueChange={(value) => updateProfile({ department: value })}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="Emergency Operations">Emergency Operations</SelectItem>
                          <SelectItem value="Medical Unit">Medical Unit</SelectItem>
                          <SelectItem value="Fire Department">Fire Department</SelectItem>
                          <SelectItem value="Police Unit">Police Unit</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label htmlFor="role">Role</Label>
                      <Select value={profile.role} onValueChange={(value) => updateProfile({ role: value })}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="Dispatcher">Dispatcher</SelectItem>
                          <SelectItem value="Responder">Responder</SelectItem>
                          <SelectItem value="Supervisor">Supervisor</SelectItem>
                          <SelectItem value="Admin">Admin</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label htmlFor="location">Location</Label>
                      <Input
                        id="location"
                        value={profile.location}
                        onChange={(e) => updateProfile({ location: e.target.value })}
                      />
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <Button onClick={() => handleSave('profile')} disabled={saving}>
                    <Save className="h-4 w-4 mr-2" />
                    {saving ? 'Saving...' : 'Save Changes'}
                  </Button>
                  <Button variant="outline" onClick={() => handleReset('profile')}>
                    <RotateCcw className="h-4 w-4 mr-2" />
                    Reset to Default
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Notification Settings */}
          <TabsContent value="notifications">
            <Card className="bg-white border border-gray-200 hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle>Notification Preferences</CardTitle>
                <CardDescription>Choose how you want to receive notifications</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold">Notification Channels</h3>
                    
                    <div className="flex items-center justify-between">
                      <Label htmlFor="emailNotifications">Email Notifications</Label>
                      <Switch
                        checked={settings.notifications.emailNotifications}
                        onCheckedChange={(checked) => updateSettings('notifications', { emailNotifications: checked })}
                      />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <Label htmlFor="pushNotifications">Push Notifications</Label>
                      <Switch
                        checked={settings.notifications.pushNotifications}
                        onCheckedChange={(checked) => updateSettings('notifications', { pushNotifications: checked })}
                      />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <Label htmlFor="smsNotifications">SMS Notifications</Label>
                      <Switch
                        checked={settings.notifications.smsNotifications}
                        onCheckedChange={(checked) => updateSettings('notifications', { smsNotifications: checked })}
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold">Alert Types</h3>
                    
                    <div className="flex items-center justify-between">
                      <Label htmlFor="newCallAlerts">New Call Alerts</Label>
                      <Switch
                        checked={settings.notifications.newCallAlerts}
                        onCheckedChange={(checked) => updateSettings('notifications', { newCallAlerts: checked })}
                      />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <Label htmlFor="callAssignedAlerts">Call Assigned Alerts</Label>
                      <Switch
                        checked={settings.notifications.callAssignedAlerts}
                        onCheckedChange={(checked) => updateSettings('notifications', { callAssignedAlerts: checked })}
                      />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <Label htmlFor="callResolvedAlerts">Call Resolved Alerts</Label>
                      <Switch
                        checked={settings.notifications.callResolvedAlerts}
                        onCheckedChange={(checked) => updateSettings('notifications', { callResolvedAlerts: checked })}
                      />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <Label htmlFor="systemAlerts">System Alerts</Label>
                      <Switch
                        checked={settings.notifications.systemAlerts}
                        onCheckedChange={(checked) => updateSettings('notifications', { systemAlerts: checked })}
                      />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <Label htmlFor="weeklyReports">Weekly Reports</Label>
                      <Switch
                        checked={settings.notifications.weeklyReports}
                        onCheckedChange={(checked) => updateSettings('notifications', { weeklyReports: checked })}
                      />
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <Button onClick={() => handleSave('notifications')} disabled={saving}>
                    <Save className="h-4 w-4 mr-2" />
                    {saving ? 'Saving...' : 'Save Changes'}
                  </Button>
                  <Button variant="outline" onClick={() => handleReset('notifications')}>
                    <RotateCcw className="h-4 w-4 mr-2" />
                    Reset to Default
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Appearance Settings */}
          <TabsContent value="appearance">
            <Card className="bg-white border border-gray-200 hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle>Appearance Settings</CardTitle>
                <CardDescription>Customize the look and feel of your dashboard</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="theme">Theme</Label>
                      <Select value={settings.appearance.theme} onValueChange={(value) => updateSettings('appearance', { theme: value as 'light' | 'dark' | 'system' })}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="light">Light</SelectItem>
                          <SelectItem value="dark">Dark</SelectItem>
                          <SelectItem value="system">System</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label htmlFor="language">Language</Label>
                      <Select value={settings.appearance.language} onValueChange={(value) => updateSettings('appearance', { language: value })}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="english">English</SelectItem>
                          <SelectItem value="spanish">Spanish</SelectItem>
                          <SelectItem value="french">French</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label htmlFor="timezone">Timezone</Label>
                      <Select value={settings.appearance.timezone} onValueChange={(value) => updateSettings('appearance', { timezone: value })}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="UTC-8">UTC-8 (PST)</SelectItem>
                          <SelectItem value="UTC-5">UTC-5 (EST)</SelectItem>
                          <SelectItem value="UTC+0">UTC+0 (GMT)</SelectItem>
                          <SelectItem value="UTC+1">UTC+1 (CET)</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="dateFormat">Date Format</Label>
                      <Select value={settings.appearance.dateFormat} onValueChange={(value) => updateSettings('appearance', { dateFormat: value })}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="MM/DD/YYYY">MM/DD/YYYY</SelectItem>
                          <SelectItem value="DD/MM/YYYY">DD/MM/YYYY</SelectItem>
                          <SelectItem value="YYYY-MM-DD">YYYY-MM-DD</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label htmlFor="timeFormat">Time Format</Label>
                      <Select value={settings.appearance.timeFormat} onValueChange={(value) => updateSettings('appearance', { timeFormat: value })}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="12h">12-hour</SelectItem>
                          <SelectItem value="24h">24-hour</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <Label htmlFor="compactMode">Compact Mode</Label>
                      <Switch
                        checked={settings.appearance.compactMode}
                        onCheckedChange={(checked) => updateSettings('appearance', { compactMode: checked })}
                      />
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <Button onClick={() => handleSave('appearance')} disabled={saving}>
                    <Save className="h-4 w-4 mr-2" />
                    {saving ? 'Saving...' : 'Save Changes'}
                  </Button>
                  <Button variant="outline" onClick={() => handleReset('appearance')}>
                    <RotateCcw className="h-4 w-4 mr-2" />
                    Reset to Default
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Security Settings */}
          <TabsContent value="security">
            <Card className="bg-white border border-gray-200 hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle>Security Settings</CardTitle>
                <CardDescription>Manage your account security and access controls</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <Label htmlFor="twoFactorAuth">Two-Factor Authentication</Label>
                        <p className="text-sm text-gray-600">
                          Add an extra layer of security to your account
                        </p>
                      </div>
                      <Switch
                        checked={settings.security.twoFactorAuth}
                        onCheckedChange={(checked) => updateSettings('security', { twoFactorAuth: checked })}
                      />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <Label htmlFor="loginNotifications">Login Notifications</Label>
                        <p className="text-sm text-gray-600">
                          Get notified when someone logs into your account
                        </p>
                      </div>
                      <Switch
                        checked={settings.security.loginNotifications}
                        onCheckedChange={(checked) => updateSettings('security', { loginNotifications: checked })}
                      />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <Label htmlFor="apiAccess">API Access</Label>
                        <p className="text-sm text-gray-600">
                          Allow third-party applications to access your account
                        </p>
                      </div>
                      <Switch
                        checked={settings.security.apiAccess}
                        onCheckedChange={(checked) => updateSettings('security', { apiAccess: checked })}
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="sessionTimeout">Session Timeout (minutes)</Label>
                      <Input
                        id="sessionTimeout"
                        type="number"
                        value={settings.security.sessionTimeout}
                        onChange={(e) => updateSettings('security', { sessionTimeout: parseInt(e.target.value) })}
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="passwordExpiry">Password Expiry (days)</Label>
                      <Input
                        id="passwordExpiry"
                        type="number"
                        value={settings.security.passwordExpiry}
                        onChange={(e) => updateSettings('security', { passwordExpiry: parseInt(e.target.value) })}
                      />
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <Button onClick={() => handleSave('security')} disabled={saving}>
                    <Save className="h-4 w-4 mr-2" />
                    {saving ? 'Saving...' : 'Save Changes'}
                  </Button>
                  <Button variant="outline" onClick={() => handleReset('security')}>
                    <RotateCcw className="h-4 w-4 mr-2" />
                    Reset to Default
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* System Settings */}
          <TabsContent value="system">
            <Card className="bg-white border border-gray-200 hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle>System Configuration</CardTitle>
                <CardDescription>Configure system endpoints and technical settings</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="apiEndpoint">API Endpoint</Label>
                      <Input
                        id="apiEndpoint"
                        value={settings.system.apiEndpoint}
                        onChange={(e) => updateSettings('system', { apiEndpoint: e.target.value })}
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="websocketEndpoint">WebSocket Endpoint</Label>
                      <Input
                        id="websocketEndpoint"
                        value={settings.system.websocketEndpoint}
                        onChange={(e) => updateSettings('system', { websocketEndpoint: e.target.value })}
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="backupFrequency">Backup Frequency</Label>
                      <Select value={settings.system.backupFrequency} onValueChange={(value) => updateSettings('system', { backupFrequency: value })}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="hourly">Hourly</SelectItem>
                          <SelectItem value="daily">Daily</SelectItem>
                          <SelectItem value="weekly">Weekly</SelectItem>
                          <SelectItem value="monthly">Monthly</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="logLevel">Log Level</Label>
                      <Select value={settings.system.logLevel} onValueChange={(value) => updateSettings('system', { logLevel: value })}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="error">Error</SelectItem>
                          <SelectItem value="warn">Warning</SelectItem>
                          <SelectItem value="info">Info</SelectItem>
                          <SelectItem value="debug">Debug</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label htmlFor="maxFileSize">Max File Size (MB)</Label>
                      <Input
                        id="maxFileSize"
                        type="number"
                        value={settings.system.maxFileSize}
                        onChange={(e) => updateSettings('system', { maxFileSize: parseInt(e.target.value) })}
                      />
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <Button onClick={() => handleSave('system')} disabled={saving}>
                    <Save className="h-4 w-4 mr-2" />
                    {saving ? 'Saving...' : 'Save Changes'}
                  </Button>
                  <Button variant="outline" onClick={() => handleReset('system')}>
                    <RotateCcw className="h-4 w-4 mr-2" />
                    Reset to Default
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}

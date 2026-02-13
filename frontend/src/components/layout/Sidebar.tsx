'use client';

import { useState } from 'react';
import { usePathname } from 'next/navigation';
import { 
  Phone, 
  BarChart3, 
  Settings, 
  Users, 
  Bell, 
  LogOut,
  Menu,
  X
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface SidebarProps {
  className?: string;
  isCollapsed?: boolean;
  onToggle?: () => void;
}

const navigation = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: BarChart3,
  },
  {
    name: 'Emergency Calls',
    href: '/calls',
    icon: Phone,
    badge: 3, // Number of active calls
  },
  {
    name: 'Analytics',
    href: '/analytics',
    icon: BarChart3,
  },
  {
    name: 'Team',
    href: '/team',
    icon: Users,
  },
  {
    name: 'Notifications',
    href: '/notifications',
    icon: Bell,
    badge: 5, // Number of unread notifications
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: Settings,
  },
];

export function Sidebar({ className, isCollapsed = false, onToggle }: SidebarProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const pathname = usePathname();

  // Function to check if a route is active
  const isActive = (href: string) => {
    return pathname === href;
  };

  const NavItem = ({ item }: { item: typeof navigation[0] }) => {
    const Icon = item.icon;
    const active = isActive(item.href);
    
    return (
      <a
        href={item.href}
        className={cn(
          // Base styles with professional dark theme
          'flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all duration-200 ease-in-out hover:translate-x-1',
          // Dark theme colors
          'text-slate-200 hover:bg-slate-800',
          // Active state - DYNAMIC ROUTE DETECTION
          active
            ? 'bg-blue-600 text-white shadow-lg'
            : 'text-slate-400',
          // Collapsed state
          isCollapsed && 'justify-center'
        )}
      >
        <Icon className={cn(
          'h-4 w-4 transition-colors',
          active ? 'text-white' : 'text-slate-400'
        )} />
        {!isCollapsed && (
          <>
            <span className="flex-1">{item.name}</span>
            {item.badge && (
              <Badge variant="secondary" className="h-5 w-5 rounded-full p-0 text-xs bg-blue-500 text-white">
                {item.badge}
              </Badge>
            )}
          </>
        )}
      </a>
    );
  };

  return (
    <>
      {/* Mobile menu button */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <Button
          variant="outline"
          size="icon"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
        </Button>
      </div>

      {/* Sidebar */}
      <div
        className={cn(
          // Professional dark theme background
          'fixed inset-y-0 left-0 z-40 w-64 bg-slate-900 border-r border-slate-700 transition-transform duration-300 ease-in-out lg:translate-x-0',
          isCollapsed && 'w-16',
          mobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
          className
        )}
      >
        <div className="flex h-full flex-col">
          {/* Header */}
          <div className="flex h-16 items-center gap-3 border-b border-slate-700 px-4">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-lg bg-blue-600 flex items-center justify-center shadow-lg">
                <Phone className="h-4 w-4 text-white" />
              </div>
              {!isCollapsed && (
                <span className="text-lg font-semibold tracking-wide text-slate-200">HackAura</span>
              )}
            </div>
            {!isCollapsed && onToggle && (
              <Button
                variant="ghost"
                size="icon"
                onClick={onToggle}
                className="ml-auto text-slate-400 hover:text-slate-200 hover:bg-slate-800"
              >
                <Menu className="h-4 w-4" />
              </Button>
            )}
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-2 p-4">
            {navigation.map((item) => (
              <NavItem key={item.name} item={item} />
            ))}
          </nav>

          {/* User section */}
          <div className="border-t border-slate-700 p-4">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-full bg-slate-700 flex items-center justify-center">
                <Users className="h-4 w-4 text-slate-300" />
              </div>
              {!isCollapsed && (
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold truncate text-slate-200">John Doe</p>
                  <p className="text-xs text-slate-400 truncate">Dispatcher</p>
                </div>
              )}
            </div>
            {!isCollapsed && (
              <div className="mt-3 flex flex-col gap-2">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-red-500"></div>
                  <span className="text-xs text-slate-400">1 Issue</span>
                </div>
                <Button variant="ghost" size="icon" className="w-full text-slate-400 hover:text-slate-200 hover:bg-slate-800">
                  <LogOut className="h-4 w-4" />
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile overlay */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 z-30 bg-background/80 backdrop-blur-sm lg:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}
    </>
  );
}

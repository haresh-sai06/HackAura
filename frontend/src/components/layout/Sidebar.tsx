'use client';

import { useState } from 'react';
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
    current: true,
  },
  {
    name: 'Emergency Calls',
    href: '/calls',
    icon: Phone,
    current: false,
    badge: 3, // Number of active calls
  },
  {
    name: 'Analytics',
    href: '/analytics',
    icon: BarChart3,
    current: false,
  },
  {
    name: 'Team',
    href: '/team',
    icon: Users,
    current: false,
  },
  {
    name: 'Notifications',
    href: '/notifications',
    icon: Bell,
    current: false,
    badge: 5, // Number of unread notifications
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: Settings,
    current: false,
  },
];

export function Sidebar({ className, isCollapsed = false, onToggle }: SidebarProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const NavItem = ({ item }: { item: typeof navigation[0] }) => {
    const Icon = item.icon;
    
    return (
      <a
        href={item.href}
        className={cn(
          'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground',
          item.current
            ? 'bg-accent text-accent-foreground'
            : 'text-muted-foreground',
          isCollapsed && 'justify-center'
        )}
      >
        <Icon className="h-4 w-4" />
        {!isCollapsed && (
          <>
            <span className="flex-1">{item.name}</span>
            {item.badge && (
              <Badge variant="secondary" className="h-5 w-5 rounded-full p-0 text-xs">
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
          'fixed inset-y-0 left-0 z-40 w-64 bg-background border-r transition-transform duration-300 ease-in-out lg:translate-x-0',
          isCollapsed && 'w-16',
          mobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
          className
        )}
      >
        <div className="flex h-full flex-col">
          {/* Header */}
          <div className="flex h-16 items-center gap-2 border-b px-4">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
                <Phone className="h-4 w-4 text-primary-foreground" />
              </div>
              {!isCollapsed && (
                <span className="text-lg font-semibold">HackAura</span>
              )}
            </div>
            {!isCollapsed && onToggle && (
              <Button
                variant="ghost"
                size="icon"
                onClick={onToggle}
                className="ml-auto"
              >
                <Menu className="h-4 w-4" />
              </Button>
            )}
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 p-4">
            {navigation.map((item) => (
              <NavItem key={item.name} item={item} />
            ))}
          </nav>

          {/* User section */}
          <div className="border-t p-4">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center">
                <Users className="h-4 w-4" />
              </div>
              {!isCollapsed && (
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">John Doe</p>
                  <p className="text-xs text-muted-foreground truncate">Dispatcher</p>
                </div>
              )}
            </div>
            {!isCollapsed && (
              <Button variant="ghost" size="icon" className="mt-2 w-full">
                <LogOut className="h-4 w-4" />
              </Button>
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

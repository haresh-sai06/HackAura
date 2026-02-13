'use client';

import { useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { 
  Phone, 
  BarChart3, 
  Settings, 
  Users, 
  Bell, 
  LogOut,
  Menu,
  X,
  Wifi,
  WifiOff
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useNavigationData } from '@/hooks/useNavigationData';
import { useUserStore } from '@/store/userStore';

interface SidebarProps {
  className?: string;
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
    badgeKey: 'activeCalls', // Dynamic badge key
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
    badgeKey: 'notifications', // Dynamic badge key
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: Settings,
  },
];

export function Sidebar({ className }: SidebarProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const pathname = usePathname();
  const router = useRouter();
  
  // Get real-time navigation data
  const { activeCallsCount, unreadNotificationsCount, loading, isConnected } = useNavigationData();
  
  // Get user profile data
  const { profile, getInitials } = useUserStore();

  // Function to check if a route is active
  const isActive = (href: string) => {
    return pathname === href;
  };

  const NavItem = ({ item }: { item: typeof navigation[0] }) => {
    const Icon = item.icon;
    const active = isActive(item.href);
    const [isHovered, setIsHovered] = useState(false);
    
    // Get badge value based on badgeKey
    const getBadgeValue = () => {
      if (item.badgeKey === 'activeCalls') {
        return activeCallsCount;
      } else if (item.badgeKey === 'notifications') {
        return unreadNotificationsCount;
      }
      return undefined;
    };
    
    const badgeValue = getBadgeValue();
    
    const handleClick = (e: React.MouseEvent) => {
      e.preventDefault();
      router.push(item.href);
      setMobileMenuOpen(false); // Close mobile menu after navigation
    };
    
    return (
      <div
        className="relative"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <a
          href={item.href}
          onClick={handleClick}
          className={cn(
            // Enhanced base styles with professional dark theme
            'flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all duration-200 ease-out relative overflow-hidden',
            // Improved hover effects with scale and glow
            'transform hover:scale-[1.02] hover:shadow-lg',
            // Dark theme colors with glass effect
            'text-slate-300/90 hover:bg-slate-700/60 hover:text-slate-100',
            // Active state with enhanced styling
            active
              ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-xl border border-blue-500/40 scale-[1.02]'
              : 'text-slate-400/80 hover:text-slate-200',
          )}
        >
          
          <Icon className={cn(
            'h-4 w-4 transition-all duration-200 flex-shrink-0 relative z-10',
            active 
              ? 'text-white scale-105 drop-shadow-sm' 
              : 'text-slate-400 group-hover:text-slate-200 group-hover:scale-105 group-hover:drop-shadow-sm'
          )} />
          
          <div className="flex-1 flex items-center justify-between relative z-10">
            <span className="font-medium truncate">{item.name}</span>
            {badgeValue !== undefined && badgeValue > 0 && (
              <Badge 
                variant="secondary" 
                className={cn(
                  'inline-flex items-center justify-center min-w-[20px] h-5 px-2 text-xs font-semibold rounded-full flex-shrink-0 shadow-md transition-all duration-200',
                  'bg-gradient-to-r from-red-500 to-orange-500 text-white',
                  isHovered && 'scale-105 shadow-lg'
                )}
              >
                {loading ? '...' : badgeValue}
              </Badge>
            )}
          </div>
          
          {/* Active state indicator */}
          {active && (
            <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-white rounded-r-full shadow-lg" />
          )}
        </a>
      </div>
    );
  };

  return (
    <>
      {/* Mobile menu button - always visible on mobile, hidden on desktop */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <Button
          variant="outline"
          size="icon"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="bg-slate-800 border-slate-600 text-slate-200 hover:bg-slate-700"
        >
          {mobileMenuOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
        </Button>
      </div>


      {/* Mobile overlay - closes sidebar when clicked */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/50 backdrop-blur-sm lg:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={cn(
          // Enhanced professional dark theme background
          'fixed inset-y-0 left-0 z-40 w-64 bg-slate-900/95 backdrop-blur-xl border-r border-slate-700/50 transition-all duration-300 ease-in-out lg:translate-x-0 shadow-2xl',
          mobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
          className
        )}
      >
        <div className="flex h-full flex-col">
          {/* Header */}
          <div className="flex h-16 items-center gap-3 border-b border-slate-700/50 px-4 min-w-0 bg-slate-800/50">
            <div className="flex items-center gap-3 min-w-0">
              <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-lg flex-shrink-0 transition-transform hover:scale-105">
                <Phone className="h-4 w-4 text-white" />
              </div>
              <span className="text-lg font-semibold tracking-wide text-slate-100 truncate min-w-0">HackAura</span>
            </div>
            
            {/* Mobile close button - always visible on mobile */}
            <div className="lg:hidden ml-auto">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setMobileMenuOpen(false)}
                className="text-slate-400 hover:text-slate-100 hover:bg-slate-700/50 transition-colors-smooth"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 p-4">
            {navigation.map((item) => (
              <NavItem key={item.name} item={item} />
            ))}
          </nav>

          {/* User section */}
          <div className="border-t border-slate-700/50 p-4 bg-slate-800/30">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-full bg-gradient-to-br from-slate-600 to-slate-700 flex items-center justify-center shadow-md">
                <span className="text-xs font-semibold text-slate-200">{getInitials()}</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold truncate text-slate-100">{profile.name}</p>
                <p className="text-xs text-slate-400 truncate">{profile.role}</p>
              </div>
              <Button variant="ghost" size="icon" className="text-slate-400 hover:text-slate-100 hover:bg-slate-700/50 transition-colors-smooth">
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

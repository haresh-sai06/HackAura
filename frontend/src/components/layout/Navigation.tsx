'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';

interface NavigationItem {
  id: 'overview' | 'calls' | 'analytics';
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: number;
  current?: boolean;
}

interface NavigationProps {
  items: NavigationItem[];
  currentView: string;
  onViewChange: (view: 'overview' | 'calls' | 'analytics') => void;
  className?: string;
}

export function Navigation({ items, currentView, onViewChange, className }: NavigationProps) {
  const [hoveredItem, setHoveredItem] = useState<string | null>(null);
  
  return (
    <nav className={cn('flex items-center gap-2 mb-6', className)}>
      {items.map((item) => {
        const Icon = item.icon;
        const isHovered = hoveredItem === item.id;
        
        return (
          <div
            key={item.id}
            className="relative"
            onMouseEnter={() => setHoveredItem(item.id)}
            onMouseLeave={() => setHoveredItem(null)}
          >
            <button
              onClick={() => onViewChange(item.id)}
              className={cn(
                'flex items-center gap-3 rounded-lg px-4 py-2 text-sm font-medium transition-all duration-300 ease-out relative overflow-hidden',
                'transform hover:scale-[1.02] hover:shadow-md',
                currentView === item.id
                  ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg border border-blue-500/30 scale-[1.02]'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-700',
                // Subtle background animation on hover
                isHovered && currentView !== item.id && 'before:absolute before:inset-0 before:bg-gradient-to-r before:from-blue-500/10 before:to-purple-500/10 before:opacity-0 before:transition-opacity before:duration-300 hover:before:opacity-100'
              )}
            >
              {/* Hover glow effect */}
              {isHovered && currentView !== item.id && (
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5 rounded-lg animate-pulse" />
              )}
              
              <Icon className={cn(
                'h-4 w-4 transition-all duration-300 flex-shrink-0 relative z-10',
                currentView === item.id 
                  ? 'text-white scale-110 drop-shadow-sm' 
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:scale-105',
                isHovered && currentView !== item.id && 'animate-pulse'
              )} />
              
              <span className="font-medium relative z-10">{item.name}</span>
              
              {item.badge && (
                <span className={cn(
                  'ml-auto relative z-10 text-xs px-2 py-1 rounded-full font-semibold transition-all duration-300',
                  currentView === item.id
                    ? 'bg-white/20 text-white'
                    : 'bg-red-500 text-white animate-pulse',
                  isHovered && 'scale-110 shadow-lg'
                )}>
                  {item.badge}
                </span>
              )}
              
              {/* Active state indicator */}
              {currentView === item.id && (
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-5 bg-white rounded-r-full shadow-lg" />
              )}
            </button>
          </div>
        );
      })}
    </nav>
  );
}

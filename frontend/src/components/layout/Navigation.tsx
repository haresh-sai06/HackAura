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
  return (
    <nav className={cn('flex items-center gap-2 mb-6', className)}>
      {items.map((item) => {
        const Icon = item.icon;
        return (
          <button
            key={item.id}
            onClick={() => onViewChange(item.id)}
            className={cn(
              'flex items-center gap-3 rounded-lg px-4 py-2 text-sm font-medium transition-colors',
              currentView === item.id
                ? 'bg-primary text-primary-foreground'
                : 'text-muted-foreground hover:text-foreground hover:bg-muted'
            )}
          >
            <Icon className="h-4 w-4" />
            <span>{item.name}</span>
            {item.badge && (
              <span className="ml-auto bg-destructive text-destructive-foreground text-xs px-2 py-1 rounded-full">
                {item.badge}
              </span>
            )}
          </button>
        );
      })}
    </nav>
  );
}

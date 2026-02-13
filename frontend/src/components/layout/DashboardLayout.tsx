'use client';

import { useState } from 'react';
import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';
import { cn } from '@/lib/utils';

interface DashboardLayoutProps {
  children: React.ReactNode;
  className?: string;
}

export function DashboardLayout({ children, className }: DashboardLayoutProps) {
  return (
    <div className="flex h-screen bg-gradient-light-blue dark:bg-gradient-dark-gray transition-colors-smooth">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden ml-64">
        <Topbar />
        
        <main className="flex-1 overflow-auto">
          <div className="p-8 animate-fade-in">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

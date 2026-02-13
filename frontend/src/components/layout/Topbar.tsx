'use client';

import { Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';

interface TopbarProps {
  className?: string;
}

export function Topbar({ className }: TopbarProps) {
  return (
    <header className={`border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 ${className}`}>
      <div className="flex h-16 items-center justify-between px-6">
        {/* Search */}
        <div className="flex items-center gap-4 flex-1">
          <div className="relative w-full max-w-xl">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5 pointer-events-none" />
            <Input
              placeholder="Search calls, contacts, or locations..."
              className="w-full bg-white text-black placeholder:text-gray-500 border border-gray-300 rounded-lg py-3 pl-10 pr-4 shadow-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>
        </div>

        {/* Right side - Logo only */}
        <div className="flex items-center">
          <div className="text-xl font-bold text-primary">
            HackAura
          </div>
        </div>
      </div>
    </header>
  );
}

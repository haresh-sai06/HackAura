'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { LoadingSpinner } from '@/components/ui/loading-spinner';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to dashboard
    router.push('/dashboard');
  }, [router]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="text-center space-y-4">
        <LoadingSpinner size="lg" />
        <p className="text-muted-foreground">Loading HackAura...</p>
      </div>
    </div>
  );
}

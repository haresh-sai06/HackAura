'use client';

import { cn } from '@/lib/utils';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function LoadingSpinner({ size = 'md', className }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
  };

  return (
    <div
      className={cn(
        'animate-spin rounded-full border-2 border-current border-t-transparent',
        sizeClasses[size],
        className
      )}
      role="status"
      aria-label="Loading"
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
}

interface LoadingStateProps {
  isLoading: boolean;
  error?: string | null;
  children: React.ReactNode;
  fallback?: React.ReactNode;
  errorFallback?: React.ReactNode;
}

export function LoadingState({ 
  isLoading, 
  error, 
  children, 
  fallback, 
  errorFallback 
}: LoadingStateProps) {
  if (error) {
    return (
      errorFallback || (
        <div className="flex items-center justify-center p-8">
          <div className="text-center">
            <div className="text-destructive font-medium mb-2">Error</div>
            <div className="text-muted-foreground text-sm">{error}</div>
          </div>
        </div>
      )
    );
  }

  if (isLoading) {
    return (
      fallback || (
        <div className="flex items-center justify-center p-8">
          <LoadingSpinner />
        </div>
      )
    );
  }

  return <>{children}</>;
}

interface SkeletonProps {
  className?: string;
  children?: React.ReactNode;
}

export function Skeleton({ className, children, ...props }: SkeletonProps) {
  return (
    <div
      className={cn(
        'animate-pulse rounded-md bg-muted',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardSkeleton() {
  return (
    <div className="rounded-lg border p-6 space-y-4">
      <div className="flex items-center justify-between">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-4 w-16" />
      </div>
      <div className="space-y-2">
        <Skeleton className="h-3 w-full" />
        <Skeleton className="h-3 w-3/4" />
      </div>
      <div className="flex items-center gap-2">
        <Skeleton className="h-2 w-16" />
        <Skeleton className="h-2 w-12" />
      </div>
    </div>
  );
}

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-2">
      {Array.from({ length: rows }).map((_, index) => (
        <div key={index} className="flex items-center gap-4 p-4 border rounded">
          <Skeleton className="h-4 w-16" />
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-4 w-20" />
          <Skeleton className="h-4 w-12" />
          <Skeleton className="h-4 w-16" />
        </div>
      ))}
    </div>
  );
}

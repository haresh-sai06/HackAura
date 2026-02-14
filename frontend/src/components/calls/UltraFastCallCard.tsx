'use client';

import { useState, useEffect } from 'react';
import { Clock, Zap, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ultraFastApi, UltraFastCall } from '@/services/ultraFastApi';

interface UltraFastCallCardProps {
  call: UltraFastCall;
  className?: string;
}

const categoryColors = {
  'Medical': 'bg-gradient-to-r from-red-50 to-red-100 text-red-700 border-red-200 dark:from-red-900/50 dark:to-red-800 dark:text-red-200 dark:border-red-700',
  'Fire': 'bg-gradient-to-r from-orange-50 to-orange-100 text-orange-700 border-orange-200 dark:from-orange-900/50 dark:to-orange-800 dark:text-orange-200 dark:border-orange-700',
  'Crime': 'bg-gradient-to-r from-blue-50 to-blue-100 text-blue-700 border-blue-200 dark:from-blue-900/50 dark:to-blue-800 dark:text-blue-200 dark:border-blue-700',
  'Other': 'bg-gradient-to-r from-gray-50 to-gray-100 text-gray-700 border-gray-200 dark:from-gray-900/50 dark:to-gray-800 dark:text-gray-200 dark:border-gray-700',
};

const priorityColors = {
  1: 'bg-red-500 text-white animate-pulse',  // Critical
  2: 'bg-orange-500 text-white',           // High
  3: 'bg-yellow-500 text-white',           // Medium
  4: 'bg-blue-500 text-white',            // Low
  5: 'bg-gray-500 text-white',             // Very Low
};

const priorityLabels = {
  1: 'CRITICAL',
  2: 'HIGH',
  3: 'MEDIUM',
  4: 'LOW',
  5: 'VERY LOW',
};

export function UltraFastCallCard({ call, className }: UltraFastCallCardProps) {
  const [formattedTime, setFormattedTime] = useState<string>('');
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    if (call.created_at) {
      try {
        const date = new Date(call.created_at);
        setFormattedTime(date.toLocaleTimeString());
      } catch (error) {
        setFormattedTime('');
      }
    }
  }, [call.created_at]);

  const getPerformanceIndicator = (timeMs: number) => {
    if (timeMs < 10) return { color: 'text-green-600', icon: Zap, label: 'Ultra-Fast' };
    if (timeMs < 50) return { color: 'text-blue-600', icon: Zap, label: 'Very Fast' };
    if (timeMs < 200) return { color: 'text-yellow-600', icon: Clock, label: 'Fast' };
    return { color: 'text-orange-600', icon: Clock, label: 'Normal' };
  };

  const performance = getPerformanceIndicator(call.processing_time_ms);
  const PerformanceIcon = performance.icon;

  // Map emergency_type to category for display
  const category = call.emergency_type?.replace('_', ' ') || 'Other';
  const categoryKey = category.includes('Medical') ? 'Medical' : 
                     category.includes('Fire') ? 'Fire' : 
                     category.includes('Police') ? 'Crime' : 'Other';

  return (
    <Card className={`transition-all duration-200 hover:shadow-lg ${className}`}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Badge className={categoryColors[categoryKey as keyof typeof categoryColors]}>
              {categoryKey}
            </Badge>
            <Badge className={`${priorityColors[call.priority as keyof typeof priorityColors]} border-0`}>
              <AlertTriangle className="w-3 h-3 mr-1" />
              {priorityLabels[call.priority as keyof typeof priorityLabels]}
            </Badge>
          </div>
          <div className={`flex items-center gap-1 ${performance.color}`}>
            <PerformanceIcon className="w-4 h-4" />
            <span className="text-xs font-medium">{performance.label}</span>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-3">
        <div className="text-sm text-gray-700 dark:text-gray-300">
          {call.summary}
        </div>
        
        <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <Zap className="w-3 h-3" />
              {call.processing_time_ms.toFixed(1)}ms
            </span>
            {call.from_number && (
              <span>From: {call.from_number}</span>
            )}
          </div>
          {isClient && formattedTime && (
            <span>{formattedTime}</span>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

// Ultra-Fast Test Component
export function UltraFastTest() {
  const [testResult, setTestResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const runTest = async () => {
    setLoading(true);
    setError('');
    
    try {
      const result = await ultraFastApi.runTest();
      setTestResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Test failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">Ultra-Fast Triage Test</h2>
        <p className="text-gray-600 dark:text-gray-400">
          Test the ultra-fast emergency triage system with minimal JSON structure
        </p>
      </div>

      <div className="mb-6">
        <button
          onClick={runTest}
          disabled={loading}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Testing...' : 'Run Ultra-Fast Test'}
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          Error: {error}
        </div>
      )}

      {testResult && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Test Result</h3>
          <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <span className="font-semibold">Category:</span> {testResult.category}
              </div>
              <div>
                <span className="font-semibold">Priority:</span> {testResult.priority}
              </div>
              <div>
                <span className="font-semibold">Processing Time:</span> {testResult.processing_time_ms}ms
              </div>
              <div>
                <span className="font-semibold">Reasoning:</span> {testResult.reasoning_byte}
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <h4 className="font-semibold mb-2">Raw Response:</h4>
            <pre className="text-sm overflow-x-auto">
              {JSON.stringify(testResult, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

'use client';

import { useState, useEffect } from 'react';
import { Clock, Zap, AlertTriangle, Shield, Phone, Info } from 'lucide-react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ultraFastApi, UltraFastResult } from '@/services/ultraFastApi';

interface UltraFastSafetyCardProps {
  result: UltraFastResult;
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

const priorityLevelColors = {
  'CRITICAL': 'bg-red-100 text-red-800 border-red-300',
  'HIGH': 'bg-orange-100 text-orange-800 border-orange-300',
  'MODERATE': 'bg-yellow-100 text-yellow-800 border-yellow-300',
  'LOW': 'bg-blue-100 text-blue-800 border-blue-300',
};

export function UltraFastSafetyCard({ result, className }: UltraFastSafetyCardProps) {
  const [expanded, setExpanded] = useState(false);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  const getPerformanceIndicator = (timeMs: number) => {
    if (timeMs < 10) return { color: 'text-green-600', icon: Zap, label: 'Ultra-Fast' };
    if (timeMs < 50) return { color: 'text-blue-600', icon: Zap, label: 'Very Fast' };
    if (timeMs < 200) return { color: 'text-yellow-600', icon: Clock, label: 'Fast' };
    return { color: 'text-orange-600', icon: Clock, label: 'Normal' };
  };

  const performance = getPerformanceIndicator(result.processing_time_ms);
  const PerformanceIcon = performance.icon;

  return (
    <Card className={`transition-all duration-200 hover:shadow-lg ${className}`}>
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Badge className={categoryColors[result.category]}>
              {result.category}
            </Badge>
            <Badge className={`${priorityColors[result.priority as keyof typeof priorityColors]} border-0`}>
              <AlertTriangle className="w-3 h-3 mr-1" />
              P{result.priority}
            </Badge>
            <Badge className={priorityLevelColors[result.priority_level as keyof typeof priorityLevelColors]}>
              {result.priority_level}
            </Badge>
          </div>
          <div className={`flex items-center gap-1 ${performance.color}`}>
            <PerformanceIcon className="w-4 h-4" />
            <span className="text-xs font-medium">{performance.label}</span>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Voice Response */}
        <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
          <div className="flex items-center gap-2 mb-2">
            <Phone className="w-4 h-4 text-blue-600" />
            <span className="font-semibold text-blue-800 dark:text-blue-200">What to Say:</span>
          </div>
          <p className="text-blue-700 dark:text-blue-300 text-sm">{result.what_to_say}</p>
        </div>

        {/* Immediate Actions */}
        <div className="p-3 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-4 h-4 text-red-600" />
            <span className="font-semibold text-red-800 dark:text-red-200">Immediate Actions:</span>
          </div>
          <ul className="space-y-1">
            {result.immediate_actions.slice(0, expanded ? undefined : 2).map((action, index) => (
              <li key={index} className="text-red-700 dark:text-red-300 text-sm flex items-start gap-2">
                <span className="text-red-500 mt-1">•</span>
                {action}
              </li>
            ))}
          </ul>
          {result.immediate_actions.length > 2 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setExpanded(!expanded)}
              className="mt-2 text-red-600 hover:text-red-700"
            >
              {expanded ? 'Show Less' : `Show ${result.immediate_actions.length - 2} More`}
            </Button>
          )}
        </div>

        {/* Safety Precautions */}
        <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
          <div className="flex items-center gap-2 mb-2">
            <Shield className="w-4 h-4 text-green-600" />
            <span className="font-semibold text-green-800 dark:text-green-200">Safety Precautions:</span>
          </div>
          <ul className="space-y-1">
            {result.safety_precautions.slice(0, expanded ? undefined : 2).map((precaution, index) => (
              <li key={index} className="text-green-700 dark:text-green-300 text-sm flex items-start gap-2">
                <span className="text-green-500 mt-1">•</span>
                {precaution}
              </li>
            ))}
          </ul>
        </div>

        {/* Performance Info */}
        <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 pt-2 border-t">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <Zap className="w-3 h-3" />
              {result.processing_time_ms.toFixed(1)}ms
            </span>
            <span className="flex items-center gap-1">
              <Info className="w-3 h-3" />
              {(result.confidence * 100).toFixed(0)}% confidence
            </span>
          </div>
          <span className="text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">
            {result.response_type}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}

// Enhanced Test Component with Safety Responses
export function UltraFastSafetyTest() {
  const [testResult, setTestResult] = useState<UltraFastResult | null>(null);
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
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">Ultra-Fast Emergency Triage with Safety</h2>
        <p className="text-gray-600 dark:text-gray-400">
          Test the enhanced ultra-fast system with safety precautions and guidance
        </p>
      </div>

      <div className="mb-6">
        <button
          onClick={runTest}
          disabled={loading}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Testing...' : 'Run Safety Test'}
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          Error: {error}
        </div>
      )}

      {testResult && (
        <div className="space-y-6">
          <h3 className="text-lg font-semibold">Emergency Response with Safety Guidance</h3>
          <UltraFastSafetyCard result={testResult} />
          
          <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <h4 className="font-semibold mb-2">Complete Response Data:</h4>
            <pre className="text-sm overflow-x-auto max-h-64">
              {JSON.stringify(testResult, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

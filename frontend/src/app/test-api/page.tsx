'use client';

import { useState, useEffect } from 'react';
import { emergencyApi } from '@/utils/api';

export default function TestAPIPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const testAPI = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log('Making API call...');
      const response = await emergencyApi.getAnalytics();
      console.log('API Response:', response);
      setData(response);
    } catch (err: any) {
      console.error('API Error:', err);
      setError(err.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    testAPI();
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">API Test Page</h1>
      
      <button 
        onClick={testAPI}
        disabled={loading}
        className="bg-blue-500 text-white px-4 py-2 rounded mb-4"
      >
        {loading ? 'Loading...' : 'Test API Call'}
      </button>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <strong>Error:</strong> {error}
        </div>
      )}

      {data && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          <strong>Success!</strong> API returned data:
          <pre className="mt-2 text-sm overflow-auto">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}

      <div className="bg-gray-100 p-4 rounded">
        <h2 className="font-bold mb-2">Debug Info:</h2>
        <p>API Base URL: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}</p>
        <p>Data State: {data ? 'Has data' : 'No data'}</p>
        <p>Error State: {error ? error : 'No error'}</p>
        <p>Loading State: {loading ? 'Loading' : 'Not loading'}</p>
      </div>
    </div>
  );
}

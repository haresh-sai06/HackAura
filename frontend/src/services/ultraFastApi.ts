/**
 * Ultra-Fast Emergency Triage API Service
 * Handles communication with the ultra-fast backend endpoints
 */

export interface UltraFastResult {
  category: 'Medical' | 'Fire' | 'Crime' | 'Other';
  priority: number;
  reasoning_byte: string;
  processing_time_ms: number;
  
  // Safety response
  what_to_say: string;
  immediate_actions: string[];
  safety_precautions: string[];
  priority_level: string;
  response_type: string;
  confidence: number;
}

export interface UltraFastCall {
  id: number;
  call_sid: string;
  from_number: string;
  emergency_type: string;
  severity_level: string;
  priority: number;
  summary: string;
  processing_time_ms: number;
  created_at: string | null;
}

export interface UltraFastStats {
  total_ultra_fast_calls: number;
  avg_processing_time_ms: number;
  category_distribution: Record<string, number>;
  performance_rating: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  calls?: UltraFastCall[];
  total?: number;
  stats?: UltraFastStats;
  error?: string;
}

class UltraFastApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  /**
   * Process emergency text with ultra-fast triage
   */
  async processEmergency(text: string): Promise<UltraFastResult> {
    try {
      const formData = new FormData();
      formData.append('text', text);

      const response = await fetch(`${this.baseUrl}/api/voice/ultra-fast`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Error processing emergency:', error);
      throw error;
    }
  }

  /**
   * Get recent ultra-fast processed calls
   */
  async getRecentCalls(limit: number = 50): Promise<{ calls: UltraFastCall[], total: number }> {
    try {
      const response = await fetch(`${this.baseUrl}/api/voice/ultra-fast/calls?limit=${limit}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (!result.success) {
        throw new Error(result.error || 'Failed to fetch calls');
      }

      return {
        calls: result.calls || [],
        total: result.total || 0
      };
    } catch (error) {
      console.error('Error fetching recent calls:', error);
      throw error;
    }
  }

  /**
   * Get ultra-fast processing statistics
   */
  async getStats(): Promise<UltraFastStats> {
    try {
      const response = await fetch(`${this.baseUrl}/api/voice/ultra-fast/stats`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (!result.success) {
        throw new Error(result.error || 'Failed to fetch stats');
      }

      return result.stats || {
        total_ultra_fast_calls: 0,
        avg_processing_time_ms: 0,
        category_distribution: {},
        performance_rating: 'UNKNOWN'
      };
    } catch (error) {
      console.error('Error fetching stats:', error);
      throw error;
    }
  }

  /**
   * Test ultra-fast processing with sample data
   */
  async runTest(): Promise<UltraFastResult> {
    const testCases = [
      'Massive fire in the building!',
      'Heart attack at main street',
      'Gun shots heard downtown',
      'Car accident on highway',
      'Person fell down stairs'
    ];

    const randomCase = testCases[Math.floor(Math.random() * testCases.length)];
    return this.processEmergency(randomCase);
  }

  /**
   * Batch process multiple emergencies
   */
  async batchProcess(texts: string[]): Promise<UltraFastResult[]> {
    const promises = texts.map(text => this.processEmergency(text));
    return Promise.all(promises);
  }

  /**
   * Health check for ultra-fast service
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}

// Create singleton instance
export const ultraFastApi = new UltraFastApiService();

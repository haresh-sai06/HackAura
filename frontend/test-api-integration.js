// Test API integration directly
const axios = require('axios');

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

async function testAnalyticsIntegration() {
  try {
    console.log('🔍 Testing analytics API integration...');
    
    // Test the analytics endpoint
    console.log('📡 Making request to /api/analytics...');
    const response = await api.get('/api/analytics');
    
    console.log('✅ API call successful!');
    console.log('📊 Response status:', response.status);
    console.log('📋 Response data:', JSON.stringify(response.data, null, 2));
    
    // Verify the data structure matches what the frontend expects
    const data = response.data;
    const requiredFields = ['totalCalls', 'callsByStatus', 'callsByType', 'callsBySeverity', 'averageResponseTime', 'resolvedCalls', 'pendingCalls'];
    
    let allFieldsPresent = true;
    requiredFields.forEach(field => {
      if (!(field in data)) {
        console.log(`❌ Missing field: ${field}`);
        allFieldsPresent = false;
      } else {
        console.log(`✅ Field present: ${field}`);
      }
    });
    
    if (allFieldsPresent) {
      console.log('🎉 All required fields are present! The frontend should display real data.');
    } else {
      console.log('⚠️  Some fields are missing. This might cause issues in the frontend.');
    }
    
    return data;
    
  } catch (error) {
    console.error('❌ API call failed:', error.message);
    if (error.response) {
      console.error('📄 Response status:', error.response.status);
      console.error('📄 Response data:', error.response.data);
    }
    return null;
  }
}

testAnalyticsIntegration();

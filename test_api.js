// Simple test to verify API integration
const axios = require('axios');

async function testAnalyticsAPI() {
  try {
    console.log('Testing analytics API...');
    
    const response = await axios.get('http://localhost:8000/api/analytics', {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000'
      }
    });
    
    console.log('✅ API call successful!');
    console.log('Status:', response.status);
    console.log('Data:', JSON.stringify(response.data, null, 2));
    
    // Verify the data structure
    const data = response.data;
    if (data.totalCalls && data.callsByStatus && data.callsByType) {
      console.log('✅ Data structure is correct');
    } else {
      console.log('❌ Data structure is incorrect');
    }
    
  } catch (error) {
    console.error('❌ API call failed:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
  }
}

testAnalyticsAPI();

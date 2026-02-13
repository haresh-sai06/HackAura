# 🚨 RAPID-100 Testing Guide

## 📋 Testing Workflow

### 1. Environment Setup

```bash
# Install required dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your actual API keys:
# - OPENAI_API_KEY (required for transcription)
# - TWILIO_ACCOUNT_SID (required)
# - TWILIO_AUTH_TOKEN (required)
# - TWILIO_PHONE_NUMBER (required)
```

### 2. Basic Component Testing

```bash
# Test individual triage components (no API calls required)
python test_basic_triage.py
```

**Expected Results:**
- ✅ Classification: Correct emergency type identification
- ✅ Severity: Accurate scoring (80+ = Critical, 60+ = High, 40+ = Moderate)
- ✅ Routing: Proper service assignment
- ✅ Summary: Concise dispatcher-ready output

### 3. Full System Testing

```bash
# Test complete triage pipeline (requires OpenAI API key)
python test_triage.py
```

### 4. Server Testing

```bash
# Start the RAPID-100 server
python main.py
```

**Server Endpoints:**
- `GET /` - System status
- `GET /health` - Health check
- `POST /api/voice` - Emergency call webhook
- `POST /api/voice/process` - Triage processing
- `POST /api/voice/status` - Call status updates

### 5. Manual Testing with Twilio

#### Setup Twilio Webhook:
1. Configure your Twilio phone number webhook URL:
   ```
   https://your-domain.com/api/voice
   ```

#### Test Call Flow:
1. Call your Twilio number
2. System responds: *"Emergency services. Please describe your emergency clearly and calmly."*
3. Describe emergency (max 30 seconds)
4. System processes and responds: *"Emergency recorded. Assistance is being dispatched."*

#### Test Scenarios:

**Critical Medical:**
```
"Help! My father is 65 years old and he's not breathing. He collapsed on the floor at MG Road."
```
**Expected:** Level 1, Ambulance, Priority 1

**Fire Emergency:**
```
"There's a fire spreading in our apartment building on Brigade Road. People are trapped."
```
**Expected:** Level 1, Fire Department, Priority 1

**Accident:**
```
"Car accident on Commercial Street. Two vehicles collided. One person is bleeding heavily."
```
**Expected:** Level 1, Multiple Services, Priority 1

**Moderate Medical:**
```
"My son fell and cut his arm. He's bleeding but it's not too bad. He needs stitches."
```
**Expected:** Level 3, Ambulance, Priority 4

### 6. API Testing with curl

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test root endpoint
curl http://localhost:8000/

# Simulate Twilio webhook (requires proper Twilio headers)
curl -X POST http://localhost:8000/api/voice \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "CallSid=test123&From=+1234567890"
```

### 7. Performance Testing

**Key Metrics:**
- ⏱️ Processing time < 5 seconds
- 🎯 Classification accuracy > 85%
- 📊 Severity scoring consistency
- 🔄 System uptime > 99%

**Load Testing:**
```bash
# Test multiple concurrent requests
python -c "
import asyncio
import aiohttp

async def test_concurrent():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(10):
            task = session.post('http://localhost:8000/api/voice/process')
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        print(f'Completed {len(responses)} requests')

asyncio.run(test_concurrent())
"
```

### 8. Integration Testing

#### Frontend Integration:
```javascript
// Test frontend-backend communication
const testEmergency = async () => {
  const response = await fetch('/api/emergency/test', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      transcript: "Help! There's a fire at MG Road"
    })
  });
  
  const result = await response.json();
  console.log('Triage Result:', result);
};
```

#### Database Integration:
```python
# Test logging and audit trail
def test_audit_logging():
    # Check if emergency calls are logged
    # Verify triage decisions are recorded
    # Ensure processing times are tracked
    pass
```

### 9. Error Handling Testing

**Test Scenarios:**
- Empty transcript
- Invalid audio file
- API service failures
- Network timeouts
- Malformed requests

**Expected Behavior:**
- Graceful fallbacks
- Appropriate error responses
- System recovery
- Logging of errors

### 10. Security Testing

**Security Checks:**
- ✅ API key protection
- ✅ Input validation
- ✅ Rate limiting
- ✅ HTTPS enforcement
- ✅ Data sanitization

### 📊 Success Criteria

**Functional Requirements:**
- ✅ Emergency classification accuracy > 85%
- ✅ Severity scoring consistency
- ✅ Processing time < 5 seconds
- ✅ 100% system uptime during testing
- ✅ Proper error handling

**Non-Functional Requirements:**
- ✅ Modular code structure
- ✅ Comprehensive logging
- ✅ Clean API documentation
- ✅ Environment configuration
- ✅ Production-ready deployment

### 🚀 Production Deployment

**Pre-deployment Checklist:**
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Monitoring setup
- [ ] Backup procedures
- [ ] Documentation complete

**Deployment Steps:**
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment: `cp .env.example .env`
3. Set up SSL/HTTPS
4. Configure monitoring
5. Start server: `python main.py`
6. Verify health endpoint: `curl /health`

### 📞 Support Contact

For issues during testing:
1. Check logs: `tail -f logs/rapid100.log`
2. Verify configuration: `cat .env`
3. Test components individually
4. Check API key validity
5. Review system resources

---

**RAPID-100 Emergency Triage System**  
*Real-Time AI for Priority Incident Dispatch*

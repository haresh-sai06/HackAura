# HackAura API Documentation

## 📋 Overview

The HackAura API provides endpoints for emergency triage, voice processing, and real-time dashboard updates. All endpoints are built with FastAPI and include automatic OpenAPI documentation.

## 🔗 Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## 📊 API Endpoints

### Health & Status

#### `GET /health`
Check server health and Ollama connection.

**Response**:
```json
{
  "status": "healthy",
  "service": "HackAura Backend",
  "version": "1.0.0",
  "ollama_status": "connected",
  "database_status": "connected"
}
```

#### `GET /`
Get server information.

**Response**:
```json
{
  "service": "HackAura Emergency Triage System",
  "version": "1.0.0",
  "description": "AI-powered emergency triage and response system"
}
```

---

## 🚨 Emergency Triage Endpoints

### `POST /api/voice/ultra-fast`
Process emergency text and return triage results with safety guidance.

**Request**:
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameters**:
  - `text` (string, optional): Emergency description text
  - `SpeechResult` (string, optional): Transcribed speech from Twilio
  - `UnstableSpeechResult` (string, optional): Unstable speech result
  - `CallSid` (string, optional): Twilio call session ID

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/voice/ultra-fast \
  -F "text=There's a massive fire in the building and people are trapped"
```

**Response**:
```json
{
  "category": "Fire",
  "priority": 1,
  "reasoning_byte": "Massive fire with people trapped indicates critical emergency",
  "processing_time_ms": 85.0,
  "what_to_say": "Help is coming! Fire department is being dispatched now. Evacuate immediately and do not use elevators. Stay low to avoid smoke inhalation and feel doors before opening. Use stairs only for evacuation and help others evacuate if safe to do so.",
  "immediate_actions": [
    "Evacuate the area immediately",
    "Do not use elevators",
    "Close doors behind you",
    "Move to designated assembly point"
  ],
  "safety_precautions": [
    "Stay low to avoid smoke inhalation",
    "Feel doors before opening - hot means fire is near",
    "Use stairs only for evacuation",
    "Meet at designated assembly point"
  ],
  "priority_level": "CRITICAL",
  "response_type": "hybrid_conversation",
  "dispatched_service": "Fire Department",
  "assigned_service": "FIRE_DEPARTMENT",
  "status": "AWAITING_FOLLOWUP",
  "confidence": 0.95,
  "timestamp": 1739534400.0,
  "created_at": 1739534400.0,
  "call_time": 1739534400.0,
  "classification_method": "rule_based",
  "safety_method": "predefined"
}
```

**Error Response**:
```json
{
  "category": "Other",
  "priority": 3,
  "reasoning_byte": "System error during triage",
  "processing_time_ms": 0.0,
  "what_to_say": "I'm having trouble understanding. Please stay on the line for assistance.",
  "immediate_actions": ["Stay calm"],
  "safety_precautions": ["Keep phone available"],
  "priority_level": "MODERATE",
  "response_type": "error",
  "confidence": 0.3
}
```

### `POST /api/voice/ultra-fast/followup`
Handle follow-up responses in emergency conversation flow.

**Request**:
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameters**:
  - `SpeechResult` (string, optional): Transcribed speech
  - `UnstableSpeechResult` (string, optional): Unstable speech result
  - `CallSid` (string, optional): Call session ID

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/voice/ultra-fast/followup \
  -F "SpeechResult=yes" \
  -F "CallSid=call_123456"
```

**Response (Escalated)**:
```json
{
  "what_to_say": "Help is on the way! Priority increased to critical. Stay on the line and we will end the call when help arrives.",
  "immediate_actions": ["Move to safety", "Follow dispatcher instructions"],
  "safety_precautions": ["Stay on line", "Keep phone available"],
  "response_type": "escalated",
  "status": "ESCALATED",
  "priority": 1,
  "category": "Fire",
  "dispatched_service": "Fire Department",
  "processing_time_ms": 25.0,
  "confidence": 0.98
}
```

**Response (Completed)**:
```json
{
  "what_to_say": "Understood. Help is on the way. We will end the call now. Stay safe.",
  "immediate_actions": ["Stay safe", "Wait for help"],
  "safety_precautions": ["Keep phone available"],
  "response_type": "completed",
  "status": "COMPLETED",
  "priority": 2,
  "category": "Fire",
  "dispatched_service": "Fire Department",
  "processing_time_ms": 20.0,
  "confidence": 0.95
}
```

### `POST /api/voice/ultra-fast/voice`
Generate TwiML voice response for emergency triage with conversation flow.

**Request**:
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameters**:
  - `SpeechResult` (string, optional): Transcribed speech
  - `UnstableSpeechResult` (string, optional): Unstable speech result
  - `CallSid` (string, optional): Call session ID

**Response (TwiML)**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">Help is coming! Fire department is being dispatched now. Evacuate immediately...</Say>
    <Pause length="1"/>
    <Gather input="speech" timeout="5" action="/voice/ultra-fast/followup" method="POST">
        <Say voice="alice">Is the situation more dangerous? Please say yes or no.</Say>
    </Gather>
</Response>
```

---

## 📞 Call Management Endpoints

### `GET /api/voice/ultra-fast/calls`
Get recent emergency calls for dashboard display.

**Request**:
- **Method**: GET
- **Parameters**:
  - `limit` (integer, optional): Maximum number of calls to return (default: 50)

**Example Request**:
```bash
curl http://localhost:8000/api/voice/ultra-fast/calls?limit=10
```

**Response**:
```json
{
  "success": true,
  "calls": [
    {
      "id": 1,
      "call_sid": "hybrid_1739534400",
      "from_number": "+15551234567",
      "emergency_type": "FIRE",
      "severity_level": "LEVEL_1",
      "priority": 1,
      "summary": "Massive fire with people trapped indicates critical emergency",
      "processing_time_ms": 85.0,
      "created_at": "2026-02-14T12:00:00Z",
      "category": "Fire"
    },
    {
      "id": 2,
      "call_sid": "hybrid_1739534300",
      "from_number": "+15559876543",
      "emergency_type": "MEDICAL",
      "severity_level": "LEVEL_2",
      "priority": 2,
      "summary": "Heart attack with difficulty breathing",
      "processing_time_ms": 92.0,
      "created_at": "2026-02-14T11:58:00Z",
      "category": "Medical"
    }
  ],
  "total": 2
}
```

### `GET /api/voice/ultra-fast/stats`
Get processing statistics and performance metrics.

**Request**:
- **Method**: GET

**Example Request**:
```bash
curl http://localhost:8000/api/voice/ultra-fast/stats
```

**Response**:
```json
{
  "success": true,
  "stats": {
    "total_calls": 150,
    "avg_processing_time_ms": 85.5,
    "min_ms": 45.2,
    "max_ms": 343.1,
    "service_type": "ollama_ai"
  }
}
```

---

## 🎙️ Legacy Voice Endpoints

### `POST /api/voice`
Handle incoming Twilio voice calls (legacy endpoint).

**Request**:
- **Method**: POST
- **Content-Type**: application/x-www-form-urlencoded
- **Parameters**: Twilio webhook parameters

**Response**: TwiML for call handling

### `POST /api/voice/process`
Process speech input from Twilio calls (legacy endpoint).

**Request**:
- **Method**: POST
- **Content-Type**: application/x-www-form-urlencoded
- **Parameters**:
  - `SpeechResult` (string): Transcribed speech
  - `CallSid` (string): Call session ID

**Response**: TwiML with AI-generated response

### `POST /api/voice/status`
Handle call status updates from Twilio.

**Request**:
- **Method**: POST
- **Content-Type**: application/x-www-form-urlencoded
- **Parameters**: Twilio status parameters

**Response**: 200 OK

---

## 📊 Data Models

### Emergency Categories

| Category | Description | Examples |
|----------|-------------|----------|
| `Fire` | Fire-related emergencies | "Building on fire", "Explosion", "Smoke everywhere" |
| `Medical` | Medical emergencies | "Heart attack", "Can't breathe", "Unconscious" |
| `Crime` | Police emergencies | "Shooting", "Robbery", "Assault" |
| `Accident` | Accident emergencies | "Car crash", "Traffic accident", "Fall down stairs" |
| `Other` | Other emergencies | "General emergency", "Need help" |

### Priority Levels

| Priority | Level | Description | Response Time |
|----------|-------|-------------|---------------|
| 1 | P1 | Critical - Life threatening | <100ms |
| 2 | P2 | High - Serious | <200ms |
| 3 | P3 | Medium - Injuries | <300ms |
| 4 | P4 | Low - Minor | <500ms |

### Severity Levels

| Level | Score Range | Description |
|-------|-------------|-------------|
| `LEVEL_1` | 80-100 | Critical - Immediate danger |
| `LEVEL_2` | 60-79 | High - Serious situation |
| `LEVEL_3` | 40-59 | Moderate - Injuries present |
| `LEVEL_4` | 0-39 | Low - Minor incident |

---

## 🔧 Configuration

### Environment Variables

```env
# Ollama Configuration
OLLAMA_MODEL=qwen2.5:0.5b
OLLAMA_HOST=localhost:11434

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Database Configuration
DATABASE_URL=sqlite:///hackaura.db

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number

# AI Assistant Configuration
AI_ASSISTANT_NAME=HackAura
AI_ASSISTANT_VOICE=alice
SPEECH_TIMEOUT=5
```

---

## 🧪 Testing

### Health Check

```bash
curl http://localhost:8000/health
```

### Triage Test

```bash
curl -X POST http://localhost:8000/api/voice/ultra-fast \
  -F "text=There's a fire in my kitchen"
```

### Follow-up Test

```bash
curl -X POST http://localhost:8000/api/voice/ultra-fast/followup \
  -F "SpeechResult=yes" \
  -F "CallSid=test_call_123"
```

### Stats Test

```bash
curl http://localhost:8000/api/voice/ultra-fast/stats
```

---

## 🚨 Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error during processing"
}
```

#### Ollama Service Error
```json
{
  "category": "Other",
  "priority": 3,
  "reasoning_byte": "AI service unavailable",
  "what_to_say": "I'm having trouble understanding. Please stay on the line for assistance.",
  "response_type": "error"
}
```

---

## 📈 Performance Metrics

### Response Times

- **Average**: 85ms
- **95th Percentile**: 200ms
- **Maximum**: 500ms

### Accuracy Metrics

- **Classification Accuracy**: >95%
- **Confidence Score**: 0.85-0.99
- **Error Rate**: <5%

---

## 🔒 Security

### Rate Limiting

- **Requests per minute**: 100
- **Burst limit**: 20 requests

### Input Validation

- Maximum text length: 1000 characters
- Sanitized HTML/Script content
- SQL injection protection

### Authentication

- Twilio request signature validation
- API key authentication (optional)

---

## 📚 SDK Examples

### Python

```python
import requests

# Process emergency text
response = requests.post(
    "http://localhost:8000/api/voice/ultra-fast",
    files={"text": "There's a fire in my building"}
)
result = response.json()
print(f"Category: {result['category']}")
print(f"Priority: {result['priority']}")
```

### JavaScript

```javascript
// Process emergency text
const formData = new FormData();
formData.append('text', 'There is a medical emergency');

fetch('http://localhost:8000/api/voice/ultra-fast', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Category:', data.category);
  console.log('Priority:', data.priority);
});
```

### cURL

```bash
# Get recent calls
curl http://localhost:8000/api/voice/ultra-fast/calls

# Get stats
curl http://localhost:8000/api/voice/ultra-fast/stats
```

---

## 🔄 WebSocket Integration

### Real-time Updates

The backend provides WebSocket connections for real-time dashboard updates:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  if (data.type === 'emergency_conversation') {
    updateDashboard(data.data);
  }
};
```

### WebSocket Events

- `emergency_conversation`: New emergency call processed
- `call_update`: Call status updated
- `system_stats`: Performance statistics updated

---

## 📞 OpenAPI Documentation

Interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

For more detailed implementation information, see the backend README.md file.

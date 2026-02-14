# HackAura Frontend Dashboard

## 📋 Overview

The HackAura frontend is a sophisticated real-time dashboard built with Next.js that provides live monitoring of emergency calls, AI triage results, and system performance metrics.

## 🚀 Features

### 📊 Real-time Dashboard
- **Live Call Monitoring**: Real-time updates of active emergency calls
- **Emergency Classification**: Visual display of emergency types and priorities
- **Performance Metrics**: AI processing speed and accuracy tracking
- **Interactive Maps**: Geographic visualization of emergency locations

### 🎯 Key Components
- **Call Cards**: Detailed view of individual emergency calls
- **Analytics Section**: Charts and statistics for system performance
- **Team Management**: Emergency responder coordination
- **Settings Panel**: System configuration and preferences

### 📱 Responsive Design
- **Desktop**: Full-featured dashboard experience
- **Tablet**: Optimized touch interface
- **Mobile**: Essential features for field use

## 🏗️ Technology Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State Management**: Zustand
- **Charts**: Recharts
- **Icons**: Lucide React
- **Real-time**: WebSocket connections
- **API**: Fetch with TypeScript interfaces

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── page.tsx           # Main dashboard
│   │   ├── calls/             # Call management pages
│   │   ├── analytics/         # Analytics dashboard
│   │   ├── team/              # Team management
│   │   ├── settings/          # System settings
│   │   └── layout.tsx         # Root layout
│   ├── components/            # Reusable React components
│   │   ├── calls/             # Call-related components
│   │   │   ├── CallCard.tsx
│   │   │   ├── CallList.tsx
│   │   │   ├── CallDetails.tsx
│   │   │   ├── UltraFastCallCard.tsx
│   │   │   └── UltraFastSafetyCard.tsx
│   │   ├── dashboard/         # Dashboard components
│   │   │   ├── AnalyticsSection.tsx
│   │   │   ├── CallsSection.tsx
│   │   │   └── OverviewSection.tsx
│   │   ├── layout/            # Layout components
│   │   │   ├── DashboardLayout.tsx
│   │   │   ├── Navigation.tsx
│   │   │   └── Sidebar.tsx
│   │   └── ui/                # Base UI components (shadcn/ui)
│   ├── services/              # API service layers
│   │   ├── ultraFastApi.ts    # Backend API client
│   │   └── websocketService.ts # WebSocket management
│   ├── hooks/                 # Custom React hooks
│   ├── types/                 # TypeScript type definitions
│   └── utils/                 # Utility functions
├── public/                    # Static assets
├── package.json              # Dependencies and scripts
├── tailwind.config.js        # Tailwind configuration
├── next.config.js            # Next.js configuration
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn
- HackAura backend running on port 8000

### 1. Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install
```

### 2. Environment Configuration

Create `.env.local` file:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# WebSocket URL (if different from API)
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Development settings
NEXT_PUBLIC_DEV_MODE=true
```

### 3. Start Development Server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 4. Build for Production

```bash
npm run build
npm start
# or
yarn build
yarn start
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |
| `NEXT_PUBLIC_WS_URL` | WebSocket server URL | `ws://localhost:8000` |
| `NEXT_PUBLIC_DEV_MODE` | Development mode flag | `true` |

### Next.js Configuration

```javascript
// next.config.js
module.exports = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    appDir: true,
  },
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
}
```

### Tailwind Configuration

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
}
```

## 📊 Core Components

### CallCard Component

Displays individual emergency call information with real-time updates.

```typescript
interface CallCardProps {
  call: EmergencyCall;
  onUpdate?: (call: EmergencyCall) => void;
}

export function CallCard({ call, onUpdate }: CallCardProps) {
  // Component implementation
}
```

### UltraFastCallCard Component

Optimized call card for ultra-fast triage results with performance metrics.

```typescript
interface UltraFastCallCardProps {
  call: UltraFastCall;
  className?: string;
}

export function UltraFastCallCard({ call, className }: UltraFastCallCardProps) {
  // Performance indicator logic
  // Category color mapping
  // Priority display
}
```

### AnalyticsSection Component

Real-time analytics dashboard with charts and metrics.

```typescript
export function AnalyticsSection() {
  const { stats, loading } = useStats();
  
  return (
    <div className="space-y-6">
      <PerformanceChart data={stats} />
      <CallVolumeChart data={stats} />
      <ResponseTimeMetrics data={stats} />
    </div>
  );
}
```

## 🔌 API Integration

### UltraFastApi Service

TypeScript client for backend API communication.

```typescript
// services/ultraFastApi.ts
export interface UltraFastResult {
  category: 'Medical' | 'Fire' | 'Crime' | 'Other';
  priority: number;
  reasoning_byte: string;
  processing_time_ms: number;
  what_to_say: string;
  immediate_actions: string[];
  safety_precautions: string[];
  confidence: number;
}

class UltraFastApiService {
  async processEmergency(text: string): Promise<UltraFastResult> {
    const formData = new FormData();
    formData.append('text', text);

    const response = await fetch(`${this.baseUrl}/api/voice/ultra-fast`, {
      method: 'POST',
      body: formData,
    });

    return response.json();
  }

  async getRecentCalls(limit: number = 50): Promise<{ calls: UltraFastCall[], total: number }> {
    const response = await fetch(`${this.baseUrl}/api/voice/ultra-fast/calls?limit=${limit}`);
    return response.json();
  }
}
```

### WebSocket Integration

Real-time updates using WebSocket connections.

```typescript
// services/websocketService.ts
class WebSocketService {
  private ws: WebSocket | null = null;
  private subscribers: Map<string, Set<(data: any) => void>> = new Map();

  connect(url: string) {
    this.ws = new WebSocket(url);
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.notifySubscribers(data.type, data);
    };
  }

  subscribe(event: string, callback: (data: any) => void) {
    if (!this.subscribers.has(event)) {
      this.subscribers.set(event, new Set());
    }
    this.subscribers.get(event)!.add(callback);
  }
}
```

## 🎨 UI Components

### shadcn/ui Components

The project uses shadcn/ui for consistent, accessible UI components:

```typescript
// Example usage
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export function EmergencyAlert({ emergency }: { emergency: EmergencyCall }) {
  return (
    <Card className="border-red-200 bg-red-50">
      <CardHeader>
        <Badge variant="destructive">{emergency.category}</Badge>
      </CardHeader>
      <CardContent>
        <p>{emergency.summary}</p>
        <Button className="mt-2">View Details</Button>
      </CardContent>
    </Card>
  );
}
```

### Custom Hooks

```typescript
// hooks/useEmergencyCalls.ts
export function useEmergencyCalls() {
  const [calls, setCalls] = useState<EmergencyCall[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch initial calls
    ultraFastApi.getRecentCalls().then(({ calls }) => {
      setCalls(calls);
      setLoading(false);
    });

    // Subscribe to real-time updates
    websocketService.subscribe('emergency_conversation', (data) => {
      setCalls(prev => [data.data, ...prev.slice(0, 49)]);
    });

    return () => {
      websocketService.unsubscribe('emergency_conversation');
    };
  }, []);

  return { calls, loading };
}
```

## 📱 Responsive Design

### Breakpoints

```css
/* Tailwind default breakpoints */
sm: 640px   /* Small devices */
md: 768px   /* Medium devices */
lg: 1024px  /* Large devices */
xl: 1280px  /* Extra large devices */
2xl: 1536px /* 2X large devices */
```

### Mobile Optimization

```typescript
// Example responsive component
export function ResponsiveCallGrid({ calls }: { calls: EmergencyCall[] }) {
  return (
    <div className="grid gap-4 
                grid-cols-1    /* Mobile: 1 column */
                md:grid-cols-2 /* Tablet: 2 columns */
                lg:grid-cols-3 /* Desktop: 3 columns */
                xl:grid-cols-4 /* Large: 4 columns */">
      {calls.map(call => (
        <CallCard key={call.id} call={call} />
      ))}
    </div>
  );
}
```

## 🧪 Testing

### Unit Tests

```bash
# Run unit tests
npm test
# or
yarn test

# Run with coverage
npm run test:coverage
```

### E2E Tests

```bash
# Run E2E tests
npm run test:e2e
# or
yarn test:e2e
```

### Component Testing

```typescript
// __tests__/CallCard.test.tsx
import { render, screen } from '@testing-library/react';
import { CallCard } from '@/components/calls/CallCard';

test('renders emergency call information', () => {
  const mockCall = {
    id: 1,
    category: 'Fire',
    priority: 1,
    summary: 'Building fire reported',
  };

  render(<CallCard call={mockCall} />);
  
  expect(screen.getByText('Fire')).toBeInTheDocument();
  expect(screen.getByText('Building fire reported')).toBeInTheDocument();
});
```

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to Vercel
vercel --prod
```

### Docker

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

```bash
# Build and run
docker build -t hackaura-frontend .
docker run -p 3000:3000 hackaura-frontend
```

### Static Export

```bash
# Generate static files
npm run build
npm run export

# Deploy to any static host
# Output in ./out/ directory
```

## 🔧 Development Tools

### ESLint Configuration

```json
{
  "extends": [
    "next/core-web-vitals",
    "@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "prefer-const": "error"
  }
}
```

### Prettier Configuration

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## 📈 Performance Optimization

### Code Splitting

```typescript
// Dynamic imports for large components
const CallDetails = dynamic(() => import('@/components/calls/CallDetails'), {
  loading: () => <div>Loading...</div>,
  ssr: false,
});
```

### Image Optimization

```typescript
import Image from 'next/image';

export function EmergencyMap({ location }: { location: Location }) {
  return (
    <Image
      src="/api/map"
      alt="Emergency location map"
      width={800}
      height={600}
      priority={true}
    />
  );
}
```

### Caching Strategy

```typescript
// API caching with SWR
import useSWR from 'swr';

export function useEmergencyStats() {
  return useSWR('/api/voice/ultra-fast/stats', fetcher, {
    refreshInterval: 5000, // Refresh every 5 seconds
    revalidateOnFocus: true,
  });
}
```

## 🔒 Security

### Environment Variables

Never expose sensitive data in the frontend:

```typescript
// ✅ Correct - Use environment variables
const API_URL = process.env.NEXT_PUBLIC_API_URL;

// ❌ Wrong - Hardcoded values
const API_URL = 'http://localhost:8000';
```

### Input Validation

```typescript
// Validate user inputs
function validateEmergencyText(text: string): boolean {
  return text.length > 0 && text.length <= 1000;
}
```

### Content Security Policy

```javascript
// next.config.js
const ContentSecurityPolicy = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
`;

module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: ContentSecurityPolicy.replace(/\s{2,}/g, ' ').trim(),
          },
        ],
      },
    ];
  },
};
```

## 🐛 Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Check backend server is running
   - Verify WebSocket URL in environment variables
   - Check network connectivity

2. **API Calls Failing**
   - Verify backend API is accessible
   - Check CORS configuration on backend
   - Validate API endpoints

3. **Build Errors**
   - Clear node_modules and reinstall
   - Check TypeScript configuration
   - Verify all dependencies are compatible

### Debug Mode

```typescript
// Enable debug logging
if (process.env.NEXT_PUBLIC_DEV_MODE) {
  console.log('Debug: API call', data);
}
```

### Performance Issues

```typescript
// Use React.memo for expensive components
export const CallCard = React.memo(({ call }: CallCardProps) => {
  // Component implementation
});

// Use useMemo for expensive calculations
const filteredCalls = useMemo(() => {
  return calls.filter(call => call.priority <= maxPriority);
}, [calls, maxPriority]);
```

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [React Documentation](https://react.dev/)

---

For specific component implementations, see the individual component files in the `src/components/` directory.

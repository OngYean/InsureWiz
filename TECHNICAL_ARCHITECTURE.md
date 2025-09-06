# InsureWiz Technical Architecture

## System Architecture Overview
InsureWiz follows a modern client-server architecture with AI integration, designed for scalability, maintainability, and performance.

## Backend Architecture

### Core Structure
```
backend/
├── app/
│   ├── core/           # Application core and configuration
│   ├── api/            # API endpoints and routing
│   ├── services/       # Business logic and external integrations
│   ├── models/         # Data models and schemas
│   ├── middleware/     # Request/response middleware
│   └── utils/          # Utility functions and helpers
├── main.py             # Application entry point
├── run.py              # Server runner
└── requirements.txt     # Python dependencies
```

### Technology Stack
- **Framework**: FastAPI (Python 3.8+)
- **ASGI Server**: Uvicorn
- **AI Integration**: LangChain + Google Gemini Pro
- **API Documentation**: Auto-generated Swagger/OpenAPI
- **Validation**: Pydantic models
- **CORS**: Configurable cross-origin resource sharing

### Key Components

#### 1. Core Application (`app/core/`)
- Application configuration and settings
- Database connection management
- Middleware configuration
- Error handling and logging

#### 2. API Layer (`app/api/`)
- RESTful API endpoints
- Request/response handling
- Authentication and authorization (future)
- Rate limiting (future)

#### 3. Services (`app/services/`)
- AI chat service with LangChain integration
- Insurance policy processing
- Claims management
- Vehicle validation logic

#### 4. Models (`app/models/`)
- Pydantic data models
- Database schemas
- API request/response models
- Validation rules

### AI Integration Architecture
```
User Request → API Endpoint → Chat Service → LangChain → Google Gemini → Response Processing → User
```

- **LangChain**: Orchestrates AI interactions and maintains conversation context
- **Google Gemini Pro**: Provides intelligent responses to insurance queries
- **Context Management**: Maintains conversation history and user context
- **Response Processing**: Formats and validates AI responses

## Frontend Architecture

### Core Structure
```
frontend/
├── app/                # Next.js 15 app router
├── components/         # Reusable React components
├── lib/               # Utility functions and configurations
├── hooks/             # Custom React hooks
├── styles/            # Global styles and Tailwind configuration
└── public/            # Static assets
```

### Technology Stack
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui (Radix UI primitives)
- **State Management**: React hooks and context
- **Form Handling**: React Hook Form + Zod validation
- **Build Tool**: Next.js built-in bundler

### Key Components

#### 1. App Router (`app/`)
- Page routing and navigation
- Layout components
- API route handlers
- Server-side rendering

#### 2. Component Library (`components/`)
- Reusable UI components
- Form components
- Layout components
- Interactive elements

#### 3. Utility Layer (`lib/`)
- API client functions
- Helper utilities
- Type definitions
- Configuration constants

### State Management
- **Local State**: React useState for component-level state
- **Global State**: React Context for app-wide state
- **Form State**: React Hook Form for form management
- **Server State**: API calls and caching

## Data Flow Architecture

### 1. User Interaction Flow
```
User Input → Frontend Component → API Call → Backend Service → AI Processing → Response → UI Update
```

### 2. AI Chat Flow
```
User Message → Chat Component → POST /api/chat → Chat Service → LangChain → Gemini API → Response Processing → Frontend Update
```

### 3. Data Validation Flow
```
User Input → Zod Schema Validation → API Request → Pydantic Validation → Service Processing → Response Validation → Frontend Display
```

## Security Architecture

### Current Implementation
- CORS configuration for local development
- Input validation with Pydantic/Zod
- Environment variable management
- API key security for Google Gemini

### Future Security Features
- User authentication and authorization
- Rate limiting and DDoS protection
- Input sanitization and XSS prevention
- HTTPS enforcement
- API key rotation

## Performance Architecture

### Backend Performance
- Async/await for non-blocking operations
- Connection pooling for database (future)
- Response caching strategies
- Background task processing

### Frontend Performance
- Next.js automatic code splitting
- Image optimization
- Lazy loading of components
- Efficient state updates
- Tailwind CSS purging

## Scalability Considerations

### Horizontal Scaling
- Stateless backend design
- Load balancer ready
- Database connection pooling
- Microservices architecture ready

### Vertical Scaling
- Efficient memory usage
- Optimized database queries
- Caching strategies
- Resource monitoring

## Monitoring and Observability

### Logging
- Structured logging with different levels
- Request/response logging
- Error tracking and reporting
- Performance metrics

### Health Checks
- `/health` endpoint for system status
- Database connectivity checks
- External service health monitoring
- Performance metrics collection

## Deployment Architecture

### Development Environment
- Local development servers
- Hot reloading for both frontend and backend
- Environment-specific configurations
- Development tools and debugging

### Production Environment
- Containerized deployment ready
- Environment variable management
- Reverse proxy configuration
- SSL/TLS termination
- CDN integration ready

## Integration Points

### External Services
- Google Gemini AI API
- Insurance data providers (future)
- Payment gateways (future)
- SMS/Email services (future)

### Internal Services
- User management system
- Policy management system
- Claims processing system
- Reporting and analytics

## Error Handling Strategy

### Backend Error Handling
- Structured error responses
- Error logging and monitoring
- Graceful degradation
- User-friendly error messages

### Frontend Error Handling
- Error boundaries for React components
- User-friendly error displays
- Retry mechanisms for failed requests
- Offline handling capabilities


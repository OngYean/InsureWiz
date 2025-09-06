# InsureWiz Development Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Development Workflow](#development-workflow)
5. [Code Standards](#code-standards)
6. [Testing](#testing)
7. [Debugging](#debugging)
8. [Deployment](#deployment)
9. [Contributing](#contributing)
10. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 18+** with npm
- **Git** for version control
- **Google AI Studio API Key** for AI functionality
- **VS Code** (recommended) with extensions:
  - Python
  - TypeScript and JavaScript
  - Tailwind CSS IntelliSense
  - Prettier
  - ESLint

### Quick Start
1. Clone the repository
2. Run the automated startup script
3. Access the application at http://localhost:3000

## Development Environment Setup

### Backend Setup

#### 1. Python Environment
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Environment Configuration
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your configuration
GOOGLE_API_KEY=your_google_api_key_here
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
LOG_LEVEL=info
DEBUG=true
```

#### 3. Start Development Server
```bash
# Run with auto-reload
python run.py

# Or use uvicorn directly
uvicorn app.core.app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

#### 1. Install Dependencies
```bash
cd frontend

# Install Node.js dependencies
npm install
```

#### 2. Environment Configuration
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=InsureWiz
NEXT_PUBLIC_APP_VERSION=1.0.0
```

#### 3. Start Development Server
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Project Structure

### Backend Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   ├── core/
│   │   ├── __init__.py
│   │   ├── app.py             # FastAPI application
│   │   └── database.py        # Database configuration
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/                # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── chat.py        # Chat endpoints
│   │   │   ├── policies.py    # Policy endpoints
│   │   │   ├── claims.py      # Claims endpoints
│   │   │   └── vehicles.py    # Vehicle endpoints
│   │   └── dependencies.py    # API dependencies
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py    # AI chat logic
│   │   ├── policy_service.py  # Policy management
│   │   ├── claim_service.py   # Claims processing
│   │   └── vehicle_service.py # Vehicle validation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chat.py            # Chat models
│   │   ├── policy.py          # Policy models
│   │   ├── claim.py           # Claim models
│   │   └── vehicle.py         # Vehicle models
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── cors.py            # CORS middleware
│   │   ├── logging.py         # Logging middleware
│   │   └── auth.py            # Authentication middleware
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py          # Helper functions
│       ├── validators.py       # Custom validators
│       └── constants.py        # Application constants
├── main.py                     # Application entry point
├── run.py                      # Development server runner
├── requirements.txt            # Python dependencies
└── env.example                 # Environment variables template
```

### Frontend Structure
```
frontend/
├── app/                        # Next.js 15 app router
│   ├── globals.css             # Global styles
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home page
│   ├── chat/                   # Chat feature
│   │   ├── page.tsx
│   │   └── components/
│   ├── policies/               # Policy management
│   │   ├── page.tsx
│   │   └── components/
│   ├── claims/                 # Claims processing
│   │   ├── page.tsx
│   │   └── components/
│   └── vehicles/               # Vehicle validation
│       ├── page.tsx
│       └── components/
├── components/                  # Reusable components
│   ├── ui/                     # shadcn/ui components
│   ├── forms/                  # Form components
│   ├── layout/                 # Layout components
│   └── common/                 # Common components
├── lib/                        # Utility functions
│   ├── api.ts                  # API client
│   ├── utils.ts                # Helper functions
│   ├── constants.ts            # Constants
│   └── types.ts                # TypeScript types
├── hooks/                      # Custom React hooks
├── styles/                     # Additional styles
├── public/                     # Static assets
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript configuration
├── tailwind.config.js          # Tailwind CSS configuration
└── next.config.mjs             # Next.js configuration
```

## Development Workflow

### 1. Feature Development
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push and create pull request
git push origin feature/new-feature
```

### 2. Code Review Process
1. Create feature branch
2. Implement feature with tests
3. Run linting and tests locally
4. Create pull request
5. Address review comments
6. Merge after approval

### 3. Commit Message Convention
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add new feature
fix: resolve bug
docs: update documentation
style: formatting changes
refactor: code restructuring
test: add or update tests
chore: maintenance tasks
```

## Code Standards

### Python (Backend)
- **Style**: Follow PEP 8
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Use Google-style docstrings
- **Imports**: Group imports (standard library, third-party, local)
- **Line Length**: Maximum 88 characters (Black formatter)

#### Example Python Code
```python
from typing import List, Optional
from fastapi import HTTPException, status
from pydantic import BaseModel

class ChatMessage(BaseModel):
    """Represents a chat message."""
    
    content: str
    sender: str
    timestamp: Optional[str] = None

async def process_chat_message(
    message: ChatMessage,
    conversation_id: Optional[str] = None
) -> dict:
    """
    Process a chat message and return AI response.
    
    Args:
        message: The chat message to process
        conversation_id: Optional conversation ID for context
        
    Returns:
        Dictionary containing AI response and metadata
        
    Raises:
        HTTPException: If message processing fails
    """
    try:
        # Process message logic here
        response = await ai_service.generate_response(message.content)
        return {
            "response": response,
            "conversation_id": conversation_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )
```

### TypeScript/JavaScript (Frontend)
- **Style**: Follow ESLint and Prettier configuration
- **TypeScript**: Use strict mode, avoid `any` type
- **Components**: Use functional components with hooks
- **Props**: Define proper interfaces for component props
- **Error Handling**: Use error boundaries and proper error states

#### Example TypeScript Code
```typescript
import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useChat } from '@/hooks/useChat';

interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: string;
}

interface ChatProps {
  initialMessages?: ChatMessage[];
  onMessageSent?: (message: ChatMessage) => void;
}

export const Chat: React.FC<ChatProps> = ({ 
  initialMessages = [], 
  onMessageSent 
}) => {
  const [inputValue, setInputValue] = useState('');
  const { messages, sendMessage, isLoading } = useChat(initialMessages);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const message: ChatMessage = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    await sendMessage(message);
    onMessageSent?.(message);
    setInputValue('');
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.sender === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-xs px-4 py-2 rounded-lg ${
                message.sender === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
      </div>
      
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex space-x-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-1"
          />
          <Button type="submit" disabled={isLoading || !inputValue.trim()}>
            Send
          </Button>
        </div>
      </form>
    </div>
  );
};
```

## Testing

### Backend Testing
```bash
# Install testing dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_chat_service.py
```

### Frontend Testing
```bash
# Install testing dependencies
npm install --save-dev jest @testing-library/react @testing-library/jest-dom

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- Chat.test.tsx
```

### Test Structure
```
tests/
├── backend/
│   ├── test_api/
│   ├── test_services/
│   └── test_models/
└── frontend/
    ├── __tests__/
    └── components/
```

## Debugging

### Backend Debugging
1. **Logging**: Use structured logging with different levels
2. **Debug Mode**: Enable debug mode in development
3. **Interactive Debugger**: Use `pdb` or `ipdb` for breakpoints
4. **API Documentation**: Use Swagger UI at `/docs`

### Frontend Debugging
1. **React DevTools**: Install browser extension
2. **Console Logging**: Use `console.log` and `console.error`
3. **Network Tab**: Monitor API calls in browser dev tools
4. **Error Boundaries**: Implement error boundaries for graceful error handling

### Common Debugging Commands
```bash
# Backend
python -m pdb run.py
uvicorn app.core.app:app --reload --log-level debug

# Frontend
npm run dev -- --debug
```

## Deployment

### Development Deployment
```bash
# Backend
cd backend
python run.py

# Frontend
cd frontend
npm run dev
```

### Production Deployment
```bash
# Backend
cd backend
pip install -r requirements.txt
gunicorn app.core.app:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
cd frontend
npm run build
npm start
```

### Docker Deployment
```dockerfile
# Backend Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.core.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

### 1. Fork and Clone
```bash
git clone https://github.com/your-username/InsureWiz.git
cd InsureWiz
```

### 2. Set Up Development Environment
Follow the setup instructions above for both backend and frontend.

### 3. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes
- Follow code standards
- Write tests for new functionality
- Update documentation
- Ensure all tests pass

### 5. Commit and Push
```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### 6. Create Pull Request
- Provide clear description of changes
- Include any relevant issue numbers
- Request review from maintainers

## Troubleshooting

### Common Issues

#### Backend Issues
1. **Import Errors**: Ensure virtual environment is activated
2. **Port Conflicts**: Change port in configuration or kill conflicting processes
3. **API Key Issues**: Verify Google API key is valid and has proper permissions
4. **Dependency Issues**: Reinstall requirements with `pip install -r requirements.txt --force-reinstall`

#### Frontend Issues
1. **Build Errors**: Clear cache with `npm run clean` or delete `.next` folder
2. **Dependency Issues**: Delete `node_modules` and reinstall
3. **TypeScript Errors**: Check type definitions and ensure proper imports
4. **Styling Issues**: Verify Tailwind CSS configuration and class names

#### General Issues
1. **CORS Errors**: Check backend CORS configuration
2. **Network Issues**: Verify API endpoints and network connectivity
3. **Performance Issues**: Check browser dev tools for bottlenecks
4. **Memory Issues**: Monitor memory usage and optimize if necessary

### Getting Help
1. Check existing issues on GitHub
2. Review documentation and code comments
3. Ask questions in discussions or issues
4. Contact maintainers for urgent issues

### Performance Optimization
1. **Backend**: Use async/await, implement caching, optimize database queries
2. **Frontend**: Implement lazy loading, optimize bundle size, use React.memo
3. **Database**: Add indexes, optimize queries, implement connection pooling
4. **Caching**: Implement Redis for session storage and response caching


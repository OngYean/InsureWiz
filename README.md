# InsureWiz - AI-Powered Insurance Platform

InsureWiz is a comprehensive insurance platform that combines modern web technologies with AI-powered assistance to help users understand insurance concepts, compare policies, and get expert advice.

## 📌 Track Info

**Track 3: Industry Collaboration**

When buying or renewing car insurance online, users often mistype or enter incorrect vehicle details. Build a smart system that detects and corrects typos or inaccurate vehicle input specifications in real time.

## 🚀 Features

- **🤖 AI Insurance Advisor**: Intelligent chatbot powered by LangChain and Google Gemini
- **📊 Policy Comparison**: Compare different insurance policies and coverage options
- **🔍 Claims Processing**: Streamlined claims submission and tracking
- **🎯 Claim Success Predictor**: AI-powered prediction of insurance claim success rates
- **🚗 Vehicle Validation**: Comprehensive vehicle information validation
- **🎨 Modern UI**: Beautiful, responsive interface built with Next.js and Tailwind CSS
- **💬 Real-time Chat**: Live AI assistance for insurance questions

## 🏗️ Architecture

- **Frontend**: Next.js 15 with TypeScript, Tailwind CSS, and shadcn/ui components
- **Backend**: FastAPI with Python, LangChain for AI integration
- **AI**: Google Gemini Pro model via LangChain for intelligent responses
- **Database**: In-memory storage (can be extended to PostgreSQL/MySQL)

## 📋 Prerequisites

- **Python 3.8+** with pip
- **Node.js 18+** with npm
- **Google AI Studio API Key** (required for AI functionality)

## 🚀 Quick Start

### Option 1: Automated Startup (Windows)

1. **Double-click** `start-project.bat` or run `start-project.ps1` in PowerShell
2. The script will automatically:
   - Check prerequisites
   - Start the AI backend server
   - Start the frontend development server
   - Open both in separate windows

### Option 2: Automated Startup (Linux)

1. **Run** the following command in your terminal:

   ```bash
   bash start-project.sh
   ```

   > If the terminal shows **Permission denied**, consider running the command above with `sudo`.

2. The script will automatically:

   - Check prerequisites (Python, Node.js)
   - Start the AI backend server in a new terminal window
   - Start the frontend development server in a new terminal window (using `next dev`)
   - Show URLs and tips for stopping servers

### Option 3: Manual Startup

#### 1. Start the AI Backend

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

# Copy environment file and add your Google API key
cp env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_api_key_here
```

**Getting a Google API Key:**

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key to your `.env` file

```bash
# Start the server
python run.py
```

The backend will be available at: http://localhost:8000

#### 2. Start the Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at: http://localhost:3000

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
LOG_LEVEL=info
```

### Frontend Configuration

The frontend automatically connects to the backend at `http://localhost:8000`. If you need to change this, update the API endpoints in the components.

## 📚 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/chat` - Send message to AI advisor
- `GET /api/conversations/{id}` - Get conversation history
- `DELETE /api/conversations/{id}` - Delete conversation
- `POST /api/advanced/claim` - Predict insurance claim success rate
- `GET /api/advanced/health` - Claim predictor health check
- `GET /health` - Health check

## 🎯 Usage

### AI Insurance Advisor

1. Navigate to the AI Advisor page
2. Ask questions about insurance concepts, policies, or claims
3. Get intelligent, contextual responses powered by Google Gemini
4. Maintain conversation context across sessions

### Claim Success Predictor

1. Navigate to the Claims page
2. Fill out the comprehensive 7-step form with incident details
3. Upload policy documents and evidence files
4. Get AI-powered prediction of claim success probability
5. Receive detailed insights and recommendations

### Policy Comparison

1. Use the comparison tool to evaluate different insurance options
2. Compare coverage, deductibles, and premiums
3. Make informed decisions about your insurance needs

### Claims Processing

1. Submit insurance claims through the streamlined interface
2. Track claim status and progress
3. Get guidance on required documentation

## 🛠️ Development

### Backend Development

```bash
cd backend

# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
python run.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Project Structure

```
InsureWiz/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # Main application
│   ├── run.py              # Server runner
│   ├── requirements.txt     # Python dependencies
│   ├── env.example         # Environment variables template
│   └── README.md           # Backend documentation
├── frontend/                # Next.js frontend
│   ├── app/                # App router pages
│   ├── components/         # React components
│   ├── lib/                # Utility functions
│   └── package.json        # Node.js dependencies
├── start-project.bat       # Windows startup script
├── start-project.ps1       # PowerShell startup script
└── README.md               # This file
```

## 🔒 Security Considerations

- **API Keys**: Never commit API keys to version control
- **CORS**: Backend is configured for local development only
- **Rate Limiting**: Consider implementing rate limiting for production
- **Authentication**: Add user authentication for production use

## 🚀 Production Deployment

### Backend

1. Use production ASGI server (Gunicorn)
2. Set up proper environment variables
3. Configure reverse proxy (nginx)
4. Use production database
5. Implement authentication and rate limiting
6. Monitor Google AI Studio API usage and costs

### Frontend

1. Build the application: `npm run build`
2. Deploy to Vercel, Netlify, or your preferred hosting
3. Update API endpoints to point to production backend
4. Configure environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Backend Connection Failed**

   - Ensure Python virtual environment is activated
   - Check that all dependencies are installed
   - Verify Google API key is set correctly

2. **Frontend Build Errors**

   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility

3. **Port Already in Use**

   - Change ports in configuration files
   - Kill processes using the ports: `netstat -ano | findstr :8000`

4. **Gemini API Issues**

   - Check your Google AI Studio quota and billing status
   - Verify API key is valid and has proper permissions

### Getting Help

- Check the API documentation at http://localhost:8000/docs
- Review the backend logs for error messages
- Ensure all prerequisites are met
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey) for API key issues

## 🙏 Acknowledgments

- Built with [Next.js](https://nextjs.org/)
- AI powered by [Google Gemini](https://ai.google.dev/) and [LangChain](https://langchain.com/)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- Styling with [Tailwind CSS](https://tailwindcss.com/)

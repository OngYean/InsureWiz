# Malaysian Motor Insurance Comparator

A comprehensive LangChain-powered AI agent for comparing Malaysian motor insurance policies from 9 major insurers.

## Features

- **Web Crawling**: Automated crawling of insurance company websites using Tavily API and Crawl4AI
- **AI-Powered Extraction**: LangChain integration with Google Gemini for structured data extraction
- **Intelligent Comparison**: Weighted scoring algorithm considering coverage, service, pricing, and Takaful preferences
- **Professional Reports**: PDF generation with Jinja2 templates and WeasyPrint
- **Compliance**: BNM professionalism guidelines and PDPA data protection

## Supported Insurers

1. **Zurich Malaysia** (Z-Driver, Motor Comprehensive)
2. **Etiqa** (Private Car, Takaful)
3. **Allianz General Insurance Malaysia**
4. **AXA Affin General**
5. **Generali Malaysia**
6. **Liberty Insurance**
7. **AmGeneral**
8. **Takaful Ikhlas**
9. **Berjaya Sompo**

## Architecture

```
app/comparator/
├── models/           # Pydantic data models
├── database/         # Supabase integration
├── scrapers/         # Insurer-specific scrapers
├── chains/           # LangChain processing
├── services/         # Core business logic
├── utils/            # Utilities and helpers
├── templates/        # Jinja2 templates
└── api/              # FastAPI endpoints
```

## API Endpoints

### Crawling
- `POST /api/comparator/crawl/discover` - Discover insurance URLs
- `POST /api/comparator/crawl/extract` - Extract and normalize policy data
- `POST /api/comparator/crawl/urls` - Crawl specific URLs

### Comparison
- `POST /api/comparator/compare/quick` - Quick policy comparison
- `POST /api/comparator/compare/detailed` - Detailed comparison with full customer profile
- `GET /api/comparator/compare/session/{id}` - Retrieve comparison session

### Reports
- `GET /api/comparator/reports/pdf/{session_id}` - Generate PDF report
- `GET /api/comparator/reports/preview/{session_id}` - HTML preview
- `POST /api/comparator/reports/email/{session_id}` - Email report

## Quick Start

### 1. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Configure required variables
GOOGLE_API_KEY=your_gemini_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
TAVILY_API_KEY=your_tavily_api_key
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Service
```bash
python start_server.py
```

### 4. Test the API
```bash
# Health check
curl http://localhost:8000/api/comparator/health

# Quick comparison
curl -X POST http://localhost:8000/api/comparator/compare/quick \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_type": "sedan",
    "coverage_type": "comprehensive",
    "max_price": 3000,
    "prefer_takaful": false
  }'
```

## Usage Examples

### Quick Comparison
```python
import requests

response = requests.post("http://localhost:8000/api/comparator/compare/quick", json={
    "vehicle_type": "sedan",
    "coverage_type": "comprehensive", 
    "max_price": 3000,
    "prefer_takaful": False
})

comparison = response.json()
print(f"Top recommendation: {comparison['ranked_policies'][0]['policy']['insurer']}")
```

### Detailed Comparison
```python
detailed_request = {
    "customer_input": {
        "personal_info": {
            "age": 30,
            "gender": "male",
            "driving_experience_years": 10,
            "annual_income": 80000
        },
        "vehicle_info": {
            "make": "Honda",
            "model": "Civic", 
            "year": 2020,
            "vehicle_value": 85000,
            "ncd_percentage": 25
        },
        "preferences": {
            "coverage_preference": "comprehensive",
            "price_range_max": 3000,
            "prefers_takaful": False,
            "important_features": ["roadside_assistance", "windscreen_cover"]
        }
    },
    "weights": {
        "coverage_weight": 0.30,
        "service_weight": 0.25,
        "pricing_weight": 0.25,
        "eligibility_weight": 0.10,
        "takaful_weight": 0.10
    }
}

response = requests.post("http://localhost:8000/api/comparator/compare/detailed", 
                        json=detailed_request)
session_id = response.json()["session_id"]
```

### Generate PDF Report
```python
# Generate PDF report
pdf_response = requests.get(f"http://localhost:8000/api/comparator/reports/pdf/{session_id}")

# Save PDF
with open("insurance_comparison.pdf", "wb") as f:
    f.write(pdf_response.content)
```

## Scoring Algorithm

The comparison uses a weighted scoring system:

- **Coverage (25%)**: Breadth and quality of coverage options
- **Service (20%)**: Customer service ratings and claim settlement
- **Pricing (25%)**: Premium competitiveness and value for money  
- **Eligibility (15%)**: Match with customer profile and vehicle
- **Takaful (15%)**: Shariah compliance for Muslim customers

## Data Sources

- **Tavily API**: Intelligent web search for discovering insurance pages
- **Crawl4AI**: Advanced content extraction with JavaScript rendering
- **Supabase**: PostgreSQL database for policy storage and sessions
- **Google Gemini**: AI-powered data extraction and analysis

## Compliance

- **BNM Guidelines**: Professional conduct and fair representation
- **PDPA 2010**: Personal data protection and privacy
- **Disclaimers**: Clear limitations and recommendation disclaimers

## Development

### Adding New Insurers
1. Create scraper class inheriting from `BaseScraper`
2. Implement `extract_policies()` method
3. Add URL patterns and search terms
4. Register in `scraper_registry`

### Custom Templates
1. Create Jinja2 template in `templates/`
2. Add CSS styling and report structure
3. Register template in `PDFGenerator`

### Testing
```bash
# Run unit tests
pytest tests/

# Test specific insurer scraper
python -m app.comparator.scrapers.zurich
```

## Deployment

### Docker
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.core.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```bash
# Required
GOOGLE_API_KEY=your_gemini_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
TAVILY_API_KEY=your_tavily_api_key

# Optional
LOG_LEVEL=INFO
CRAWL_TIMEOUT=30
MAX_POLICIES_PER_INSURER=50
ENABLE_CACHING=true
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

## Support

For issues and questions:
- Create GitHub issues for bugs
- Check documentation for usage questions
- Review compliance guidelines for regulatory questions

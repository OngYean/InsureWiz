# InsureWiz API Reference

## API Overview
The InsureWiz API provides a RESTful interface for Malaysian insurance and Takaful operations, AI-powered chat functionality, and system management. The API is built with FastAPI and provides automatic OpenAPI documentation, with support for Malaysian insurance regulations and Takaful principles.

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com` (configurable)

## Authentication
Currently, the API operates without authentication for development purposes. Future versions will include:
- JWT token-based authentication
- API key management
- Role-based access control

## API Endpoints

### 1. Health Check

#### GET /health
Check the health status of the API server.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK`: Server is healthy
- `503 Service Unavailable`: Server is unhealthy

---

### 2. AI Chat Endpoints

#### POST /api/chat
Send a message to the AI Malaysian insurance and Takaful advisor and receive an intelligent response. The AI supports Malay (Bahasa Malaysia), English, and Chinese languages.

**Request Body:**
```json
{
  "message": "What is comprehensive car insurance?",
  "conversation_id": "optional-conversation-id",
  "user_context": {
    "user_type": "individual",
    "experience_level": "beginner",
    "language": "en",
    "location": "Malaysia"
  }
}
```

**Response:**
```json
{
  "response": "Comprehensive car insurance in Malaysia provides coverage for damage to your vehicle from various sources including theft, vandalism, natural disasters, and accidents with animals. It's the most extensive form of auto insurance coverage available. In Malaysia, this typically includes flood coverage under special perils and may affect your No Claim Discount (NCD).",
  "conversation_id": "conv_12345",
  "timestamp": "2024-01-15T10:30:00Z",
  "confidence_score": 0.95,
  "suggested_questions": [
    "What's the difference between comprehensive and third-party coverage in Malaysia?",
    "How does NCD work for comprehensive insurance?",
    "What special perils are covered in Malaysian comprehensive policies?"
  ],
  "language": "en",
  "malaysian_context": true
}
```

**Status Codes:**
- `200 OK`: Message processed successfully
- `400 Bad Request`: Invalid request format
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

**Error Response:**
```json
{
  "error": "Invalid message format",
  "detail": "Message field is required",
  "status_code": 400
}
```

---

#### GET /api/conversations/{conversation_id}
Retrieve the conversation history for a specific conversation.

**Path Parameters:**
- `conversation_id` (string): Unique identifier for the conversation

**Response:**
```json
{
  "conversation_id": "conv_12345",
  "messages": [
    {
      "id": "msg_1",
      "content": "What is comprehensive car insurance?",
      "timestamp": "2024-01-15T10:30:00Z",
      "sender": "user"
    },
    {
      "id": "msg_2",
      "content": "Comprehensive car insurance provides coverage for damage to your vehicle from various sources...",
      "timestamp": "2024-01-15T10:30:05Z",
      "sender": "assistant"
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:05Z"
}
```

**Status Codes:**
- `200 OK`: Conversation retrieved successfully
- `404 Not Found`: Conversation not found
- `500 Internal Server Error`: Server error

---

#### DELETE /api/conversations/{conversation_id}
Delete a specific conversation and its history.

**Path Parameters:**
- `conversation_id` (string): Unique identifier for the conversation

**Response:**
```json
{
  "message": "Conversation deleted successfully",
  "conversation_id": "conv_12345"
}
```

**Status Codes:**
- `200 OK`: Conversation deleted successfully
- `404 Not Found`: Conversation not found
- `500 Internal Server Error`: Server error

---

### 3. Policy Management Endpoints

#### GET /api/policies
Retrieve available insurance policies.

**Query Parameters:**
- `type` (string, optional): Filter by policy type (auto, home, life, health)
- `coverage_level` (string, optional): Filter by coverage level (basic, standard, premium)
- `limit` (integer, optional): Number of policies to return (default: 10)
- `offset` (integer, optional): Number of policies to skip (default: 0)

**Response:**
```json
{
  "policies": [
    {
      "id": "policy_001",
      "name": "Comprehensive Auto Insurance",
      "type": "auto",
      "coverage_level": "premium",
      "description": "Complete coverage for your vehicle including comprehensive and collision",
      "base_premium": 1200.00,
      "deductible": 500.00,
      "features": [
        "Comprehensive coverage",
        "Collision coverage",
        "Liability protection",
        "Roadside assistance"
      ]
    }
  ],
  "total_count": 1,
  "limit": 10,
  "offset": 0
}
```

**Status Codes:**
- `200 OK`: Policies retrieved successfully
- `400 Bad Request`: Invalid query parameters
- `500 Internal Server Error`: Server error

---

#### GET /api/policies/{policy_id}
Retrieve detailed information about a specific policy.

**Path Parameters:**
- `policy_id` (string): Unique identifier for the policy

**Response:**
```json
{
  "id": "policy_001",
  "name": "Comprehensive Auto Insurance",
  "type": "auto",
  "coverage_level": "premium",
  "description": "Complete coverage for your vehicle including comprehensive and collision",
  "base_premium": 1200.00,
  "deductible": 500.00,
  "features": [
    "Comprehensive coverage",
    "Collision coverage",
    "Liability protection",
    "Roadside assistance"
  ],
  "coverage_details": {
    "property_damage": 100000,
    "bodily_injury": 300000,
    "uninsured_motorist": 50000,
    "comprehensive_deductible": 500,
    "collision_deductible": 500
  },
  "exclusions": [
    "Racing or speed testing",
    "Commercial use",
    "Off-road driving"
  ]
}
```

**Status Codes:**
- `200 OK`: Policy retrieved successfully
- `404 Not Found`: Policy not found
- `500 Internal Server Error`: Server error

---

### 4. Claims Management Endpoints

#### POST /api/claims
Submit a new insurance claim.

**Request Body:**
```json
{
  "policy_id": "policy_001",
  "claim_type": "auto_accident",
  "description": "Rear-ended by another vehicle at traffic light",
  "incident_date": "2024-01-10T14:30:00Z",
  "location": {
    "address": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "zip_code": "12345"
  },
  "damage_estimate": 2500.00,
  "contact_info": {
    "name": "John Doe",
    "phone": "+1-555-0123",
    "email": "john.doe@email.com"
  }
}
```

**Response:**
```json
{
  "claim_id": "claim_12345",
  "status": "submitted",
  "submitted_at": "2024-01-15T10:30:00Z",
  "estimated_processing_time": "5-7 business days",
  "next_steps": [
    "Submit photos of damage",
    "Provide police report if available",
    "Schedule inspection appointment"
  ]
}
```

**Status Codes:**
- `201 Created`: Claim submitted successfully
- `400 Bad Request`: Invalid claim data
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

---

#### GET /api/claims/{claim_id}
Retrieve the status and details of a specific claim.

**Path Parameters:**
- `claim_id` (string): Unique identifier for the claim

**Response:**
```json
{
  "claim_id": "claim_12345",
  "policy_id": "policy_001",
  "status": "under_review",
  "claim_type": "auto_accident",
  "description": "Rear-ended by another vehicle at traffic light",
  "incident_date": "2024-01-10T14:30:00Z",
  "submitted_at": "2024-01-15T10:30:00Z",
  "current_step": "Damage assessment",
  "estimated_completion": "2024-01-25T00:00:00Z",
  "updates": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "status": "Claim submitted",
      "description": "Initial claim received and assigned to adjuster"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Claim retrieved successfully
- `404 Not Found`: Claim not found
- `500 Internal Server Error`: Server error

---

### 5. Vehicle Validation Endpoints

#### POST /api/vehicles/validate
Validate vehicle information and retrieve details with Malaysian JPJ integration.

**Request Body:**
```json
{
  "vin": "1HGBH41JXMN109186",
  "license_plate": "ABC1234",
  "state": "Selangor",
  "jpj_verification": true
}
```

**Response:**
```json
{
  "valid": true,
  "vehicle": {
    "vin": "1HGBH41JXMN109186",
    "make": "Honda",
    "model": "Civic",
    "year": 2021,
    "trim": "EX",
    "engine": "2.0L I4",
    "transmission": "CVT",
    "fuel_type": "Gasoline",
    "body_style": "Sedan",
    "color": "Blue"
  },
  "registration": {
    "status": "Active",
    "expiration": "2025-01-15",
    "owner": "Ahmad bin Abdullah",
    "jpj_status": "Valid",
    "road_tax_expiry": "2025-01-15",
    "insurance_status": "Active"
  },
  "malaysian_details": {
    "jpj_verified": true,
    "state_registration": "Selangor",
    "vehicle_category": "Private",
    "engine_capacity": "2000cc"
  }
}
```

**Status Codes:**
- `200 OK`: Vehicle validation completed
- `400 Bad Request`: Invalid vehicle data
- `404 Not Found`: Vehicle not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

---

### 6. Malaysian Insurance Endpoints

#### GET /api/insurance/ncd-calculator
Calculate No Claim Discount (NCD) for Malaysian motor insurance.

**Query Parameters:**
- `years_without_claim` (integer): Number of years without claims
- `policy_type` (string): Type of policy (comprehensive, third-party)
- `vehicle_type` (string): Type of vehicle (private, commercial)

**Response:**
```json
{
  "ncd_percentage": 55,
  "ncd_amount": 275.00,
  "base_premium": 500.00,
  "final_premium": 225.00,
  "ncd_tier": "55%",
  "next_tier": "60%",
  "years_to_next_tier": 1,
  "malaysian_standard": true
}
```

**Status Codes:**
- `200 OK`: NCD calculation completed successfully
- `400 Bad Request`: Invalid parameters
- `500 Internal Server Error`: Server error

---

#### GET /api/insurance/panel-hospitals
Retrieve list of panel hospitals for health insurance claims.

**Query Parameters:**
- `state` (string, optional): Filter by state
- `specialty` (string, optional): Filter by medical specialty
- `insurance_provider` (string, optional): Filter by insurance company

**Response:**
```json
{
  "hospitals": [
    {
      "name": "Hospital Kuala Lumpur",
      "state": "Kuala Lumpur",
      "specialties": ["General", "Cardiology", "Orthopedics"],
      "insurance_providers": ["AIA", "Great Eastern", "Prudential"],
      "address": "Jalan Pahang, Kuala Lumpur",
      "contact": "+603-2615-5555"
    }
  ],
  "total_count": 1,
  "malaysian_coverage": true
}
```

---

## Error Handling

### Standard Error Response Format
All API endpoints return errors in a consistent format:

```json
{
  "error": "Error type description",
  "detail": "Detailed error message",
  "status_code": 400,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Rate Limiting
Currently, the API operates without rate limiting. Future versions will implement:
- Per-endpoint rate limits
- User-based rate limiting
- IP-based rate limiting
- Rate limit headers in responses

## Pagination
For endpoints that return lists, pagination is supported:

**Query Parameters:**
- `limit`: Number of items per page (default: 10, max: 100)
- `offset`: Number of items to skip (default: 0)

**Response Headers:**
- `X-Total-Count`: Total number of items
- `X-Page-Count`: Total number of pages
- `X-Current-Page`: Current page number

## Data Validation
All API endpoints use Pydantic models for request/response validation:
- Automatic type conversion
- Required field validation
- Format validation (email, phone, etc.)
- Custom validation rules

## API Versioning
The current API version is v1. Future versions will be available at:
- `/api/v2/` for version 2
- `/api/v3/` for version 3

## SDKs and Libraries
Official client libraries are planned for:
- Python
- JavaScript/TypeScript
- Java
- .NET

## Support and Documentation
- **Interactive API Docs**: `/docs` (Swagger UI)
- **Alternative Docs**: `/redoc` (ReDoc)
- **OpenAPI Schema**: `/openapi.json`
- **GitHub Repository**: [InsureWiz Repository]
- **Issues**: [GitHub Issues]

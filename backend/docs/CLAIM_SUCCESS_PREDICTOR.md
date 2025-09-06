# InsureWiz Claim Success Predictor - Technical Documentation

## Overview

The InsureWiz Claim Success Predictor is a comprehensive AI-powered system that analyzes motor insurance claims to predict their likelihood of success. It combines machine learning models, computer vision, natural language processing, and intelligent document processing to provide accurate claim assessments.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                           │
│        Next.js 15 + TypeScript + React                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           7-Step Claim Form                         │   │
│  │  • Incident Details      • Vehicle Information     │   │
│  │  • Documentation        • Driver Details           │   │
│  │  • File Uploads         • AI Insights Display     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND LAYER                            │
│               FastAPI + Python 3.11+                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              PREDICTION PIPELINE                    │   │
│  │  ┌─────────────┬─────────────┬─────────────────┐   │   │
│  │  │  Document   │  Computer   │   ML Prediction │   │   │
│  │  │ Processing  │   Vision    │     Engine      │   │   │
│  │  │             │             │                 │   │   │
│  │  │ • PDF OCR   │ • ResNet50  │ • Linear Reg.   │   │   │
│  │  │ • Text Ext. │ • Damage    │ • Feature Eng.  │   │   │
│  │  │ • Fallback  │   Detection │ • Confidence    │   │   │
│  │  └─────────────┴─────────────┴─────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ AI Processing
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   AI/ML LAYER                               │
│  ┌──────────────┬──────────────┬──────────────────────┐    │
│  │  Document    │  Computer    │   LLM Insights       │    │
│  │  Intelligence│   Vision     │                      │    │
│  │              │              │                      │    │
│  │ • PyPDF      │ • PyTorch    │ • Google Gemini      │    │
│  │ • Tesseract  │ • ResNet50   │ • Policy Analysis    │    │
│  │ • pdf2image  │ • PIL        │ • Risk Assessment    │    │
│  │ • OCR Fall.  │ • Transform  │ • Recommendations   │    │
│  └──────────────┴──────────────┴──────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. **Document Processing Engine**

#### Primary Method: Direct PDF Text Extraction

- **Library**: `pypdf` (PyPDF)
- **Speed**: Very fast (milliseconds)
- **Accuracy**: 100% for text-based PDFs
- **Use Cases**: Standard policy documents, digital forms

#### Fallback Method: OCR Text Recognition

- **Libraries**: `pytesseract`, `pdf2image`, `PIL`
- **Engine**: Google Tesseract OCR
- **Configuration**: 300 DPI, English language
- **Performance**: 1-5 seconds per page, 95%+ accuracy
- **Triggers**: When direct extraction fails or returns insufficient text (<50 meaningful characters)

#### Implementation Details

```python
def extract_text_from_pdf(pdf_file: io.BytesIO) -> str:
    # 1. Validate PDF header
    # 2. Attempt direct text extraction
    # 3. Quality assessment (meaningful text check)
    # 4. Automatic OCR fallback if needed
    # 5. Error handling and logging
```

### 2. **Computer Vision System**

#### Model Architecture

- **Base Model**: ResNet50 (pre-trained ImageNet weights)
- **Fine-tuning**: Custom classification layer for damage detection
- **Classes**: 2 classes ('damage', 'no_damage')
- **Framework**: PyTorch
- **Device Support**: CUDA (GPU) / CPU fallback

#### Image Processing Pipeline

```python
def predict_image_label(image_bytes: bytes) -> str:
    # 1. Load image from bytes using PIL
    # 2. Apply transforms (resize, normalize)
    # 3. Model inference on GPU/CPU
    # 4. Softmax probability calculation
    # 5. Return predicted class label
```

#### Image Transforms

- Resize to 224x224 pixels
- Convert to tensor
- Normalize with ImageNet statistics
- RGB format compatibility

### 3. **Machine Learning Prediction Engine**

#### Model Type

- **Algorithm**: Linear Regression Pipeline
- **Framework**: scikit-learn
- **Serialization**: joblib for model persistence
- **Features**: 20+ engineered features from form data

#### Feature Engineering

```python
# Core Features Processed:
- Incident type (categorical encoding)
- Driver age (numerical)
- Vehicle age (numerical)
- Weather conditions (categorical)
- Road conditions (categorical)
- Police report status (binary)
- Traffic violations (numerical)
- Previous claims (numerical)
- Evidence quality (derived from CV)
- And 10+ additional factors
```

#### Prediction Pipeline

```python
def predict_regression(form_data: Dict, image_label: str) -> float:
    # 1. Feature extraction and encoding
    # 2. DataFrame construction
    # 3. Model prediction
    # 4. Normalization (0-1 range)
    # 5. Confidence calculation
```

### 4. **LLM Intelligence System**

#### AI Model Integration

- **Provider**: Google Generative AI (Gemini)
- **Model**: gemini-2.0-flash-exp
- **Context Window**: Large context for comprehensive analysis
- **Response Format**: Structured insights and recommendations

#### Enhanced Data Processing

```python
def get_ai_insights(form_data: dict, policy_text: str) -> str:
    # Comprehensive data integration:
    # - Incident details (type, time, weather, road conditions)
    # - Vehicle & driver information (age, specs, value)
    # - Documentation status (reports, witnesses, timing)
    # - Risk factors (violations, claims history)
    # - Policy coverage analysis
```

#### Intelligent Analysis Capabilities

**Risk Assessment**

- Driver profile evaluation based on age and experience
- Vehicle risk factors (age, value, engine capacity)
- Environmental condition impact analysis
- Damage severity correlation checks

**Documentation Analysis**

- Evidence completeness scoring
- Procedural compliance verification
- 24-hour reporting requirement checks
- Risk indicator identification

**Policy Matching**

- Coverage type alignment assessment
- Deductible implication analysis
- Exclusion identification
- Claims eligibility evaluation

## API Endpoints

### Primary Endpoint

```
POST /api/advanced/claim
```

#### Request Format

- **Method**: POST (Multipart form data)
- **policy_document**: UploadFile (PDF format)
- **evidence_files**: List[UploadFile] (images, documents)
- **form_data_json**: String (JSON-encoded form data)

#### Response Format

```json
{
  "prediction": 0.85,
  "confidence": 0.92,
  "ai_insights": "Detailed AI analysis...",
  "processing_time": 2.34,
  "model_version": "v1.2.0"
}
```

### Health Check Endpoint

```
GET /api/advanced/health
```

#### Response

```json
{
  "status": "healthy",
  "timestamp": "2025-09-06T10:30:00Z",
  "features": {
    "ml_prediction": "ready",
    "cv_analysis": "ready",
    "llm_insights": "ready",
    "pdf_processing": "ready"
  }
}
```

## Data Flow

### Complete Prediction Pipeline

```
1. Form Submission → FastAPI Backend
2. File Processing → PDF Text Extraction (OCR fallback)
3. Image Analysis → Computer Vision Damage Detection
4. Feature Engineering → ML Model Input Preparation
5. ML Prediction → Linear Regression Inference
6. LLM Analysis → Comprehensive Insights Generation
7. Response Assembly → JSON Result Compilation
8. Frontend Display → Speedometer + AI Insights
```

### Error Handling & Fallbacks

```
PDF Processing: Direct extraction → OCR fallback → Empty string
CV Analysis: Model inference → "unknown" label → Continue pipeline
ML Prediction: Feature processing → Default confidence → Error response
LLM Insights: API call → Retry logic → Fallback message
```

## Performance Characteristics

### Processing Speed

- **Form Processing**: <100ms
- **PDF Text Extraction**: 50ms-5s (depending on OCR usage)
- **Computer Vision**: 200-500ms
- **ML Prediction**: <50ms
- **LLM Insights**: 1-3s
- **Total Pipeline**: 2-8s typical

### Accuracy Metrics

- **PDF Text Extraction**: 100% (direct), 95%+ (OCR)
- **Damage Detection**: 90%+ on clear images
- **Claim Prediction**: Model-dependent, validated on test data
- **Overall Confidence**: Weighted combination of component confidences

### Resource Requirements

- **Memory**: 2-4GB for model loading
- **CPU**: Multi-core recommended for OCR processing
- **GPU**: Optional (improves CV inference speed)
- **Storage**: ~500MB for model files

## Dependencies

### System Requirements

```bash
# OCR Engine
sudo apt-get install tesseract-ocr

# Image processing libraries
sudo apt-get install python3-dev
```

### Python Packages

```bash
# Core ML/AI
torch>=2.0.0
torchvision>=0.15.0
scikit-learn>=1.3.0
joblib>=1.3.0

# Document Processing
pypdf>=3.0.0
pytesseract>=0.3.10
pdf2image>=3.1.0
pillow>=10.0.0

# LLM Integration
google-generativeai>=0.3.0

# API Framework
fastapi>=0.104.0
uvicorn>=0.24.0
python-multipart>=0.0.6
```

## Configuration

### Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_google_ai_api_key

# Optional
TESSERACT_CMD=/usr/bin/tesseract  # Custom Tesseract path
CUDA_VISIBLE_DEVICES=0           # GPU selection
```

### Model Paths

```python
MODELS_DIR = "app/ml/models/"
REGRESSION_MODEL = "linear_regression_pipeline.joblib"
CV_MODEL = "cv_resnet50_model.pth"
```

## Security Considerations

### Data Privacy

- Files processed in memory (no persistent storage)
- Temporary file cleanup after processing
- PDF content sanitization for LLM processing

### API Security

- File type validation (PDF, images only)
- File size limits (configurable)
- Request rate limiting
- Input sanitization

### Model Security

- Model file integrity checks
- Secure model loading procedures
- Error message sanitization

## Monitoring & Logging

### Logging Levels

```python
# Info Level
logger.info("Successfully extracted text using direct PDF parsing")
logger.info("OCR extracted text from page 1")
logger.info("Prediction completed successfully: 85%")

# Warning Level
logger.warning("Direct PDF parsing returned insufficient text, falling back to OCR")
logger.warning("OCR failed for page 3")

# Error Level
logger.error("Error extracting text from PDF: {error}")
logger.error("Prediction pipeline failed completely")
```

### Performance Metrics

- Processing time per request
- Success/failure rates by component
- Model inference statistics
- Resource utilization tracking

## Future Enhancements

### Planned Improvements

1. **Multi-language OCR Support**: Expand beyond English
2. **Advanced CV Models**: Implement damage severity estimation
3. **Real-time Processing**: WebSocket-based streaming updates
4. **Model Versioning**: A/B testing framework for ML models
5. **Caching Layer**: Redis for frequently accessed policy documents

### Scalability Considerations

- Horizontal scaling with load balancers
- Model serving optimization (ONNX, TensorRT)
- Asynchronous processing with task queues
- Microservice architecture decomposition

## Troubleshooting

### Common Issues

**OCR Processing Failures**

```bash
# Install missing system dependencies
sudo apt-get install tesseract-ocr libtesseract-dev

# Verify Tesseract installation
tesseract --version
```

**Model Loading Errors**

```python
# Check model file paths and permissions
os.path.exists(REGRESSION_MODEL_PATH)
os.access(CV_MODEL_PATH, os.R_OK)
```

**GPU Memory Issues**

```python
# Force CPU usage if GPU memory insufficient
DEVICE = torch.device("cpu")
```

**API Key Configuration**

```bash
# Verify environment variable
echo $GOOGLE_API_KEY

# Test API connectivity
python -c "import google.generativeai as genai; genai.configure(api_key='$GOOGLE_API_KEY')"
```

This technical documentation provides a comprehensive overview of the InsureWiz Claim Success Predictor system, covering architecture, implementation details, performance characteristics, and operational considerations.

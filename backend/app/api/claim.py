"""
Advanced Claim Prediction API endpoints with ML analysis
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from app.models.claim import ClaimPredictionResponse
from app.ml.predict import run_prediction
import json
import io
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/advanced", tags=["advanced"])

@router.get("/health")
async def claim_health():
    """Health check for claim prediction features"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "ml_prediction": "ready",
            "cv_analysis": "ready", 
            "llm_insights": "ready",
            "pdf_processing": "ready"
        }
    }

@router.post(
    "/claim",
    response_model=ClaimPredictionResponse,
    summary="Predict motor insurance claim success",
    description="""
This endpoint predicts the success rate of a motor insurance claim based on the details of the incident.
It takes into account various factors like incident type, weather conditions, and evidence provided.

**Note:** The prediction is based on a machine learning model and should be considered as an estimate, not a guarantee.
"""
)
async def predict_claim_success(
    policy_document: UploadFile = File(..., description="The user's policy document in PDF format."),
    evidence_files: List[UploadFile] = File(..., description="A list of supporting evidence files (images, videos, etc.)."),
    form_data_json: str = Form(..., description="A JSON string of the form data.")
):
    """
    Predicts the success of a motor insurance claim.

    - **policy_document**: The user's policy document (PDF).
    - **evidence_files**: Supporting evidence files.
    - **form_data_json**: A JSON string containing the form data.
    """
    try:
        logger.info("Starting claim prediction analysis")
        
        form_data = json.loads(form_data_json)
        
        # Read evidence files into memory
        evidence_files_bytes = [await file.read() for file in evidence_files]
        
        # Read policy document into an in-memory stream
        policy_document_stream = await policy_document.read()
        policy_document_io = io.BytesIO(policy_document_stream)

        # Get prediction from the ML models
        result = run_prediction(form_data, evidence_files_bytes, policy_document_io)

        if "error" in result:
            logger.error(f"Prediction error: {result['error']}")
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Prediction service error",
                    "error": result["error"]
                }
            )

        logger.info(f"Prediction completed successfully: {result.get('prediction', 0)}%")
        return ClaimPredictionResponse(**result)
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in form_data_json: {e}")
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON format in form data"
        )
    except Exception as e:
        logger.error(f"Unexpected error in claim prediction: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during claim prediction"
        )

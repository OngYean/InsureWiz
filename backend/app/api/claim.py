from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import List
from app.models.claim import ClaimPredictionRequest, ClaimPredictionResponse
import json

router = APIRouter()

@router.post(
    "/advanced/claim",
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
    form_data = json.loads(form_data_json)
    # Here you would process the uploaded files and form data,
    # and then use your machine learning model to make a prediction.
    # For now, we'll return a mock response.

    # Mock logic to generate a prediction
    prediction = 75
    confidence = 0.85
    key_factors = ["Police report filed", "Clear description of incident", "Evidence provided"]

    if form_data.get("vehicleDamage") == "total-loss":
        prediction -= 20
        key_factors.append("Vehicle is a total loss")

    if form_data.get("injuries") == "yes":
        prediction -= 10
        key_factors.append("Injuries reported")

    return ClaimPredictionResponse(
        prediction=prediction,
        confidence=confidence,
        key_factors=key_factors
    )

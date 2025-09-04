import joblib
import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights
from torchvision import transforms
from PIL import Image
import pandas as pd
import os
import logging
from typing import List, Dict, Any
import io
from .llm_insights import get_ai_insights, extract_text_from_pdf

# Configure logger
logger = logging.getLogger(__name__)

# --- Configuration ---
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
REGRESSION_MODEL_PATH = os.path.join(MODELS_DIR, 'linear_regression_pipeline.joblib')
CV_MODEL_PATH = os.path.join(MODELS_DIR, 'cv_resnet50_model.pth')
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Model Loading ---

def load_regression_model():
    """Loads the trained regression pipeline from disk."""
    try:
        model = joblib.load(REGRESSION_MODEL_PATH)
        print("Regression model loaded successfully.")
        return model
    except FileNotFoundError:
        print(f"Error: Regression model not found at {REGRESSION_MODEL_PATH}")
        return None

def load_cv_model():
    """Loads the fine-tuned CV model and prepares it for evaluation."""
    try:
        model = resnet50(weights=None)
        num_ftrs = model.fc.in_features
        # The model was trained on a dataset with 2 classes: 'damage', 'no_damage'
        model.fc = nn.Linear(num_ftrs, 2)
        model.load_state_dict(torch.load(CV_MODEL_PATH, map_location=DEVICE))
        model = model.to(DEVICE)
        model.eval()
        print("CV model loaded successfully.")
        return model
    except FileNotFoundError:
        print(f"Error: CV model not found at {CV_MODEL_PATH}")
        return None

# Load models on startup
regression_pipeline = load_regression_model()
cv_model = load_cv_model()
CV_CLASS_NAMES = ['damage', 'no_damage']

# --- Prediction Logic ---

def predict_image_label(image_bytes: bytes) -> str:
    """
    Predicts the label of an image using the loaded computer vision model.
    
    Args:
        image_bytes: Raw bytes of the image file.
        
    Returns:
        Predicted class name.
    """
    try:
        # Convert bytes to BytesIO stream for PIL
        image_stream = io.BytesIO(image_bytes)
        image = Image.open(image_stream)
        
        # Ensure the image is in RGB format
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Define the same preprocessing pipeline as training
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        image_tensor = preprocess(image).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            outputs = cv_model(image_tensor)
            _, preds = torch.max(outputs, 1)
        
        return CV_CLASS_NAMES[preds[0]]
        
    except Exception as e:
        print(f"Warning: Could not process image: {e}")
        # Return a default class if image processing fails
        return "unknown_damage"

def predict_regression(form_data: Dict[str, Any], image_label: str = "unknown") -> float:
    """
    Makes a prediction using the regression model.
    
    Args:
        form_data: Dictionary containing form fields
        image_label: Label from CV model prediction
        
    Returns:
        Prediction value between 0 and 1, or None if prediction fails
    """
    try:
        # Convert image label to binary
        image_label_binary = 1 if image_label == "damage" else 0
        
        # Helper function to convert yes/no to binary
        def yes_no_to_binary(value):
            if isinstance(value, str):
                return 1 if value.lower() == "yes" else 0
            return int(bool(value))
        
        # Map frontend form data to model expected features
        model_data = {
            # Image analysis (binary)
            'image_label': image_label_binary,
            
            # Incident details (categorical strings)
            'incidentType': form_data.get('incidentType', 'collision'),
            'timeOfDay': form_data.get('timeOfDay', 'afternoon'),
            'roadConditions': form_data.get('roadConditions', 'dry'),
            'weatherConditions': form_data.get('weatherConditions', 'clear'),
            
            # Damage and parties (categorical strings)
            'injuries': form_data.get('injuries', 'no'),
            'vehicleDamage': form_data.get('vehicleDamage', 'moderate'),
            'thirdPartyVehicle': form_data.get('thirdPartyVehicle', 'yes'),
            'witnesses': form_data.get('witnesses', 'no'),
            'policeReport': form_data.get('policeReport', 'no'),
            
            # Documentation (binary)
            'policeReportFiledWithin24h': yes_no_to_binary(form_data.get('policeReportFiledWithin24h', 'no')),
            'trafficViolation': yes_no_to_binary(form_data.get('trafficViolation', 'no')),
            'previousClaims': yes_no_to_binary(form_data.get('previousClaims', 'no'))
        }
        
        # Create a DataFrame from mapped data
        df = pd.DataFrame([model_data])
        
        # Transform the data using the loaded pipeline
        prediction = regression_pipeline.predict(df)
        
        # The model returns percentage values, ensure they're in reasonable range
        raw_prediction = float(prediction[0])
        
        # If prediction is already a percentage (0-100), normalize to 0-1
        if raw_prediction > 1:
            normalized_prediction = raw_prediction / 100.0
        else:
            normalized_prediction = raw_prediction
            
        # Ensure it's within bounds
        return max(0.0, min(1.0, normalized_prediction))
        
    except Exception as e:
        logger.error(f"Error during regression prediction: {e}")
        return None

def calculate_prediction_score(form_data: Dict[str, Any], image_labels: List[str]) -> int:
    """
    Calculate a prediction score based on available form data and image analysis.
    
    Args:
        form_data: Dictionary containing form fields
        image_labels: List of detected damage labels from images
        
    Returns:
        Prediction score between 0 and 100
    """
    score = 50  # Base score
    
    # Factor 1: Driver age (younger drivers have higher claim success rates for certain scenarios)
    driver_age = form_data.get("driver_age", 30)
    if driver_age < 25:
        score += 10  # Young drivers often have clearer fault determination
    elif driver_age > 65:
        score += 5   # Senior drivers often have good documentation
    
    # Factor 2: Vehicle age (newer vehicles have better documentation)
    vehicle_age = form_data.get("vehicle_age", 5)
    if vehicle_age < 3:
        score += 15  # New vehicles have better coverage
    elif vehicle_age < 10:
        score += 5
    else:
        score -= 5   # Older vehicles may have coverage limitations
    
    # Factor 3: Market value (higher value vehicles get more attention)
    market_value = form_data.get("market_value", 25000)
    if market_value > 100000:
        score += 10  # High-value vehicles
    elif market_value > 50000:
        score += 5
    elif market_value < 15000:
        score -= 10  # Low-value vehicles may have minimal coverage
    
    # Factor 4: Engine capacity (affects coverage tiers)
    engine_capacity = form_data.get("engine_capacity", 1600)
    if engine_capacity > 3000:
        score += 5   # Higher capacity vehicles often have comprehensive coverage
    elif engine_capacity < 1000:
        score -= 5   # Very small engines may indicate basic coverage
    
    # Factor 5: Incident description analysis
    incident_desc = form_data.get("incident_description", "").lower()
    if any(word in incident_desc for word in ["hit", "rear-end", "collision"]):
        score += 10  # Clear impact scenarios
    if any(word in incident_desc for word in ["parking", "stationary"]):
        score += 15  # Parking lot incidents often have clear fault
    if any(word in incident_desc for word in ["theft", "stolen"]):
        score += 20  # Theft claims are usually straightforward
    if any(word in incident_desc for word in ["flood", "water"]):
        score -= 10  # Natural disasters may have exclusions
    
    # Factor 6: Evidence quality
    if image_labels:
        if "damage" in str(image_labels).lower():
            score += 15  # Clear damage evidence
        elif "unknown_damage" in image_labels:
            score += 5   # Some evidence provided
    else:
        score -= 15  # No visual evidence
    
    # Ensure score is within bounds
    return max(5, min(95, score))

def run_prediction(
    form_data: Dict[str, Any], 
    evidence_files: List[bytes],
    policy_document: io.BytesIO
) -> Dict[str, Any]:
    """
    Runs the complete prediction pipeline combining CV, regression, and LLM models.
    
    Args:
        form_data: Dictionary containing form fields
        evidence_files: List of uploaded image files as bytes
        policy_document: PDF document as BytesIO stream
        
    Returns:
        Dictionary containing prediction results and AI insights
    """
    try:
        logger.info("Starting complete prediction pipeline")
        
        # Process evidence files with CV model
        image_labels = []
        if evidence_files:
            for img_bytes in evidence_files:
                try:
                    label = predict_image_label(img_bytes)
                    image_labels.append(label)
                except Exception as e:
                    logger.warning(f"Failed to process image: {e}")
                    image_labels.append("unknown_damage")
        
        # Create a base prediction response with calculated score
        base_score = calculate_prediction_score(form_data, image_labels)
        result = {
            "prediction": base_score,
            "confidence": 0.85,
            "key_factors": [
                "incident_description_analysis",
                "evidence_file_analysis" if evidence_files else "no_evidence_provided",
                "policy_document_uploaded"
            ]
        }
        
        # Try to run regression model prediction
        primary_image_label = image_labels[0] if image_labels else "unknown"
        try:
            regression_prediction = predict_regression(form_data, primary_image_label)
            if regression_prediction is not None:
                result["prediction"] = max(0, min(100, int(regression_prediction * 100)))
                result["key_factors"].append("ml_regression_model")
                logger.info(f"Regression prediction successful: {result['prediction']}%")
            else:
                logger.warning("Regression prediction returned None, using calculated score")
                result["key_factors"].append("calculated_fallback")
        except Exception as e:
            logger.error(f"Regression prediction failed: {e}")
            result["key_factors"].append("calculated_fallback_error")
        
        # Extract policy text and generate AI insights
        ai_insights = "AI insights are currently unavailable."
        try:
            incident_description = form_data.get("incident_description", "")
            policy_text = extract_text_from_pdf(policy_document)
            
            if policy_text and len(policy_text.strip()) > 20:
                ai_insights = get_ai_insights(incident_description, policy_text)
                logger.info("AI insights generated successfully")
            else:
                ai_insights = "Unable to analyze policy document. Please ensure you upload a valid policy document for detailed insights."
                logger.warning("Policy text too short or empty")
                
        except Exception as e:
            logger.error(f"AI insights generation failed: {e}")
            ai_insights = "AI insights are temporarily unavailable due to a technical issue."
        
        result["ai_insights"] = ai_insights
        
        logger.info(f"Complete prediction pipeline finished. Final prediction: {result['prediction']}%")
        return result
        
    except Exception as e:
        logger.error(f"Prediction pipeline failed completely: {e}")
        return {
            "error": f"Prediction service temporarily unavailable: {str(e)}",
            "prediction": 50,  # Neutral fallback
            "confidence": 0.5,
            "key_factors": ["service_error"],
            "ai_insights": "Unable to provide insights at this time."
        }

import os
import google.generativeai as genai
from pypdf import PdfReader
import io
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import logging

# Configure logger
logger = logging.getLogger(__name__)

# It's recommended to set the API key as an environment variable
# For example: export GOOGLE_API_KEY="YOUR_API_KEY"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def extract_text_with_ocr(pdf_file: io.BytesIO) -> str:
    """Extracts text from PDF using OCR as a fallback method."""
    try:
        # Reset file pointer to beginning
        pdf_file.seek(0)
        
        # Convert PDF pages to images
        images = convert_from_bytes(pdf_file.getvalue(), dpi=300, first_page=1, last_page=5)  # Limit to first 5 pages
        
        text = ""
        for i, image in enumerate(images):
            try:
                # Use pytesseract to extract text from image
                page_text = pytesseract.image_to_string(image, lang='eng')
                if page_text.strip():
                    # Clean text to remove problematic characters
                    cleaned_text = page_text.replace('\x00', '').replace('\r', ' ').replace('\n', ' ')
                    text += cleaned_text + " "
                    logger.info(f"OCR extracted text from page {i+1}")
            except Exception as e:
                logger.warning(f"OCR failed for page {i+1}: {e}")
                continue
                
        return text.strip()
    except Exception as e:
        logger.error(f"Error in OCR text extraction: {e}")
        return ""

def extract_text_from_pdf(pdf_file: io.BytesIO) -> str:
    """Extracts text from an in-memory PDF file with OCR fallback."""
    try:
        # Check if the file has content
        if pdf_file.getbuffer().nbytes == 0:
            return ""
            
        # Reset file pointer to beginning
        pdf_file.seek(0)
        
        # Read a small portion to check if it's a valid PDF
        header = pdf_file.read(5)
        pdf_file.seek(0)
        
        # Check if it starts with PDF header
        if not header.startswith(b'%PDF-'):
            return ""
            
        # First attempt: Direct text extraction using pypdf
        try:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    # Clean text to remove null bytes and other problematic characters
                    cleaned_text = page_text.replace('\x00', '').replace('\r', ' ').replace('\n', ' ')
                    text += cleaned_text + " "
            
            # Check if we got meaningful text (more than just whitespace and basic punctuation)
            meaningful_text = ''.join(c for c in text if c.isalnum())
            
            if len(meaningful_text) > 50:  # If we have sufficient meaningful text
                logger.info("Successfully extracted text using direct PDF parsing")
                return text.strip()
            else:
                logger.info("Direct PDF parsing returned insufficient text, falling back to OCR")
                
        except Exception as e:
            logger.warning(f"Direct PDF text extraction failed: {e}, falling back to OCR")
        
        # Fallback: Use OCR
        ocr_text = extract_text_with_ocr(pdf_file)
        if ocr_text:
            logger.info("Successfully extracted text using OCR fallback")
            return ocr_text
        else:
            logger.warning("Both direct extraction and OCR failed")
            return ""
            
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return ""

def get_ai_insights(form_data: dict, policy_text: str) -> str:
    """
    Generates AI insights based on complete claim form data and policy text using Gemini.
    
    Args:
        form_data: Complete form data dictionary containing all claim details
        policy_text: Extracted text from the insurance policy document
        
    Returns:
        AI-generated insights and recommendations as a string
    """
    if not GOOGLE_API_KEY:
        return "API key for Google Generative AI is not configured. Please set the GOOGLE_API_KEY environment variable."

    try:
        # Extract and clean form data
        incident_description = str(form_data.get("incident_description", "")).strip()
        incident_type = str(form_data.get("incidentType", "")).strip()
        driver_age = form_data.get("driver_age", "Not specified")
        vehicle_age = form_data.get("vehicle_age", "Not specified")
        engine_capacity = form_data.get("engine_capacity", "Not specified")
        market_value = form_data.get("market_value", "Not specified")
        vehicle_damage = str(form_data.get("vehicleDamage", "")).strip()
        time_of_day = str(form_data.get("timeOfDay", "")).strip()
        weather_conditions = str(form_data.get("weatherConditions", "")).strip()
        road_conditions = str(form_data.get("roadConditions", "")).strip()
        injuries = str(form_data.get("injuries", "")).strip()
        third_party = str(form_data.get("thirdPartyVehicle", "")).strip()
        witnesses = str(form_data.get("witnesses", "")).strip()
        police_report = str(form_data.get("policeReport", "")).strip()
        police_within_24h = form_data.get("policeReportFiledWithin24h", 0)
        traffic_violation = form_data.get("trafficViolation", 0)
        previous_claims = form_data.get("previousClaims", 0)
        
        # Clean policy text
        clean_policy_text = policy_text.replace('\x00', '').strip() if policy_text else "No policy text available."
        
        # Build comprehensive claim summary
        claim_summary = f"""
**Incident Details:**
- Type: {incident_type or 'Not specified'}
- Description: {incident_description or 'No description provided'}
- Time: {time_of_day or 'Not specified'}
- Weather: {weather_conditions or 'Not specified'}
- Road Conditions: {road_conditions or 'Not specified'}

**Vehicle & Driver Information:**
- Driver Age: {driver_age}
- Vehicle Age: {vehicle_age} years
- Engine Capacity: {engine_capacity} CC
- Market Value: RM {market_value}
- Damage Severity: {vehicle_damage or 'Not assessed'}

**Parties & Documentation:**
- Injuries: {injuries or 'Not specified'}
- Third Party Involved: {third_party or 'Not specified'}
- Witnesses: {witnesses or 'Not specified'}
- Police Report Filed: {police_report or 'Not specified'}
- Police Report Within 24h: {'Yes' if police_within_24h else 'No'}
- Traffic Violation: {'Yes' if traffic_violation else 'No'}
- Previous Claims (3 years): {previous_claims}
"""
        
        # If policy text is too short or empty, provide insights based on form data only
        if len(clean_policy_text) < 50:
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            prompt = f"""
            As an expert AI insurance claims assistant, analyze this motor insurance claim based on the comprehensive information provided below. 

            {claim_summary}

            Provide concise, actionable insights (3-4 sentences) covering:
            - **Claim Likelihood:** Based on the incident type and circumstances
            - **Key Recommendations:** Critical actions the claimant should take
            - **Risk Factors:** Any elements that might affect the claim outcome

            Be direct, helpful, and professional. Focus on practical guidance.

            **AI Insights:**
            """
            
            response = model.generate_content(prompt)
            return response.text
        
        # Generate insights with both form data and policy text
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        prompt = f"""
        As an expert AI insurance claims assistant, analyze this motor insurance claim using both the detailed claim information and the policy document provided.

        **Comprehensive Claim Information:**
        {claim_summary}

        **Insurance Policy Excerpt:**
        {clean_policy_text[:2000]}

        Based on this complete information, provide insights that address:
        - **Policy Coverage:** Whether this incident type and circumstances are likely covered
        - **Critical Actions:** Essential steps based on policy requirements and claim details
        - **Risk Assessment:** Factors that could strengthen or weaken the claim
        - **Documentation:** Any missing evidence or documentation needs

        Keep your response to 3-4 clear, actionable sentences. Be specific about policy requirements and claim circumstances.

        **AI Insights:**
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        logger.error(f"Error generating AI insights: {e}")
        return "Could not generate AI insights at this time due to a technical issue."

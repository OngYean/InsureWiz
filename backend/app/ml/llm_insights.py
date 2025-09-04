import os
import google.generativeai as genai
from pypdf import PdfReader
import io

# It's recommended to set the API key as an environment variable
# For example: export GOOGLE_API_KEY="YOUR_API_KEY"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def extract_text_from_pdf(pdf_file: io.BytesIO) -> str:
    """Extracts text from an in-memory PDF file."""
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
            
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                # Clean text to remove null bytes and other problematic characters
                cleaned_text = page_text.replace('\x00', '').replace('\r', ' ').replace('\n', ' ')
                text += cleaned_text + " "
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def get_ai_insights(incident_description: str, policy_text: str) -> str:
    """
    Generates AI insights based on incident description and policy text using Gemini.
    """
    if not GOOGLE_API_KEY:
        return "API key for Google Generative AI is not configured. Please set the GOOGLE_API_KEY environment variable."

    try:
        # Clean inputs to remove any problematic characters
        clean_description = incident_description.replace('\x00', '').strip() if incident_description else "No description provided."
        clean_policy_text = policy_text.replace('\x00', '').strip() if policy_text else "No policy text available."
        
        # If policy text is too short or empty, provide a generic response
        if len(clean_policy_text) < 50:
            return "Unable to analyze policy document. Please ensure you upload a valid policy document for detailed insights."
        
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # Using the latest available flash model

        prompt = f"""
        As an expert AI insurance claims assistant, your task is to provide clear, concise, and helpful insights to a user about their motor insurance claim.

        You will be given two pieces of information:
        1. The user's description of the incident.
        2. The text extracted from their insurance policy document.

        Based on this information, analyze the situation and provide insights that address the following:
        - **Policy Coverage:** Briefly mention if the incident type (e.g., collision, theft) seems to be covered under the policy.
        - **Key Considerations:** Highlight 1-2 critical actions the user should take or be aware of (e.g., "Since you mentioned a third party was involved, be sure to get their contact and insurance details," or "Your policy mentions a specific timeline for reporting claims, so it's important to act quickly.").
        - **Potential Exclusions:** Point out any potential clauses or exclusions from the policy that might be relevant to the user's description (e.g., "Note that the policy may not cover damage if it resulted from a traffic violation.").

        Keep your response to a maximum of 3-4 short, easy-to-understand sentences. Do not start with a greeting. Be direct and helpful.

        ---
        **User's Incident Description:**
        "{clean_description}"

        ---
        **Insurance Policy Text:**
        "{clean_policy_text[:2000]}"
        ---

        **AI Insights:**
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Error generating AI insights: {e}")
        return "Could not generate AI insights at this time due to a technical issue."

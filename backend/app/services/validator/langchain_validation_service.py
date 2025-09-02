"""
LangChain-powered vehicle validation service with Tavily search integration
"""
import json
from typing import Dict, List, Optional, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from app.config import settings
from .data_loader import vehicle_data_loader


class TypoDetection(BaseModel):
    """Typo and error detection information"""
    brand_has_typo: bool = Field(default=False, description="Whether brand name contains typos")
    corrected_brand: Optional[str] = Field(default=None, description="Corrected brand name if typo detected")
    model_has_typo: bool = Field(default=False, description="Whether model name contains typos")
    corrected_model: Optional[str] = Field(default=None, description="Corrected model name if typo detected")
    year_has_error: bool = Field(default=False, description="Whether year input has errors")
    corrected_year: Optional[int] = Field(default=None, description="Corrected year if error detected")
    color_has_typo: bool = Field(default=False, description="Whether color name contains typos")
    corrected_color: Optional[str] = Field(default=None, description="Corrected color name if typo detected")


class InsuranceRisk(BaseModel):
    """Insurance-specific risk assessment"""
    policy_risk_level: str = Field(default="medium", description="Risk level: low, medium, high, critical")
    pricing_impact: str = Field(default="minor", description="Impact on insurance pricing: none, minor, moderate, significant")
    coverage_validity: str = Field(default="valid", description="Coverage validity: valid, questionable, invalid")
    fraud_indicators: List[str] = Field(default_factory=list, description="List of potential fraud indicators if any")


class ColorValidation(BaseModel):
    """Enhanced color validation information"""
    color_found_locally: bool = Field(description="Whether the color was found in local database")
    color_available_for_model: bool = Field(description="Whether the color is available for this model")
    alternative_colors: List[str] = Field(default_factory=list, description="List of alternative color options")
    color_verification_source: str = Field(default="local_database", description="Source of color verification (local_database or search)")
    insurance_color_category: str = Field(default="standard", description="Insurance color category (standard, premium, rare)")


class VehicleInfo(BaseModel):
    """Enhanced vehicle information"""
    brand: str = Field(description="Vehicle brand/manufacturer")
    model: str = Field(description="Vehicle model")
    year: str = Field(description="Vehicle year")
    market_availability: str = Field(default="available", description="Availability in Malaysian market")
    assembly_type: str = Field(default="unknown", description="Assembly type (local, import, etc.)")
    insurance_category: str = Field(default="family", description="Insurance vehicle category (economy, family, luxury, sports)")
    common_insurance_model: bool = Field(default=True, description="Whether this is a commonly insured model in Malaysia")


class VehicleValidationResult(BaseModel):
    """Enhanced structured vehicle validation result for insurance applications"""
    validation_status: str = Field(description="Validation status: valid, warning, invalid, or unable_to_verify")
    confidence_score: int = Field(description="Confidence score from 0 to 100")
    typo_detection: TypoDetection = Field(description="Typo and error detection results")
    insurance_risk: InsuranceRisk = Field(description="Insurance-specific risk assessment")
    color_validation: ColorValidation = Field(description="Color validation details")
    vehicle_info: VehicleInfo = Field(description="Vehicle information")
    search_performed: bool = Field(default=False, description="Whether external search was performed")
    image_urls: List[str] = Field(default_factory=list, description="List of vehicle image URLs")
    validation_notes: str = Field(default="", description="Additional validation notes")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for insurance application optimization")


class VehicleValidationAgent:
    """LangChain agent for comprehensive vehicle validation using Tavily search"""
    
    def __init__(self):
        # Initialize Google Gemini
        self.llm = ChatGoogleGenerativeAI(
            model=settings.ai_model,
            google_api_key=settings.google_api_key,
            temperature=0.1
        )
        
        # Initialize Tavily search tool
        self.tavily_tool = TavilySearch(
            api_key=settings.tavily_api_key,
            max_results=3,
            search_depth="basic",  # Use basic to conserve credits
            include_images=True,  # Enable image search
            include_answer=True
        )
        
        # Setup agent
        self._setup_agent()
    
    def _setup_agent(self):
        """Setup the LangChain structured output chain"""
        # Create system prompt for vehicle validation
        system_prompt = """You are an expert vehicle validation AI that MUST return structured JSON data for insurance applications.

🎯 CRITICAL: You MUST respond with valid JSON in the exact format specified. No explanatory text, no markdown, just the required JSON structure.

You must return a JSON object with ALL these fields filled:

{{
  "validation_status": "valid" | "warning" | "invalid" | "unable_to_verify",
  "confidence_score": <integer 0-100>,
  "typo_detection": {{
    "brand_has_typo": <boolean>,
    "corrected_brand": <string or null>,
    "model_has_typo": <boolean>,
    "corrected_model": <string or null>,
    "year_has_error": <boolean>,
    "corrected_year": <integer or null>,
    "color_has_typo": <boolean>,
    "corrected_color": <string or null>
  }},
  "insurance_risk": {{
    "policy_risk_level": "low" | "medium" | "high" | "critical",
    "pricing_impact": "none" | "minor" | "moderate" | "significant",
    "coverage_validity": "valid" | "questionable" | "invalid",
    "fraud_indicators": [<array of strings>]
  }},
  "color_validation": {{
    "color_found_locally": <boolean>,
    "color_available_for_model": <boolean>,
    "alternative_colors": [<array of strings>],
    "color_verification_source": "local_database" | "search" | "error",
    "insurance_color_category": "standard" | "premium" | "rare"
  }},
  "vehicle_info": {{
    "brand": <string>,
    "model": <string>,
    "year": <string>,
    "market_availability": "available" | "unavailable" | "unknown",
    "assembly_type": "local" | "import" | "unknown",
    "insurance_category": "economy" | "family" | "luxury" | "sports",
    "common_insurance_model": <boolean>
  }},
  "search_performed": <boolean>,
  "image_urls": [<array of strings>],
  "validation_notes": <string>,
  "recommendations": [<array of strings>]
}}

VALIDATION RULES FOR MALAYSIAN INSURANCE:
1. Common typos: Toyata→Toyota, Hond→Honda, Peroduaا→Perodua, Civick→Civic, Myvii→Myvi
2. Valid years: 1990-2025 for insurance applications
3. Popular Malaysian brands: Proton, Perodua, Toyota, Honda, Nissan, Mazda
4. Insurance categories: economy, family, luxury, sports
5. Risk levels: low, medium, high, critical

ALWAYS fill ALL required fields. Use these defaults if unsure:
- validation_status: "unable_to_verify"
- confidence_score: 50
- policy_risk_level: "medium"
- pricing_impact: "minor"
- coverage_validity: "valid"
- fraud_indicators: []
- alternative_colors: []
- image_urls: []
- recommendations: []

You MUST return valid JSON that matches this exact structure."""

        # Create structured LLM
        structured_llm = self.llm.with_structured_output(VehicleValidationResult)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        # Create the validation chain
        self.validation_chain = self.prompt | structured_llm
    
    async def validate_vehicle(self, vehicle_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate complete vehicle information
        
        Args:
            vehicle_data: Dict containing year, brand, model, color, owner_ic, plate_number
            
        Returns:
            Validation results with vehicle information
        """
        try:
            # First, check against local CSV data
            local_validation = self._validate_against_csv(vehicle_data)
            
            # Prepare validation input (excluding personal identifiers for search)
            year = vehicle_data.get('year')
            brand = vehicle_data.get('brand')
            model = vehicle_data.get('model')
            color = vehicle_data.get('color')
            
            validation_input = f"""
🚗 INSURANCE APPLICATION VEHICLE VALIDATION REQUEST

📋 USER INPUT DATA:
- Year: {year}
- Brand: {brand}  
- Model: {model}
- Color: {color}

🔍 TYPO & ERROR DETECTION ANALYSIS:
Please perform smart error detection on the above inputs:
1. Check for common brand name typos (e.g., "Toyata", "Hond", "Nisssan", "Peroduaا")
2. Identify model name misspellings (e.g., "Camry" variants, "Civick", "Myvii")
3. Validate year format and detect input errors (e.g., "202" instead of "2022")
4. Analyze color name variations and typos

📊 LOCAL DATABASE VERIFICATION:
- Brand found in {year}: {local_validation['brand_found']}
- Model found for brand: {local_validation['model_found']} 
- Color found for model: {local_validation['color_found']}
- Available colors in database: {', '.join(local_validation.get('available_colors', [])[:5])}
- Total records in year: {local_validation['total_records']}

🎯 INSURANCE-SPECIFIC VALIDATION REQUIREMENTS:
1. CRITICAL ERRORS (Would invalidate insurance policy):
   - Impossible year/model combinations
   - Non-existent vehicle specifications
   - Invalid Malaysian market vehicles

2. WARNING ISSUES (Could cause pricing errors or delays):
   - Uncommon color variants for specific models
   - Import vs local assembly discrepancies
   - Model year affecting insurance categories

3. OPTIMIZATION SUGGESTIONS:
   - More common color options for better pricing
   - Alternative model names if typos detected
   - Year corrections for accurate premium calculation

🇲🇾 MALAYSIAN INSURANCE MARKET CONTEXT:
- Focus on vehicles commonly insured in Malaysia
- Consider right-hand drive requirement
- Analyze against popular models: Myvi, Viva, Camry, Civic, Almera, X70, Saga
- Check against common Malaysian brands: Proton, Perodua, Toyota, Honda, Nissan

💡 SMART CORRECTION RECOMMENDATIONS:
- If typos detected, provide exact corrected spelling
- If invalid combination, suggest nearest valid alternative
- If color not found, recommend available colors for the model
- Explain reasoning for insurance application context

Provide comprehensive validation with focus on preventing insurance policy delays and ensuring accurate coverage.
"""
            print(validation_input)
            # Execute structured validation chain
            result = await self._execute_validation_chain_async(validation_input)
            
            # Search for images separately since we removed tools
            vehicle_images = await self._search_vehicle_images(vehicle_data, local_validation)
            
            # Structure the final response
            return self._structure_validation_result_from_pydantic(result, local_validation, vehicle_data, vehicle_images)
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Validation failed: {str(e)}",
                "confidence": 0,
                "vehicle_info": None
            }
    
    def _validate_against_csv(self, vehicle_data: Dict[str, Any]) -> Dict[str, bool]:
        """Validate against local CSV database"""
        try:
            year = vehicle_data.get('year')
            brand = vehicle_data.get('brand')
            model = vehicle_data.get('model')
            color = vehicle_data.get('color')
            
            # Get data for the year
            df = vehicle_data_loader.load_year_data(year)
            total_records = len(df)
            
            # Check brand (case-insensitive)
            brands = vehicle_data_loader.get_brands(year)
            brand_found = brand.lower() in [b.lower() for b in brands]
            
            # Find the correct case version of brand for model lookup
            brand_exact = brand
            if brand_found:
                for b in brands:
                    if b.lower() == brand.lower():
                        brand_exact = b
                        break
            
            # Check model (case-insensitive)
            models = vehicle_data_loader.get_models_for_brand(year, brand_exact)
            model_found = model.lower() in [m.lower() for m in models]
            
            # Find the correct case version of model for color lookup
            model_exact = model
            if model_found:
                for m in models:
                    if m.lower() == model.lower():
                        model_exact = m
                        break
            
            # Check color
            color_found = False
            vehicle_colors = []
            if brand_found and model_found:
                vehicle_colors = df[
                    (df['maker'] == brand_exact) & 
                    (df['model'] == model_exact)
                ]['colour'].dropna().unique().tolist()
                color_found = color.lower() in [c.lower() for c in vehicle_colors]
            
            return {
                "brand_found": brand_found,
                "model_found": model_found,
                "color_found": color_found,
                "total_records": total_records,
                "available_colors": vehicle_colors
            }
            
        except Exception as e:
            return {
                "brand_found": False,
                "model_found": False,
                "color_found": False,
                "total_records": 0,
                "available_colors": []
            }
    
    async def _execute_agent_async(self, input_text: str) -> Dict[str, Any]:
        """Execute the LangChain agent asynchronously with structured output"""
        try:
            result = self.agent_executor.invoke({"input": input_text})
            return result
        except Exception as e:
            return {"output": f"Agent execution failed: {str(e)}"}
    
    def _extract_images_from_search(self, agent_result: Dict[str, Any]) -> List[str]:
        """Extract vehicle images from Tavily search results"""
        images = []
        try:
            # Check if there are intermediate steps with search results
            intermediate_steps = agent_result.get("intermediate_steps", [])
            
            for step in intermediate_steps:
                if len(step) >= 2:
                    step_name, step_data = step[0], step[1]
                    
                    # Handle different formats of Tavily results
                    if isinstance(step_data, list):
                        # step_data is a list of search results
                        for result in step_data:
                            if isinstance(result, dict):
                                images.extend(self._extract_images_from_result(result))
                    elif isinstance(step_data, dict):
                        # step_data is a single search result
                        images.extend(self._extract_images_from_result(step_data))
            
            # Also check the main output for any image URLs
            output = agent_result.get("output", "")
            if isinstance(output, str):
                import re
                # Extract URLs that might be images
                image_urls = re.findall(r'https?://[^\s]+\.(?:jpg|jpeg|png|webp|gif)', output, re.IGNORECASE)
                images.extend(image_urls)
            
            # Clean and filter images
            clean_images = []
            for img in images:
                if isinstance(img, str) and img.startswith(('http://', 'https://')):
                    # Verify it's likely an image URL
                    if any(ext in img.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
                        clean_images.append(img)
            
            # Remove duplicates and limit to 4 images for better UI
            unique_images = list(dict.fromkeys(clean_images))
            return unique_images[:4]
            
        except Exception as e:
            print(f"Error extracting images: {e}")
            return []
    
    def _extract_images_from_result(self, result: Dict[str, Any]) -> List[str]:
        """Extract images from a single Tavily search result"""
        images = []
        
        # Check for direct image fields
        if "images" in result and isinstance(result["images"], list):
            images.extend(result["images"])
        
        if "image" in result:
            images.append(result["image"])
        
        # Check for image URLs in content
        content = result.get("content", "")
        if isinstance(content, str):
            import re
            image_urls = re.findall(r'https?://[^\s]+\.(?:jpg|jpeg|png|webp|gif)', content, re.IGNORECASE)
            images.extend(image_urls)
        
        # Check for image URLs in the URL field (sometimes Tavily returns image URLs directly)
        url = result.get("url", "")
        if isinstance(url, str) and any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
            images.append(url)
        
        return images
    
    def _structure_validation_result_from_pydantic(
        self, 
        pydantic_result: VehicleValidationResult, 
        local_validation: Dict[str, Any], 
        vehicle_data: Dict[str, Any],
        vehicle_images: List[str]
    ) -> Dict[str, Any]:
        """Structure the final validation result from enhanced Pydantic model"""
        
        try:
            # Convert Pydantic model to dict safely
            result_data = pydantic_result.model_dump()
            
            # Extract key validation information with safe access
            status = result_data.get("validation_status", "unable_to_verify")
            confidence = result_data.get("confidence_score", 50)
            typo_info = result_data.get("typo_detection", {})
            insurance_risk = result_data.get("insurance_risk", {})
            
            # Extract vehicle specifications from CSV if available
            vehicle_info = self._get_vehicle_specifications(vehicle_data, local_validation)
            
            # Enhanced recommendations with insurance focus
            recommendations = self._generate_insurance_recommendations(
                local_validation, 
                vehicle_data, 
                typo_info, 
                insurance_risk,
                result_data
            )
            
            # Generate insurance-focused validation message
            message = self._generate_insurance_validation_message(
                status, 
                confidence, 
                local_validation, 
                typo_info,
                insurance_risk
            )
            
            return {
                "status": status,
                "confidence": confidence,
                "message": message,
                "vehicle_info": vehicle_info,
                "vehicle_images": vehicle_images,
                "local_validation": local_validation,
                "agent_analysis": result_data.get("validation_notes", ""),
                "typo_detection": typo_info,
                "insurance_risk": insurance_risk,
                "recommendations": recommendations,
                "full_analysis": result_data  # Include full analysis for debugging
            }
            
        except Exception as e:
            print(f"Error structuring validation result: {e}")
            # Return a safe fallback structure
            return {
                "status": "error",
                "confidence": 0,
                "message": f"Failed to structure validation result: {str(e)}",
                "vehicle_info": self._get_vehicle_specifications(vehicle_data, local_validation),
                "vehicle_images": vehicle_images,
                "local_validation": local_validation,
                "agent_analysis": "Error occurred during analysis",
                "typo_detection": {},
                "insurance_risk": {},
                "recommendations": ["Unable to generate recommendations due to processing error"],
                "full_analysis": {}
            }

    def _generate_insurance_recommendations(
        self, 
        local_validation: Dict[str, Any], 
        vehicle_data: Dict[str, Any],
        typo_info: Dict[str, Any],
        insurance_risk: Dict[str, Any],
        result_data: Dict[str, Any]
    ) -> List[str]:
        """Generate insurance-focused recommendations"""
        recommendations = []
        
        # Typo corrections
        if typo_info.get("brand_has_typo"):
            corrected = typo_info.get("corrected_brand")
            if corrected:
                recommendations.append(f"TYPO DETECTED: Brand should be '{corrected}' instead of '{vehicle_data.get('brand')}'")
        
        if typo_info.get("model_has_typo"):
            corrected = typo_info.get("corrected_model")
            if corrected:
                recommendations.append(f"TYPO DETECTED: Model should be '{corrected}' instead of '{vehicle_data.get('model')}'")
                
        if typo_info.get("year_has_error"):
            corrected = typo_info.get("corrected_year")
            if corrected:
                recommendations.append(f"YEAR ERROR: Year should be '{corrected}' instead of '{vehicle_data.get('year')}'")
                
        if typo_info.get("color_has_typo"):
            corrected = typo_info.get("corrected_color")
            if corrected:
                recommendations.append(f"COLOR TYPO: Color should be '{corrected}' instead of '{vehicle_data.get('color')}'")
        
        # Insurance risk warnings
        risk_level = insurance_risk.get("policy_risk_level", "")
        if risk_level in ["high", "critical"]:
            recommendations.append(f"⚠️ INSURANCE RISK: {risk_level.upper()} risk level detected - policy approval may be delayed")
        
        pricing_impact = insurance_risk.get("pricing_impact", "")
        if pricing_impact in ["moderate", "significant"]:
            recommendations.append(f"💰 PRICING IMPACT: {pricing_impact.capitalize()} impact on insurance premium expected")
        
        # Coverage validity
        coverage = insurance_risk.get("coverage_validity", "")
        if coverage == "invalid":
            recommendations.append("❌ CRITICAL: This vehicle configuration may result in invalid insurance coverage")
        elif coverage == "questionable":
            recommendations.append("⚠️ WARNING: Insurance coverage validity is questionable - manual review recommended")
        
        # Fraud indicators
        fraud_indicators = insurance_risk.get("fraud_indicators", [])
        if fraud_indicators:
            recommendations.append(f"🚨 FRAUD ALERT: Potential indicators detected: {', '.join(fraud_indicators)}")
        
        # Standard validation recommendations
        if not local_validation["brand_found"]:
            recommendations.append("Please verify the vehicle brand spelling for accurate insurance quotes")
        
        if not local_validation["model_found"]:
            recommendations.append("Please check the vehicle model name to ensure correct policy coverage")
        
        if not local_validation["color_found"]:
            available_colors = local_validation.get("available_colors", [])
            if available_colors:
                color_list = ', '.join(available_colors[:3])
                recommendations.append(f"Color not found in database. Common options: {color_list}")
        
        # Insurance optimization suggestions
        color_validation = result_data.get("color_validation", {})
        color_category = color_validation.get("insurance_color_category", "")
        if color_category == "premium":
            recommendations.append("💎 This color may qualify for premium insurance rates")
        elif color_category == "rare":
            recommendations.append("⚠️ Rare color detected - may affect insurance valuation")
        
        vehicle_info = result_data.get("vehicle_info", {})
        if vehicle_info.get("common_insurance_model"):
            recommendations.append("✅ This is a commonly insured model in Malaysia - faster processing expected")
        
        return recommendations
    
    def _generate_insurance_validation_message(
        self, 
        status: str, 
        confidence: int, 
        local_validation: Dict[str, Any],
        typo_info: Dict[str, Any],
        insurance_risk: Dict[str, Any]
    ) -> str:
        """Generate insurance-focused validation message"""
        
        # Check for critical issues first
        if typo_info.get("brand_has_typo") or typo_info.get("model_has_typo"):
            return f"⚠️ TYPOS DETECTED: Vehicle information contains errors that could delay insurance approval (Confidence: {confidence}%)"
        
        risk_level = insurance_risk.get("policy_risk_level", "")
        if risk_level == "critical":
            return f"❌ CRITICAL RISK: Vehicle configuration may invalidate insurance policy (Confidence: {confidence}%)"
        elif risk_level == "high":
            return f"⚠️ HIGH RISK: Insurance approval may require manual review (Confidence: {confidence}%)"
        
        coverage = insurance_risk.get("coverage_validity", "")
        if coverage == "invalid":
            return f"❌ INVALID COVERAGE: This vehicle configuration cannot be insured (Confidence: {confidence}%)"
        
        # Standard validation messages with insurance context
        if status == "valid":
            if local_validation["color_found"]:
                return f"✅ READY FOR INSURANCE: Vehicle fully validated for Malaysian insurance application (Confidence: {confidence}%)"
            else:
                return f"✅ APPROVED: Vehicle validated, color confirmed via search - ready for insurance (Confidence: {confidence}%)"
        elif status == "warning":
            return f"⚠️ REVIEW NEEDED: Vehicle found but some details need verification for insurance accuracy (Confidence: {confidence}%)"
        elif status == "invalid":
            return f"❌ REJECTED: Vehicle information invalid for Malaysian insurance application (Confidence: {confidence}%)"
        else:
            return f"🔍 VERIFICATION NEEDED: Unable to validate vehicle for insurance purposes (Confidence: {confidence}%)"
    
    def _get_vehicle_specifications(
        self, 
        vehicle_data: Dict[str, Any], 
        local_validation: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Extract vehicle specifications from CSV data"""
        try:
            if not (local_validation["brand_found"] and local_validation["model_found"]):
                return None
            
            year = vehicle_data.get('year')
            brand = vehicle_data.get('brand')
            model = vehicle_data.get('model')
            
            df = vehicle_data_loader.load_year_data(year)
            vehicle_records = df[
                (df['maker'] == brand) & 
                (df['model'] == model)
            ]
            
            if vehicle_records.empty:
                return None
            
            # Get the most common specifications
            specs = {
                "brand": brand,
                "model": model,
                "year": year,
                "type": vehicle_records['type'].mode().iloc[0] if not vehicle_records['type'].empty else "Unknown",
                "fuel_type": vehicle_records['fuel'].mode().iloc[0] if not vehicle_records['fuel'].empty else "Unknown",
                "available_colors": sorted(vehicle_records['colour'].dropna().unique().tolist()),
                "common_states": sorted(vehicle_records['state'].value_counts().head(3).index.tolist()),
                "total_registrations": len(vehicle_records)
            }
            
            return specs
            
        except Exception as e:
            return None
    
    def _generate_validation_message(
        self, 
        status: str, 
        confidence: int, 
        local_validation: Dict[str, Any]
    ) -> str:
        """Generate human-readable validation message for Malaysian context"""
        if status == "valid":
            if local_validation["color_found"]:
                return f"Vehicle information fully validated for Malaysian registration (Confidence: {confidence}%)"
            else:
                return f"Vehicle model validated, color verification completed via search (Confidence: {confidence}%)"
        elif status == "warning":
            if not local_validation["color_found"]:
                return f"Vehicle model found in Malaysia, but {local_validation.get('vehicle_color', 'color')} may be rare or non-standard for this model (Confidence: {confidence}%)"
            else:
                return f"Vehicle information has minor discrepancies that need attention (Confidence: {confidence}%)"
        elif status == "invalid":
            return f"Vehicle information could not be validated for Malaysian market (Confidence: {confidence}%)"
        else:
            return f"Unable to verify vehicle information in Malaysian database (Confidence: {confidence}%)"
    
    def _generate_recommendations(
        self, 
        local_validation: Dict[str, Any], 
        vehicle_data: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        if not local_validation["brand_found"]:
            recommendations.append("Please verify the vehicle brand spelling")
        
        if not local_validation["model_found"]:
            recommendations.append("Please check the vehicle model name")
        
        if not local_validation["color_found"]:
            available_colors = local_validation.get("available_colors", [])
            if available_colors:
                color_list = ', '.join(available_colors[:5])
                recommendations.append(
                    f"Color '{vehicle_data.get('color')}' not found in local database. Common colors for this model: {color_list}"
                )
                if len(available_colors) > 5:
                    recommendations.append(f"Additional {len(available_colors) - 5} colors available for this model")
            else:
                recommendations.append("Please verify the color name for this vehicle model")
        
        # Add privacy notice
        recommendations.append("Search validation performed without including personal identifiers for privacy protection")
        
        return recommendations

    async def _execute_validation_chain_async(self, input_text: str) -> VehicleValidationResult:
        """Execute the structured validation chain with proper error handling"""
        try:
            # First attempt: use structured output
            result = self.validation_chain.invoke({"input": input_text})
            
            # Validate the result is a VehicleValidationResult instance
            if not isinstance(result, VehicleValidationResult):
                print(f"AI returned unexpected type: {type(result)}. Attempting to parse...")
                
                # Try to parse if it's a string or dict
                if isinstance(result, str):
                    try:
                        import json
                        parsed_json = json.loads(result)
                        result = VehicleValidationResult(**parsed_json)
                    except:
                        return self._create_fallback_validation_result("AI returned unparseable string response")
                elif isinstance(result, dict):
                    try:
                        result = VehicleValidationResult(**result)
                    except:
                        return self._create_fallback_validation_result("AI returned invalid dict structure")
                else:
                    return self._create_fallback_validation_result("AI returned unexpected response type")
            
            # Validate that all required nested fields are properly structured
            result = self._ensure_complete_validation_result(result)
            
            return result
            
        except Exception as e:
            print(f"Validation chain error: {str(e)}")
            # Return a complete default result if the chain fails
            return self._create_fallback_validation_result(str(e))
    
    def _ensure_complete_validation_result(self, result: VehicleValidationResult) -> VehicleValidationResult:
        """Ensure all required fields are present in the validation result"""
        try:
            # Check if typo_detection is missing or incomplete
            if not hasattr(result, 'typo_detection') or result.typo_detection is None:
                result.typo_detection = TypoDetection()
            elif not isinstance(result.typo_detection, TypoDetection):
                # Convert dict to TypoDetection if needed
                if isinstance(result.typo_detection, dict):
                    result.typo_detection = TypoDetection(**result.typo_detection)
                else:
                    result.typo_detection = TypoDetection()
            
            # Check if insurance_risk is missing or incomplete  
            if not hasattr(result, 'insurance_risk') or result.insurance_risk is None:
                result.insurance_risk = InsuranceRisk()
            elif not isinstance(result.insurance_risk, InsuranceRisk):
                # Convert dict to InsuranceRisk if needed
                if isinstance(result.insurance_risk, dict):
                    result.insurance_risk = InsuranceRisk(**result.insurance_risk)
                else:
                    result.insurance_risk = InsuranceRisk()
            
            # Check if color_validation is missing or incomplete
            if not hasattr(result, 'color_validation') or result.color_validation is None:
                result.color_validation = ColorValidation(
                    color_found_locally=False,
                    color_available_for_model=False
                )
            elif not isinstance(result.color_validation, ColorValidation):
                # Convert dict to ColorValidation if needed
                if isinstance(result.color_validation, dict):
                    result.color_validation = ColorValidation(**result.color_validation)
                else:
                    result.color_validation = ColorValidation(
                        color_found_locally=False,
                        color_available_for_model=False
                    )
            
            # Check if vehicle_info is missing or incomplete
            if not hasattr(result, 'vehicle_info') or result.vehicle_info is None:
                result.vehicle_info = VehicleInfo(
                    brand="Unknown",
                    model="Unknown", 
                    year="Unknown"
                )
            elif not isinstance(result.vehicle_info, VehicleInfo):
                # Convert dict to VehicleInfo if needed
                if isinstance(result.vehicle_info, dict):
                    result.vehicle_info = VehicleInfo(**result.vehicle_info)
                else:
                    result.vehicle_info = VehicleInfo(
                        brand="Unknown",
                        model="Unknown", 
                        year="Unknown"
                    )
            
            # Ensure basic fields have values
            if not result.validation_status:
                result.validation_status = "unable_to_verify"
            
            if not result.confidence_score:
                result.confidence_score = 50
                
            if not result.validation_notes:
                result.validation_notes = "Validation completed"
                
            if not result.recommendations:
                result.recommendations = ["No specific recommendations available"]
            
            return result
            
        except Exception as e:
            print(f"Error ensuring complete validation result: {e}")
            return self._create_fallback_validation_result(f"Failed to ensure complete result: {str(e)}")
    
    def _create_fallback_validation_result(self, error_message: str) -> VehicleValidationResult:
        """Create a complete fallback validation result"""
        return VehicleValidationResult(
            validation_status="unable_to_verify",
            confidence_score=0,
            typo_detection=TypoDetection(
                brand_has_typo=False,
                corrected_brand=None,
                model_has_typo=False,
                corrected_model=None,
                year_has_error=False,
                corrected_year=None,
                color_has_typo=False,
                corrected_color=None
            ),
            insurance_risk=InsuranceRisk(
                policy_risk_level="medium",
                pricing_impact="minor", 
                coverage_validity="questionable",
                fraud_indicators=[]
            ),
            color_validation=ColorValidation(
                color_found_locally=False,
                color_available_for_model=False,
                alternative_colors=[],
                color_verification_source="error",
                insurance_color_category="standard"
            ),
            vehicle_info=VehicleInfo(
                brand="",
                model="",
                year="",
                market_availability="unknown",
                assembly_type="unknown",
                insurance_category="family",
                common_insurance_model=False
            ),
            search_performed=False,
            image_urls=[],
            validation_notes=f"Validation failed: {error_message}",
            recommendations=[f"Validation error occurred: {error_message}"]
        )
    
    async def _search_vehicle_images(self, vehicle_data: Dict[str, Any], local_validation: Dict[str, Any]) -> List[str]:
        """Search for vehicle images using Tavily"""
        images = []
        
        if (local_validation["brand_found"] and local_validation["model_found"]):
            brand = vehicle_data['brand']
            model = vehicle_data['model'] 
            year = vehicle_data['year']
            color = vehicle_data['color']
            
            # Always prioritize color-specific searches for better image results
            image_search_queries = [
                f"{brand} {model} {year} {color} Malaysia car",
                f"{brand} {model} {color} Malaysia {year}",
                f"{brand} {model} {year} {color} Malaysia review",
                f"{brand} {model} {year} Malaysia {color}",
                f"{brand} {model} {year} Malaysia"
            ]
            
            for query in image_search_queries:
                try:
                    print(f"Searching for images with query: {query}")
                    image_results = self.tavily_tool.invoke({"query": query})
                    if image_results:
                        # Extract images from Tavily results
                        extracted_images = self._extract_images_from_search_result(image_results)
                        images.extend(extracted_images)
                        break  # Stop after first successful image search
                except Exception as e:
                    print(f"Image search failed for query '{query}': {e}")
                    continue
        
        return images[:4]  # Limit to 4 images
    
    def _extract_images_from_search_result(self, search_result) -> List[str]:
        """Extract image URLs from Tavily search result"""
        images = []
        try:
            if isinstance(search_result, list):
                for result in search_result:
                    if isinstance(result, dict):
                        if "images" in result and isinstance(result["images"], list):
                            images.extend(result["images"])
                        if "image" in result:
                            images.append(result["image"])
            elif isinstance(search_result, dict):
                if "images" in search_result and isinstance(search_result["images"], list):
                    images.extend(search_result["images"])
                if "image" in search_result:
                    images.append(search_result["image"])
        except Exception as e:
            print(f"Error extracting images: {e}")
        
        return images
    
    def _structure_validation_result_from_pydantic(
        self, 
        pydantic_result: VehicleValidationResult, 
        local_validation: Dict[str, Any], 
        vehicle_data: Dict[str, Any],
        vehicle_images: List[str]
    ) -> Dict[str, Any]:
        """Structure the final validation result from Pydantic model"""
        
        # Extract vehicle specifications from CSV if available
        vehicle_info = self._get_vehicle_specifications(vehicle_data, local_validation)
        
        return {
            "status": pydantic_result.validation_status,
            "confidence": pydantic_result.confidence_score,
            "message": self._generate_validation_message(pydantic_result.validation_status, pydantic_result.confidence_score, local_validation),
            "vehicle_info": vehicle_info,
            "vehicle_images": vehicle_images,
            "local_validation": local_validation,
            "agent_analysis": pydantic_result.validation_notes,
            "pydantic_data": {
                "validation_status": pydantic_result.validation_status,
                "confidence_score": pydantic_result.confidence_score,
                "color_validation": {
                    "color_found_locally": pydantic_result.color_validation.color_found_locally,
                    "color_available_for_model": pydantic_result.color_validation.color_available_for_model,
                    "alternative_colors": pydantic_result.color_validation.alternative_colors,
                    "color_verification_source": pydantic_result.color_validation.color_verification_source
                },
                "vehicle_info": {
                    "brand": pydantic_result.vehicle_info.brand,
                    "model": pydantic_result.vehicle_info.model,
                    "year": pydantic_result.vehicle_info.year,
                    "market_availability": pydantic_result.vehicle_info.market_availability,
                    "assembly_type": pydantic_result.vehicle_info.assembly_type
                },
                "search_performed": pydantic_result.search_performed,
                "image_urls": pydantic_result.image_urls,
                "validation_notes": pydantic_result.validation_notes,
                "recommendations": pydantic_result.recommendations
            },
            "recommendations": pydantic_result.recommendations
        }


# Global instance
vehicle_validation_agent = VehicleValidationAgent()

"""
General utility functions for the comparator module
"""

import re
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import hashlib
import json

logger = logging.getLogger(__name__)

def sanitize_text(text: str) -> str:
    """Sanitize text input for security"""
    if not text:
        return ""
    
    # Remove potentially harmful characters
    text = re.sub(r'[<>"\';()&+]', '', text)
    
    # Limit length
    text = text[:1000]
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def format_currency(amount: float, currency: str = "RM") -> str:
    """Format currency amount"""
    return f"{currency} {amount:,.2f}"

def calculate_vehicle_age(year: int) -> int:
    """Calculate vehicle age from year"""
    return max(0, datetime.now().year - year)

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate Malaysian phone number"""
    # Remove all non-digits
    digits = re.sub(r'\D', '', phone)
    
    # Malaysian mobile numbers: 01X-XXXXXXX (10-11 digits)
    # Landline: 0X-XXXXXXX (9-10 digits)
    if len(digits) >= 9 and len(digits) <= 11:
        return digits.startswith('0')
    
    return False

def generate_session_id() -> str:
    """Generate a unique session ID"""
    timestamp = datetime.now().isoformat()
    hash_input = f"{timestamp}_{id(object())}"
    return hashlib.md5(hash_input.encode()).hexdigest()[:16]

def parse_age_range(text: str) -> Dict[str, Optional[int]]:
    """Parse age range from text (e.g., '18-65 years')"""
    result = {"min_age": None, "max_age": None}
    
    # Pattern for age ranges
    patterns = [
        r'(\d+)\s*-\s*(\d+)\s*years?',
        r'(\d+)\s*to\s*(\d+)\s*years?',
        r'age\s*(\d+)\s*-\s*(\d+)',
        r'between\s*(\d+)\s*and\s*(\d+)\s*years?'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            result["min_age"] = int(match.group(1))
            result["max_age"] = int(match.group(2))
            break
    
    return result

def extract_numeric_value(text: str, keywords: List[str]) -> Optional[float]:
    """Extract numeric value associated with keywords"""
    text_lower = text.lower()
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in text_lower:
            # Look for numbers near the keyword
            pattern = fr'{re.escape(keyword_lower)}\s*:?\s*([0-9,]+(?:\.[0-9]{{1,2}})?)'
            match = re.search(pattern, text_lower)
            if match:
                try:
                    return float(match.group(1).replace(',', ''))
                except ValueError:
                    continue
    
    return None

def chunk_text(text: str, max_length: int = 8000, overlap: int = 200) -> List[str]:
    """Split text into chunks for processing"""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + max_length
        
        if end >= len(text):
            chunks.append(text[start:])
            break
        
        # Try to break at a sentence boundary
        chunk = text[start:end]
        last_period = chunk.rfind('.')
        last_newline = chunk.rfind('\n')
        
        break_point = max(last_period, last_newline)
        if break_point > start + (max_length // 2):  # Don't break too early
            end = start + break_point + 1
        
        chunks.append(text[start:end])
        start = max(start + 1, end - overlap)
    
    return chunks

def normalize_insurer_name(name: str) -> str:
    """Normalize insurer name for consistency"""
    name = name.strip()
    
    # Common normalizations
    normalizations = {
        'zurich malaysia': 'Zurich Malaysia',
        'zurich': 'Zurich Malaysia',
        'etiqa': 'Etiqa',
        'allianz': 'Allianz General Insurance Malaysia',
        'allianz malaysia': 'Allianz General Insurance Malaysia',
        'axa': 'AXA Affin General',
        'axa affin': 'AXA Affin General',
        'generali': 'Generali Malaysia',
        'liberty': 'Liberty Insurance',
        'amgeneral': 'AmGeneral',
        'am general': 'AmGeneral',
        'takaful ikhlas': 'Takaful Ikhlas',
        'ikhlas': 'Takaful Ikhlas',
        'sompo': 'Berjaya Sompo',
        'berjaya sompo': 'Berjaya Sompo',
        'tokio marine': 'Tokio Marine',
        'great eastern': 'Great Eastern General',
        'great eastern general': 'Great Eastern General'
    }
    
    name_lower = name.lower()
    return normalizations.get(name_lower, name)

def calculate_data_freshness_score(last_checked: Optional[datetime]) -> float:
    """Calculate data freshness score (0-100)"""
    if not last_checked:
        return 0.0
    
    days_old = (datetime.now() - last_checked).days
    
    if days_old == 0:
        return 100.0
    elif days_old <= 7:
        return 90.0
    elif days_old <= 30:
        return 75.0
    elif days_old <= 90:
        return 50.0
    else:
        return 25.0

def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Mask sensitive data for logging"""
    masked = data.copy()
    
    sensitive_fields = ['email', 'phone', 'ic_number', 'license_number']
    
    for field in sensitive_fields:
        if field in masked:
            value = str(masked[field])
            if len(value) > 4:
                masked[field] = value[:2] + '*' * (len(value) - 4) + value[-2:]
            else:
                masked[field] = '*' * len(value)
    
    return masked

def create_comparison_key(policy: Dict[str, Any]) -> str:
    """Create a unique key for policy comparison"""
    key_parts = [
        policy.get('insurer', '').lower(),
        policy.get('product_name', '').lower(),
        policy.get('coverage_type', '').lower()
    ]
    
    key = '_'.join(part.replace(' ', '_') for part in key_parts if part)
    return re.sub(r'[^a-z0-9_]', '', key)

def format_feature_list(features: List[str], max_items: int = 5) -> str:
    """Format feature list for display"""
    if not features:
        return "None specified"
    
    if len(features) <= max_items:
        return ", ".join(features)
    else:
        shown = features[:max_items]
        remaining = len(features) - max_items
        return f"{', '.join(shown)} and {remaining} more"

def validate_comparison_request(request_data: Dict[str, Any]) -> List[str]:
    """Validate comparison request data"""
    errors = []
    
    # Check required customer data
    if not request_data.get('customer'):
        errors.append("Customer information is required")
        return errors
    
    customer = request_data['customer']
    
    # Validate customer name
    if not customer.get('name'):
        errors.append("Customer name is required")
    
    # Validate vehicle data
    vehicle = customer.get('vehicle', {})
    if not vehicle.get('make'):
        errors.append("Vehicle make is required")
    if not vehicle.get('model'):
        errors.append("Vehicle model is required")
    if not vehicle.get('year'):
        errors.append("Vehicle year is required")
    elif not (1980 <= vehicle['year'] <= datetime.now().year + 1):
        errors.append("Vehicle year must be between 1980 and current year")
    
    # Validate driver data
    driver = customer.get('driver', {})
    if not driver.get('age'):
        errors.append("Driver age is required")
    elif not (18 <= driver['age'] <= 99):
        errors.append("Driver age must be between 18 and 99")
    
    if driver.get('license_years') is None:
        errors.append("License years is required")
    elif driver['license_years'] < 0:
        errors.append("License years cannot be negative")
    
    # Validate consent
    if not customer.get('consent_data_processing'):
        errors.append("Data processing consent is required")
    
    return errors

def log_performance_metrics(operation: str, duration: float, **kwargs):
    """Log performance metrics"""
    metrics = {
        "operation": operation,
        "duration_seconds": round(duration, 3),
        "timestamp": datetime.now().isoformat(),
        **kwargs
    }
    
    logger.info(f"Performance: {json.dumps(metrics)}")

class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_calls: int = 60, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def can_proceed(self, identifier: str = "default") -> bool:
        """Check if request can proceed"""
        now = datetime.now()
        
        # Clean old calls
        cutoff = now - timedelta(seconds=self.time_window)
        self.calls = [(call_time, call_id) for call_time, call_id in self.calls if call_time > cutoff]
        
        # Count calls for this identifier
        identifier_calls = [call for call in self.calls if call[1] == identifier]
        
        if len(identifier_calls) >= self.max_calls:
            return False
        
        # Record this call
        self.calls.append((now, identifier))
        return True

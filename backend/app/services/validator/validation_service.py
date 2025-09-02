"""
Validation service for Malaysian vehicle data formats
"""
import re
from typing import Dict, Optional, List


class MalaysianValidator:
    """Validator for Malaysian-specific formats"""
    
    def __init__(self):
        # Malaysian IC format: YYMMDD-PB-XXXX (12 digits total)
        self.ic_pattern = re.compile(r'^\d{6}-\d{2}-\d{4}$')
        
        # Malaysian car plate patterns
        self.plate_patterns = [
            # Standard format: ABC 1234
            re.compile(r'^[A-Z]{1,3}\s?\d{1,4}[A-Z]?$'),
            # Federal Territory: WA 1234 A
            re.compile(r'^W[A-Z]{1,2}\s?\d{1,4}\s?[A-Z]$'),
            # Sabah/Sarawak: SA 1234 A
            re.compile(r'^S[A-Z]{1,2}\s?\d{1,4}\s?[A-Z]?$'),
            # Special series: 1 ABC 1234
            re.compile(r'^\d{1}\s?[A-Z]{1,3}\s?\d{1,4}$'),
        ]
    
    def validate_ic(self, ic: str) -> Dict[str, any]:
        """Validate Malaysian IC number"""
        if not ic:
            return {'valid': False, 'error': 'IC number is required'}
        
        # Remove spaces and normalize
        ic_clean = ic.replace(' ', '').replace('-', '')
        
        # Check length
        if len(ic_clean) != 12:
            return {'valid': False, 'error': 'IC must be 12 digits'}
        
        # Check if all digits
        if not ic_clean.isdigit():
            return {'valid': False, 'error': 'IC must contain only digits'}
        
        # Format check (with dashes)
        ic_formatted = f"{ic_clean[:6]}-{ic_clean[6:8]}-{ic_clean[8:]}"
        if not self.ic_pattern.match(ic_formatted):
            return {'valid': False, 'error': 'Invalid IC format'}
        
        # Basic date validation
        year_part = ic_clean[:2]
        month_part = ic_clean[2:4]
        day_part = ic_clean[4:6]
        
        try:
            month = int(month_part)
            day = int(day_part)
            
            if month < 1 or month > 12:
                return {'valid': False, 'error': 'Invalid month in IC'}
            
            if day < 1 or day > 31:
                return {'valid': False, 'error': 'Invalid day in IC'}
                
        except ValueError:
            return {'valid': False, 'error': 'Invalid date in IC'}
        
        return {
            'valid': True, 
            'formatted': ic_formatted,
            'error': None
        }
    
    def validate_plate_number(self, plate: str) -> Dict[str, any]:
        """Validate Malaysian car plate number"""
        if not plate:
            return {'valid': False, 'error': 'Plate number is required'}
        
        # Clean and normalize
        plate_clean = plate.upper().strip()
        
        # Check against patterns
        for pattern in self.plate_patterns:
            if pattern.match(plate_clean):
                return {
                    'valid': True,
                    'formatted': plate_clean,
                    'error': None
                }
        
        return {
            'valid': False, 
            'error': 'Invalid Malaysian plate number format'
        }
    
    def validate_year(self, year: int, available_years: List[int]) -> Dict[str, any]:
        """Validate registration year"""
        if year not in available_years:
            return {
                'valid': False,
                'error': f'Data not available for year {year}'
            }
        
        return {'valid': True, 'error': None}


# Global instance
malaysian_validator = MalaysianValidator()

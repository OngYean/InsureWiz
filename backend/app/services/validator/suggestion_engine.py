"""
Fast fuzzy matching and suggestion engine for vehicle data
"""
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher
import re


class FuzzyMatcher:
    """Fast fuzzy string matching for suggestions"""
    
    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold
    
    def similarity(self, a: str, b: str) -> float:
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def find_matches(self, query: str, candidates: List[str], max_results: int = 5) -> List[Dict]:
        """Find fuzzy matches for a query string"""
        if not query or not candidates:
            return []
        
        query_lower = query.lower()
        matches = []
        
        for candidate in candidates:
            candidate_lower = candidate.lower()
            
            # Exact prefix match gets highest priority
            if candidate_lower.startswith(query_lower):
                score = 1.0
            # Contains match gets medium priority
            elif query_lower in candidate_lower:
                score = 0.8
            # Fuzzy match
            else:
                score = self.similarity(query, candidate)
            
            if score >= self.threshold:
                matches.append({
                    'text': candidate,
                    'score': score,
                    'completion': self._get_completion(query, candidate)
                })
        
        # Sort by score (descending) and return top results
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:max_results]
    
    def _get_completion(self, query: str, match: str) -> str:
        """Get the completion text for tab completion"""
        query_lower = query.lower()
        match_lower = match.lower()
        
        if match_lower.startswith(query_lower):
            return match[len(query):]
        return ""


class InsuranceTypoDetector:
    """Advanced typo detection for insurance applications"""
    
    def __init__(self):
        # Common insurance application typos
        self.brand_typos = {
            # Malaysian popular brands
            'toyata': 'Toyota',
            'toyoto': 'Toyota', 
            'toyata': 'Toyota',
            'hond': 'Honda',
            'honda': 'Honda',
            'nisssan': 'Nissan',
            'nisan': 'Nissan',
            'nissan': 'Nissan',
            'peroduaا': 'Perodua',
            'perodua': 'Perodua',
            'protan': 'Proton',
            'proton': 'Proton',
            'mazd': 'Mazda',
            'mazda': 'Mazda',
            'bmv': 'BMW',
            'bmw': 'BMW',
            'mercedes': 'Mercedes-Benz',
            'merc': 'Mercedes-Benz',
            'benz': 'Mercedes-Benz',
            'audi': 'Audi',
            'ford': 'Ford',
            'hyundai': 'Hyundai',
            'hyundae': 'Hyundai',
            'kia': 'Kia',
            'subaru': 'Subaru',
            'lexus': 'Lexus',
            'infinity': 'Infiniti',
            'infiniti': 'Infiniti'
        }
        
        self.model_typos = {
            # Popular Malaysian models
            'camry': 'Camry',
            'camray': 'Camry',
            'camri': 'Camry',
            'civic': 'Civic',
            'civick': 'Civic',
            'civi': 'Civic',
            'accord': 'Accord',
            'accor': 'Accord',
            'myvi': 'Myvi',
            'myvii': 'Myvi',
            'myvy': 'Myvi',
            'viva': 'Viva',
            'viv': 'Viva',
            'saga': 'Saga',
            'sag': 'Saga',
            'wira': 'Wira',
            'wir': 'Wira',
            'almera': 'Almera',
            'almira': 'Almera',
            'almer': 'Almera',
            'x70': 'X70',
            'x-70': 'X70',
            'x 70': 'X70',
            'bezza': 'Bezza',
            'bezz': 'Bezza',
            'ativa': 'Ativa',
            'ativ': 'Ativa',
            'corolla': 'Corolla',
            'coroll': 'Corolla',
            'corol': 'Corolla'
        }
        
        self.color_typos = {
            'whit': 'White',
            'white': 'White',
            'whte': 'White',
            'blac': 'Black',
            'black': 'Black',
            'blck': 'Black',
            'red': 'Red',
            'rad': 'Red',
            'blue': 'Blue',
            'blu': 'Blue',
            'gre': 'Grey',
            'gray': 'Grey',
            'grey': 'Grey',
            'silv': 'Silver',
            'silver': 'Silver',
            'silvr': 'Silver',
            'gold': 'Gold',
            'gol': 'Gold',
            'maroon': 'Maroon',
            'maron': 'Maroon',
            'green': 'Green',
            'grn': 'Green',
            'yellow': 'Yellow',
            'yelow': 'Yellow',
            'yelo': 'Yellow',
            'orange': 'Orange',
            'orng': 'Orange',
            'brown': 'Brown',
            'brn': 'Brown',
            'purple': 'Purple',
            'purpl': 'Purple',
            'pink': 'Pink',
            'pnk': 'Pink'
        }
    
    def detect_brand_typo(self, brand: str) -> tuple[bool, str]:
        """Detect and correct brand name typos"""
        brand_lower = brand.lower().strip()
        if brand_lower in self.brand_typos:
            return True, self.brand_typos[brand_lower]
        return False, brand
    
    def detect_model_typo(self, model: str) -> tuple[bool, str]:
        """Detect and correct model name typos"""
        model_lower = model.lower().strip()
        if model_lower in self.model_typos:
            return True, self.model_typos[model_lower]
        return False, model
    
    def detect_color_typo(self, color: str) -> tuple[bool, str]:
        """Detect and correct color name typos"""
        color_lower = color.lower().strip()
        if color_lower in self.color_typos:
            return True, self.color_typos[color_lower]
        return False, color
    
    def detect_year_error(self, year_input: str) -> tuple[bool, int]:
        """Detect and correct year input errors"""
        try:
            # Handle common year input errors
            year_str = str(year_input).strip()
            
            # Fix truncated years like "23" -> "2023", "22" -> "2022"
            if len(year_str) == 2 and year_str.isdigit():
                year_int = int(year_str)
                if year_int <= 30:  # Assume 2000s
                    corrected_year = 2000 + year_int
                else:  # Assume 1900s
                    corrected_year = 1900 + year_int
                return True, corrected_year
            
            # Fix incomplete years like "202" -> "2022" (assume most recent)
            elif len(year_str) == 3 and year_str.startswith("20"):
                # Assume current decade
                import datetime
                current_year = datetime.datetime.now().year
                corrected_year = int(year_str + str(current_year)[-1])
                return True, corrected_year
            
            # Normal 4-digit year
            elif len(year_str) == 4 and year_str.isdigit():
                year_int = int(year_str)
                # Check if reasonable range for vehicles
                if 1900 <= year_int <= 2030:
                    return False, year_int
                else:
                    # Try to correct impossible years
                    current_year = datetime.datetime.now().year
                    return True, current_year
            
            # Invalid format
            else:
                import datetime
                return True, datetime.datetime.now().year
                
        except:
            import datetime
            return True, datetime.datetime.now().year


class SuggestionEngine:
    """Enhanced suggestion engine for vehicle data with insurance focus"""
    
    def __init__(self):
        self.fuzzy_matcher = FuzzyMatcher(threshold=0.4)
        self.typo_detector = InsuranceTypoDetector()
    
    def get_brand_suggestions(self, query: str, brands: List[str]) -> Dict:
        """Get brand suggestions with typo detection"""
        # First check for common typos
        has_typo, corrected_brand = self.typo_detector.detect_brand_typo(query)
        
        if has_typo:
            # Return the corrected brand as primary suggestion
            return {
                'primary': corrected_brand,
                'suggestions': [corrected_brand] + [b for b in brands if b != corrected_brand][:4],
                'completion': corrected_brand[len(query):] if corrected_brand.lower().startswith(query.lower()) else ""
            }
        
        matches = self.fuzzy_matcher.find_matches(query, brands, max_results=5)
        
        if not matches:
            return {
                'primary': None,
                'suggestions': [],
                'completion': ''
            }
        
        primary = matches[0]
        return {
            'primary': primary['text'],
            'suggestions': [match['text'] for match in matches],
            'completion': primary['completion']
        }
    
    def get_model_suggestions(self, query: str, models: List[str]) -> Dict:
        """Get model suggestions with typo detection"""
        # First check for common typos
        has_typo, corrected_model = self.typo_detector.detect_model_typo(query)
        
        if has_typo:
            # Return the corrected model as primary suggestion
            return {
                'primary': corrected_model,
                'suggestions': [corrected_model] + [m for m in models if m != corrected_model][:4],
                'completion': corrected_model[len(query):] if corrected_model.lower().startswith(query.lower()) else ""
            }
        
        matches = self.fuzzy_matcher.find_matches(query, models, max_results=5)
        
        if not matches:
            return {
                'primary': None,
                'suggestions': [],
                'completion': ''
            }
        
        primary = matches[0]
        return {
            'primary': primary['text'],
            'suggestions': [match['text'] for match in matches],
            'completion': primary['completion']
        }
    
    def get_color_suggestions(self, query: str, colors: List[str]) -> Dict:
        """Get color suggestions with typo detection"""
        # First check for common typos
        has_typo, corrected_color = self.typo_detector.detect_color_typo(query)
        
        if has_typo:
            # Return the corrected color as primary suggestion
            return {
                'primary': corrected_color,
                'suggestions': [corrected_color] + [c for c in colors if c != corrected_color][:4],
                'completion': corrected_color[len(query):] if corrected_color.lower().startswith(query.lower()) else ""
            }
        
        matches = self.fuzzy_matcher.find_matches(query, colors, max_results=5)
        
        if not matches:
            return {
                'primary': None,
                'suggestions': [],
                'completion': ''
            }
        
        primary = matches[0]
        return {
            'primary': primary['text'],
            'suggestions': [match['text'] for match in matches],
            'completion': primary['completion']
        }


# Global instance
suggestion_engine = SuggestionEngine()

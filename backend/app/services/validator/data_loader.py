"""
Data loader for vehicle data with lazy loading by year
"""
import pandas as pd
import os
from typing import Dict, List, Optional
from pathlib import Path


class VehicleDataLoader:
    def __init__(self):
        self._cached_data: Dict[int, pd.DataFrame] = {}
        self._brand_cache: Dict[int, List[str]] = {}
        self._model_cache: Dict[int, Dict[str, List[str]]] = {}
        self._color_cache: Dict[int, Dict[str, Dict[str, List[str]]]] = {}  # year -> brand -> model -> colors
        self.data_dir = Path(__file__).parent / "data"
    
    def load_year_data(self, year: int) -> pd.DataFrame:
        """Load vehicle data for a specific year with caching"""
        if year in self._cached_data:
            return self._cached_data[year]
        
        csv_file = self.data_dir / f"cars_{year}.csv"
        if not csv_file.exists():
            raise FileNotFoundError(f"No data available for year {year}")
        
        # Load and cache the data
        df = pd.read_csv(csv_file)
        self._cached_data[year] = df
        
        # Pre-process and cache brands and models
        self._preprocess_year_data(year, df)
        
        return df
    
    def _preprocess_year_data(self, year: int, df: pd.DataFrame):
        """Pre-process data for fast lookups"""
        # Cache unique brands
        brands = sorted(df['maker'].dropna().unique().tolist())
        self._brand_cache[year] = brands
        
        # Cache models by brand
        models_by_brand = {}
        colors_by_brand = {}
        
        for brand in brands:
            brand_data = df[df['maker'] == brand]
            brand_models = sorted(brand_data['model'].dropna().unique().tolist())
            models_by_brand[brand] = brand_models
            
            # Cache colors by model for this brand
            colors_by_model = {}
            for model in brand_models:
                model_colors = brand_data[brand_data['model'] == model]['colour'].dropna().unique().tolist()
                colors_by_model[model] = sorted([color for color in model_colors if color])
            colors_by_brand[brand] = colors_by_model
        
        self._model_cache[year] = models_by_brand
        self._color_cache[year] = colors_by_brand
    
    def get_brands(self, year: int) -> List[str]:
        """Get all brands for a specific year"""
        if year not in self._brand_cache:
            self.load_year_data(year)
        return self._brand_cache[year]
    
    def get_models_for_brand(self, year: int, brand: str) -> List[str]:
        """Get all models for a specific brand and year"""
        if year not in self._model_cache:
            self.load_year_data(year)
        return self._model_cache[year].get(brand, [])
    
    def get_available_years(self) -> List[int]:
        """Get all available years"""
        years = []
        for file in self.data_dir.glob("cars_*.csv"):
            try:
                year = int(file.stem.split("_")[1])
                years.append(year)
            except (ValueError, IndexError):
                continue
        return sorted(years)
    
    def get_colors_for_model(self, year: int, brand: str, model: str) -> List[str]:
        """Get all colors for a specific brand, model and year"""
        if year not in self._color_cache:
            self.load_year_data(year)
        
        return self._color_cache[year].get(brand, {}).get(model, [])
    
    def clear_cache(self):
        """Clear all cached data"""
        self._cached_data.clear()
        self._brand_cache.clear()
        self._model_cache.clear()
        self._color_cache.clear()


# Global instance
vehicle_data_loader = VehicleDataLoader()

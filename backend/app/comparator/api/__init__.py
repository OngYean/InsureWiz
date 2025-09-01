"""
API package for Malaysian Motor Insurance Comparator
"""

from .main import router as comparator_router
from .crawl import router as crawl_router
from .compare import router as compare_router  
from .reports import router as reports_router

__all__ = [
    "comparator_router",
    "crawl_router", 
    "compare_router",
    "reports_router"
]

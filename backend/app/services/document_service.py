from typing import List, Dict, Any, Optional
from langchain.schema import Document
from app.services.vector_store import vector_store_service
from app.utils.logger import setup_logger
from app.utils.exceptions import VectorStoreException

logger = setup_logger("document_service")

class DocumentService:
    """Service for managing knowledge base documents and ingestion"""
    
    def __init__(self):
        self.vector_store = vector_store_service
    
    def add_insurance_knowledge(self, namespace: str = "insurance_knowledge") -> bool:
        """Add default insurance knowledge base to the vector store"""
        try:
            # Malaysian Insurance Knowledge Base
            insurance_documents = [
                Document(
                    page_content="""
                    Malaysian Motor Insurance Coverage Types:
                    
                    1. Third-Party Coverage:
                    - Covers damage to third-party vehicles and property
                    - Minimum legal requirement in Malaysia
                    - Does not cover your own vehicle damage
                    - Includes personal injury protection
                    
                    2. Third-Party, Fire & Theft:
                    - Includes third-party coverage
                    - Covers fire damage to your vehicle
                    - Covers theft of your vehicle
                    - Does not cover accident damage
                    
                    3. Comprehensive Coverage:
                    - Full coverage including own damage
                    - Covers third-party, fire, theft, and accident damage
                    - Includes windscreen coverage
                    - Covers natural disasters (flood, storm)
                    - Personal accident coverage for driver and passengers
                    
                    No Claim Discount (NCD):
                    - Starts at 0% for new policies
                    - Increases by 10% each claim-free year
                    - Maximum 55% after 5 years
                    - Resets to 0% after a claim
                    - Transferable between insurance companies
                    """,
                    metadata={
                        "source": "malaysian_insurance_guide",
                        "category": "motor_insurance",
                        "language": "english"
                    }
                ),
                Document(
                    page_content="""
                    Malaysian Home Insurance Coverage:
                    
                    1. Fire Insurance:
                    - Covers fire damage to building structure
                    - Includes lightning and explosion damage
                    - Covers smoke damage
                    - Building replacement cost coverage
                    
                    2. Contents Insurance:
                    - Covers personal belongings inside home
                    - Includes furniture, electronics, jewelry
                    - Theft and burglary protection
                    - Natural disaster coverage
                    
                    3. Liability Coverage:
                    - Third-party injury on your property
                    - Property damage to neighbors
                    - Legal defense costs
                    - Medical expenses coverage
                    
                    4. Natural Disaster Coverage:
                    - Flood damage protection
                    - Storm and wind damage
                    - Landslide coverage
                    - Earthquake protection (if applicable)
                    
                    Mortgage Protection:
                    - MRTA (Mortgage Reducing Term Assurance)
                    - MLTA (Mortgage Level Term Assurance)
                    - Covers outstanding loan balance
                    - Protects family from debt burden
                    """,
                    metadata={
                        "source": "malaysian_insurance_guide",
                        "category": "home_insurance",
                        "language": "english"
                    }
                ),
                Document(
                    page_content="""
                    Malaysian Health Insurance & Medical Takaful:
                    
                    1. Hospitalization Coverage:
                    - Room and board expenses
                    - Surgical procedures coverage
                    - Medical consultation fees
                    - Diagnostic tests and X-rays
                    - Medication and treatment costs
                    
                    2. Panel Hospital Benefits:
                    - Direct billing with network hospitals
                    - No upfront payment required
                    - Streamlined claims process
                    - Preferred provider discounts
                    
                    3. Critical Illness Protection:
                    - Cancer, heart attack, stroke coverage
                    - Lump sum payment upon diagnosis
                    - Early stage critical illness benefits
                    - Multiple critical illness coverage
                    
                    4. Deductibles and Co-pays:
                    - Annual deductible amounts
                    - Co-payment percentages
                    - Out-of-pocket maximum limits
                    - Pre-authorization requirements
                    
                    5. Pre-existing Conditions:
                    - Waiting period requirements
                    - Exclusions for known conditions
                    - Medical underwriting process
                    - Condition-specific coverage limits
                    """,
                    metadata={
                        "source": "malaysian_insurance_guide",
                        "category": "health_insurance",
                        "language": "english"
                    }
                ),
                Document(
                    page_content="""
                    Malaysian Life Insurance & Family Takaful:
                    
                    1. Term Life Insurance:
                    - Pure death benefit protection
                    - Fixed premium for policy term
                    - No cash value accumulation
                    - Cost-effective coverage option
                    - Renewable and convertible options
                    
                    2. Whole Life Insurance:
                    - Lifetime death benefit protection
                    - Cash value accumulation
                    - Premiums for life
                    - Investment component
                    - Policy loan availability
                    
                    3. Investment-Linked Products:
                    - Unit-linked insurance policies
                    - Investment fund selection
                    - Flexible premium payments
                    - Market-linked returns
                    - Risk and reward balance
                    
                    4. Riders and Additional Benefits:
                    - Accidental death benefit
                    - Critical illness rider
                    - Disability income rider
                    - Waiver of premium rider
                    - Child protection rider
                    
                    5. MRTA/MLTA for Property:
                    - Mortgage protection coverage
                    - Decreasing term coverage
                    - Level term coverage
                    - Loan balance protection
                    - Family financial security
                    """,
                    metadata={
                        "source": "malaysian_insurance_guide",
                        "category": "life_insurance",
                        "language": "english"
                    }
                ),
                Document(
                    page_content="""
                    Malaysian Claims Process Guidelines:
                    
                    1. Motor Insurance Claims:
                    - Report accident within 24 hours
                    - Obtain JPJ/PDRM police report
                    - Take photos of damage
                    - Contact insurance company immediately
                    - Submit claim within 30 days
                    
                    2. Required Documentation:
                    - Completed claim form
                    - Police report (for accidents)
                    - Medical certificates (for injury)
                    - Repair estimates
                    - Photos of damage
                    - Insurance policy document
                    
                    3. Claims Timeline:
                    - Initial report: Within 24 hours
                    - Documentation submission: Within 30 days
                    - Investigation period: 14-30 days
                    - Settlement: Within 60 days
                    - Appeal period: 30 days
                    
                    4. Dispute Resolution:
                    - Internal review process
                    - Bank Negara mediation
                    - Insurance Ombudsman
                    - Legal proceedings (if necessary)
                    - Consumer protection rights
                    
                    5. Common Claim Rejections:
                    - Late reporting
                    - Incomplete documentation
                    - Policy exclusions
                    - Fraudulent claims
                    - Non-disclosure of information
                    """,
                    metadata={
                        "source": "malaysian_insurance_guide",
                        "category": "claims_process",
                        "language": "english"
                    }
                ),
                Document(
                    page_content="""
                    Malaysian Insurance Regulations & Compliance:
                    
                    1. Bank Negara Malaysia (BNM) Guidelines:
                    - Insurance Act 1996
                    - Takaful Act 1984
                    - Financial Services Act 2013
                    - Islamic Financial Services Act 2013
                    - Regulatory compliance requirements
                    
                    2. Consumer Protection:
                    - Fair treatment principles
                    - Transparency requirements
                    - Complaint handling procedures
                    - Dispute resolution mechanisms
                    - Financial education initiatives
                    
                    3. Anti-Money Laundering (AML):
                    - Customer due diligence
                    - Suspicious transaction reporting
                    - Record keeping requirements
                    - Risk assessment procedures
                    - Staff training requirements
                    
                    4. Data Protection:
                    - Personal Data Protection Act 2010
                    - Customer information security
                    - Consent management
                    - Data retention policies
                    - Privacy protection measures
                    
                    5. Market Conduct:
                    - Sales practices standards
                    - Product disclosure requirements
                    - Claims handling standards
                    - Customer service requirements
                    - Professional conduct rules
                    """,
                    metadata={
                        "source": "malaysian_insurance_guide",
                        "category": "regulations",
                        "language": "english"
                    }
                )
            ]
            
            # Add documents to vector store
            success = self.vector_store.add_documents(
                documents=insurance_documents,
                namespace=namespace
            )
            
            if success:
                logger.info(f"Successfully added {len(insurance_documents)} insurance knowledge documents")
                return True
            else:
                logger.error("Failed to add insurance knowledge documents")
                return False
                
        except Exception as e:
            logger.error(f"Error adding insurance knowledge: {str(e)}")
            raise VectorStoreException(
                message="Failed to add insurance knowledge",
                details={"error": str(e)}
            )
    
    def add_custom_documents(self, documents: List[Document], namespace: str = "custom_knowledge") -> bool:
        """Add custom documents to the knowledge base"""
        try:
            success = self.vector_store.add_documents(
                documents=documents,
                namespace=namespace
            )
            
            if success:
                logger.info(f"Successfully added {len(documents)} custom documents")
                return True
            else:
                logger.error("Failed to add custom documents")
                return False
                
        except Exception as e:
            logger.error(f"Error adding custom documents: {str(e)}")
            raise VectorStoreException(
                message="Failed to add custom documents",
                details={"error": str(e)}
            )
    
    def search_knowledge(self, query: str, namespace: str = "insurance_knowledge") -> List[Document]:
        """Search the knowledge base for relevant information"""
        try:
            results = self.vector_store.similarity_search(
                query=query,
                namespace=namespace
            )
            
            logger.info(f"Found {len(results)} relevant documents for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
            raise VectorStoreException(
                message="Failed to search knowledge base",
                details={"error": str(e)}
            )
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            stats = self.vector_store.get_index_stats()
            return stats
            
        except Exception as e:
            logger.error(f"Error getting knowledge base stats: {str(e)}")
            raise VectorStoreException(
                message="Failed to get knowledge base statistics",
                details={"error": str(e)}
            )

# Global document service instance
document_service = DocumentService()


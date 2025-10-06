"""
RAG (Retrieval-Augmented Generation) engine for intelligent test generation
using financial domain knowledge - Simplified version for compatibility
"""
from typing import List, Dict, Any
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

class FinancialRAGEngine:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.knowledge_base = FINANCIAL_DOMAIN_DOCS
        
    def initialize_knowledge_base(self, financial_docs: List[str]):
        """Initialize the knowledge base with financial domain documents"""
        self.knowledge_base = financial_docs
        print(f"Initialized knowledge base with {len(financial_docs)} documents")
        
    def load_existing_knowledge_base(self):
        """Load existing knowledge base (simplified version)"""
        # In a real implementation, this would load from disk
        self.knowledge_base = FINANCIAL_DOMAIN_DOCS
        print("Loaded existing financial domain knowledge base")
    
    def generate_domain_aware_tests(self, api_spec: Dict, query_context: str) -> List[Dict]:
        """Generate tests using domain knowledge"""
        api_name = api_spec.get("name", "Unknown API")
        api_type = api_spec.get("type", "unknown")
        
        # Simple keyword-based matching for relevant knowledge
        relevant_docs = self._find_relevant_knowledge(query_context)
        
        # Generate test scenarios based on knowledge
        scenarios = []
        
        if "banking" in api_type.lower() or "transaction" in api_type.lower():
            scenarios.extend([
                {
                    "name": f"{api_name} AML Compliance Test",
                    "description": "Test anti-money laundering transaction monitoring",
                    "priority": "high",
                    "type": "compliance"
                },
                {
                    "name": f"{api_name} Transaction Integrity Test", 
                    "description": "Verify transaction authorization and limits",
                    "priority": "high",
                    "type": "functional"
                }
            ])
        
        if "payment" in api_type.lower() or "card" in api_type.lower():
            scenarios.extend([
                {
                    "name": f"{api_name} PCI DSS Compliance Test",
                    "description": "Test credit card data encryption and protection",
                    "priority": "high",
                    "type": "security"
                }
            ])
        
        # Add GDPR scenarios for all financial APIs
        scenarios.append({
            "name": f"{api_name} GDPR Data Privacy Test",
            "description": "Test personal data protection and user rights",
            "priority": "medium", 
            "type": "compliance"
        })
        
        return scenarios
    
    def get_compliance_requirements(self, transaction_type: str) -> Dict[str, Any]:
        """Get compliance requirements for specific transaction types"""
        requirements = {}
        
        if "credit_card" in transaction_type:
            requirements = {
                "type": transaction_type,
                "requirements": """
                PCI DSS Compliance Requirements:
                - Encrypt cardholder data in transit and at rest
                - Restrict access to cardholder data on need-to-know basis
                - Regularly test security systems and processes
                - Maintain vulnerability management program
                - Implement strong access control measures
                """
            }
        elif "bank" in transaction_type:
            requirements = {
                "type": transaction_type,
                "requirements": """
                Banking Compliance Requirements:
                - Implement proper transaction authorization
                - Monitor for suspicious activity patterns
                - Maintain audit trails for all transactions
                - Validate transaction amounts against limits
                - Ensure proper customer due diligence
                """
            }
        else:
            requirements = {
                "type": transaction_type,
                "requirements": "General financial compliance requirements apply"
            }
            
        return requirements
    
    def _find_relevant_knowledge(self, query: str) -> List[str]:
        """Find relevant knowledge documents based on query"""
        relevant = []
        query_lower = query.lower()
        
        for doc in self.knowledge_base:
            # Simple keyword matching
            if any(keyword in doc.lower() for keyword in 
                   ["pci", "aml", "gdpr", "transaction", "compliance", "security"]):
                if any(word in doc.lower() for word in query_lower.split()):
                    relevant.append(doc)
        
        return relevant if relevant else self.knowledge_base[:2]  # Return first 2 as fallback

# Financial domain knowledge for initialization
FINANCIAL_DOMAIN_DOCS = [
    """
    PCI DSS Compliance Testing Requirements:
    - All credit card data must be encrypted in transit and at rest
    - Access to cardholder data must be restricted and logged
    - Regular vulnerability scans must be performed
    - Strong access control measures must be implemented
    - Cardholder data must not be stored unnecessarily
    - Network security testing must be performed regularly
    """,
    """
    Anti-Money Laundering (AML) Testing:
    - Transaction monitoring for suspicious patterns
    - Customer due diligence verification
    - Sanctions screening for all parties
    - Reporting of suspicious activities within required timeframes
    - Know Your Customer (KYC) procedures must be tested
    - Large transaction reporting thresholds must be validated
    """,
    """
    Financial Transaction Integrity:
    - All transactions must have proper authorization
    - Transaction amounts must be validated against limits
    - Duplicate transaction detection and prevention
    - Audit trails must be maintained for all transactions
    - Transaction reversal procedures must be tested
    - Multi-factor authentication for high-value transactions
    """,
    """
    GDPR Data Privacy Requirements:
    - Personal financial data must be protected
    - Users must have right to data portability
    - Data retention policies must be enforced
    - Consent management for data processing
    - Right to be forgotten must be implemented
    - Data breach notification procedures must be tested
    """,
    """
    SOX Financial Reporting Compliance:
    - Internal controls over financial reporting must be tested
    - Accuracy of financial data must be validated
    - Segregation of duties must be enforced
    - Management assertions must be testable
    - IT general controls must be evaluated
    - Change management processes must be validated
    """,
    """
    Banking Security Best Practices:
    - Multi-factor authentication for all access
    - Session timeout and management
    - Secure communication protocols (TLS 1.3+)
    - Input validation and sanitization
    - Rate limiting and DDoS protection
    - Fraud detection and prevention systems
    """
]
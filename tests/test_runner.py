"""
AI-Enhanced Test Runner with intelligent test execution and analysis
"""
import pytest
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.ai_engine import AITestEngine, TestCase
from core.rag_engine import FinancialRAGEngine, FINANCIAL_DOMAIN_DOCS
from api_clients.financial_apis import AlphaVantageClient, MockBankingAPI, CurrencyExchangeClient

class AITestRunner:
    def __init__(self):
        self.ai_engine = AITestEngine()
        self.rag_engine = FinancialRAGEngine()
        self.test_results = []
        self.initialize_rag()
    
    def initialize_rag(self):
        """Initialize RAG knowledge base with financial domain knowledge"""
        try:
            self.rag_engine.load_existing_knowledge_base()
        except:
            # If no existing knowledge base, create new one
            self.rag_engine.initialize_knowledge_base(FINANCIAL_DOMAIN_DOCS)
    
    def run_ai_generated_tests(self, api_specs: List[Dict]) -> Dict[str, Any]:
        """Run AI-generated tests for given API specifications"""
        all_results = []
        
        for api_spec in api_specs:
            print(f"Generating tests for API: {api_spec.get('name', 'Unknown')}")
            
            # Generate test cases using AI
            test_cases = self.ai_engine.generate_test_cases(
                api_spec, 
                context="Financial application testing with focus on security and compliance"
            )
            
            # Get RAG-enhanced test scenarios
            rag_scenarios = self.rag_engine.generate_domain_aware_tests(
                api_spec, 
                "Banking and financial services"
            )
            
            # Execute tests
            for test_case in test_cases:
                result = self._execute_test_case(test_case, api_spec)
                all_results.append(result)
        
        # AI analysis of results
        analysis = self.ai_engine.analyze_test_results(all_results)
        
        return {
            "test_results": all_results,
            "ai_analysis": analysis,
            "total_tests": len(all_results),
            "passed_tests": len([r for r in all_results if r["status"] == "passed"]),
            "failed_tests": len([r for r in all_results if r["status"] == "failed"]),
            "timestamp": datetime.now().isoformat()
        }
    
    def _execute_test_case(self, test_case: TestCase, api_spec: Dict) -> Dict[str, Any]:
        """Execute a single test case"""
        try:
            # Determine which API client to use based on spec
            api_type = api_spec.get("type", "unknown")
            
            if api_type == "stock_api":
                client = AlphaVantageClient()
                result = self._test_stock_api(client, test_case)
            elif api_type == "banking_api":
                client = MockBankingAPI()
                result = self._test_banking_api(client, test_case)
            elif api_type == "currency_api":
                client = CurrencyExchangeClient()
                result = self._test_currency_api(client, test_case)
            else:
                result = {
                    "status": "skipped",
                    "message": f"Unknown API type: {api_type}"
                }
            
            return {
                "test_name": test_case.name,
                "test_type": test_case.test_type,
                "priority": test_case.priority,
                "api_endpoint": test_case.api_endpoint,
                "status": result["status"],
                "message": result.get("message", ""),
                "response_time": result.get("response_time", 0),
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                "test_name": test_case.name,
                "test_type": test_case.test_type,
                "priority": test_case.priority,
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _test_stock_api(self, client: AlphaVantageClient, test_case: TestCase) -> Dict:
        """Test stock API endpoints"""
        if "get_stock_price" in test_case.name.lower():
            symbol = test_case.test_data.get("symbol", "AAPL") if test_case.test_data else "AAPL"
            response = client.get_stock_price(symbol)
            
            return {
                "status": "passed" if response.success else "failed",
                "message": f"Stock price API response: {response.status_code}",
                "response_time": response.response_time
            }
        
        return {"status": "skipped", "message": "Test not implemented"}
    
    def _test_banking_api(self, client: MockBankingAPI, test_case: TestCase) -> Dict:
        """Test banking API endpoints"""
        if "balance" in test_case.name.lower():
            account_id = test_case.test_data.get("account_id", "ACC001") if test_case.test_data else "ACC001"
            response = client.get_account_balance(account_id)
            
            return {
                "status": "passed" if response.success else "failed",
                "message": f"Balance API response: {response.status_code}",
                "response_time": response.response_time
            }
        
        elif "transfer" in test_case.name.lower():
            from_acc = test_case.test_data.get("from_account", "ACC001") if test_case.test_data else "ACC001"
            to_acc = test_case.test_data.get("to_account", "ACC002") if test_case.test_data else "ACC002"
            amount = test_case.test_data.get("amount", 100.0) if test_case.test_data else 100.0
            
            response = client.transfer_funds(from_acc, to_acc, amount)
            
            return {
                "status": "passed" if response.success else "failed",
                "message": f"Transfer API response: {response.status_code}",
                "response_time": response.response_time
            }
        
        return {"status": "skipped", "message": "Test not implemented"}
    
    def _test_currency_api(self, client: CurrencyExchangeClient, test_case: TestCase) -> Dict:
        """Test currency exchange API"""
        if "exchange_rate" in test_case.name.lower():
            from_curr = test_case.test_data.get("from_currency", "USD") if test_case.test_data else "USD"
            to_curr = test_case.test_data.get("to_currency", "EUR") if test_case.test_data else "EUR"
            
            response = client.get_exchange_rate(from_curr, to_curr)
            
            return {
                "status": "passed" if response.success else "failed",
                "message": f"Exchange rate API response: {response.status_code}",
                "response_time": response.response_time
            }
        
        return {"status": "skipped", "message": "Test not implemented"}
    
    def generate_test_report(self, results: Dict[str, Any], output_file: str = "test_report.json"):
        """Generate comprehensive test report with AI insights"""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n=== AI-Enhanced Test Report ===")
        print(f"Total Tests: {results['total_tests']}")
        print(f"Passed: {results['passed_tests']}")
        print(f"Failed: {results['failed_tests']}")
        print(f"Success Rate: {(results['passed_tests']/results['total_tests']*100):.1f}%")
        
        if results.get('ai_analysis'):
            print(f"\n=== AI Analysis ===")
            print(results['ai_analysis'])
        
        print(f"\nDetailed report saved to: {output_file}")

# Sample API specifications for testing
SAMPLE_API_SPECS = [
    {
        "name": "Stock Market API",
        "type": "stock_api",
        "description": "API for retrieving stock market data",
        "endpoints": ["/quote", "/historical"],
        "authentication": "API Key"
    },
    {
        "name": "Banking API",
        "type": "banking_api", 
        "description": "Core banking operations API",
        "endpoints": ["/balance", "/transfer", "/history"],
        "authentication": "OAuth 2.0"
    },
    {
        "name": "Currency Exchange API",
        "type": "currency_api",
        "description": "Real-time currency exchange rates",
        "endpoints": ["/rates", "/convert"],
        "authentication": "API Key"
    }
]

if __name__ == "__main__":
    runner = AITestRunner()
    results = runner.run_ai_generated_tests(SAMPLE_API_SPECS)
    runner.generate_test_report(results)
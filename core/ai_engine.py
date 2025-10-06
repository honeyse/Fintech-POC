"""
AI Engine for intelligent test generation and analysis
"""
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    
from typing import List, Dict, Any, Optional
import json
import os
from dotenv import load_dotenv

load_dotenv()

class TestCase:
    def __init__(self, name: str, description: str, test_type: str, priority: str, 
                 steps: List[str], expected_result: str, api_endpoint: Optional[str] = None, 
                 test_data: Optional[Dict] = None):
        self.name = name
        self.description = description
        self.test_type = test_type
        self.priority = priority
        self.steps = steps
        self.expected_result = expected_result
        self.api_endpoint = api_endpoint
        self.test_data = test_data

class AITestEngine:
    def __init__(self, api_key: Optional[str] = None):
        if OPENAI_AVAILABLE:
            # For older OpenAI versions
            openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
        else:
            print("OpenAI not available. Using mock AI responses.")
    
    def generate_test_cases(self, api_spec: Dict, context: str = "") -> List[TestCase]:
        """Generate test cases using AI based on API specification"""
        if not OPENAI_AVAILABLE:
            return self._generate_mock_test_cases(api_spec)
        
        prompt = f"""
        As an expert financial software tester, generate comprehensive test cases for this API:
        
        API Specification: {json.dumps(api_spec, indent=2)}
        Context: {context}
        
        Generate test cases covering:
        1. Happy path scenarios
        2. Edge cases and boundary conditions
        3. Error handling
        4. Security vulnerabilities
        5. Performance considerations
        6. Financial compliance scenarios
        
        Return a JSON array of test cases.
        """
        
        try:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7
            )
            
            # Parse response and create test cases
            return self._parse_ai_response(response.choices[0].text, api_spec)
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_mock_test_cases(api_spec)
    
    def analyze_test_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Use AI to analyze test results and identify patterns"""
        if not OPENAI_AVAILABLE:
            return self._generate_mock_analysis(results)
        
        prompt = f"""
        Analyze these test results and provide insights:
        
        Results: {json.dumps(results, indent=2)}
        
        Provide analysis including:
        1. Overall test health
        2. Failure patterns
        3. Risk assessment
        4. Recommendations for improvement
        5. Potential issues to investigate
        """
        
        try:
            if OPENAI_AVAILABLE:
                response = openai.Completion.create(
                    engine="gpt-3.5-turbo-instruct",
                    prompt=prompt,
                    max_tokens=1000,
                    temperature=0.3
                )
                return {"analysis": response.choices[0].text.strip()}
            else:
                return self._generate_mock_analysis(results)
        except Exception as e:
            return {"error": f"Analysis failed: {e}"}
    
    def generate_test_data(self, data_type: str, count: int = 10) -> List[Dict]:
        """Generate realistic test data for financial scenarios"""
        if not OPENAI_AVAILABLE:
            return self._generate_mock_test_data(data_type, count)
        
        prompt = f"""
        Generate {count} realistic {data_type} test data samples for financial testing.
        
        For example, if data_type is "bank_transaction", generate realistic bank transactions.
        If it's "credit_card", generate realistic credit card data (use fake numbers).
        
        Return as JSON array with realistic but fake data suitable for testing.
        """
        
        try:
            if OPENAI_AVAILABLE:
                response = openai.Completion.create(
                    engine="gpt-3.5-turbo-instruct",
                    prompt=prompt,
                    max_tokens=1000,
                    temperature=0.8
                )
                return json.loads(response.choices[0].text.strip())
            else:
                return self._generate_mock_test_data(data_type, count)
        except Exception as e:
            print(f"Test data generation failed: {e}")
            return self._generate_mock_test_data(data_type, count)
    
    def _generate_mock_test_cases(self, api_spec: Dict) -> List[TestCase]:
        """Generate mock test cases when AI is not available"""
        api_name = api_spec.get("name", "Unknown API")
        api_type = api_spec.get("type", "unknown")
        
        mock_cases = [
            TestCase(
                name=f"{api_name} Happy Path Test",
                description=f"Test successful operation of {api_name}",
                test_type="functional",
                priority="high",
                steps=["Send valid request", "Verify response"],
                expected_result="Successful response with expected data",
                api_endpoint="/api/test",
                test_data={"test": "data"}
            ),
            TestCase(
                name=f"{api_name} Error Handling Test",
                description=f"Test error handling for {api_name}",
                test_type="functional",
                priority="medium",
                steps=["Send invalid request", "Verify error response"],
                expected_result="Proper error message returned",
                api_endpoint="/api/test",
                test_data={"invalid": "data"}
            ),
            TestCase(
                name=f"{api_name} Security Test",
                description=f"Test security of {api_name}",
                test_type="security",
                priority="high",
                steps=["Send malicious payload", "Verify rejection"],
                expected_result="Request blocked or sanitized",
                api_endpoint="/api/test",
                test_data={"malicious": "payload"}
            )
        ]
        
        return mock_cases
    
    def _generate_mock_analysis(self, results: List[Dict]) -> Dict[str, Any]:
        """Generate mock analysis when AI is not available"""
        total_tests = len(results)
        passed_tests = len([r for r in results if r.get("status") == "passed"])
        failed_tests = total_tests - passed_tests
        
        return {
            "overall_health": "Good" if passed_tests > failed_tests else "Needs Attention",
            "success_rate": f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%",
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "recommendations": [
                "Review failed tests for patterns",
                "Add more edge case testing",
                "Consider load testing for performance validation"
            ]
        }
    
    def _generate_mock_test_data(self, data_type: str, count: int) -> List[Dict]:
        """Generate mock test data when AI is not available"""
        from faker import Faker
        fake = Faker()
        
        if data_type == "bank_transaction":
            return [
                {
                    "transaction_id": fake.uuid4(),
                    "amount": round(fake.random.uniform(10.0, 10000.0), 2),
                    "from_account": fake.iban(),
                    "to_account": fake.iban(),
                    "description": fake.sentence(),
                    "timestamp": fake.date_time().isoformat()
                } for _ in range(count)
            ]
        elif data_type == "credit_card":
            return [
                {
                    "card_number": fake.credit_card_number(),
                    "expiry_date": fake.credit_card_expire(),
                    "cvv": fake.credit_card_security_code(),
                    "cardholder_name": fake.name(),
                    "credit_limit": round(fake.random.uniform(1000.0, 50000.0), 2)
                } for _ in range(count)
            ]
        else:
            return [{"id": i, "data": fake.sentence()} for i in range(count)]
    
    def _parse_ai_response(self, response_text: str, api_spec: Dict) -> List[TestCase]:
        """Parse AI response into TestCase objects"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                test_cases_data = json.loads(json_match.group(0))
                return [TestCase(**tc) for tc in test_cases_data if isinstance(tc, dict)]
        except:
            pass
        
        # Fallback to mock test cases
        return self._generate_mock_test_cases(api_spec)
"""
Financial API clients for testing various financial services
"""
import requests
from typing import Dict, Any, Optional, List
import json
import time
import random

class APIResponse:
    def __init__(self, status_code: int, data: Dict[Any, Any], headers: Dict[str, str], 
                 response_time: float, success: bool):
        self.status_code = status_code
        self.data = data
        self.headers = headers
        self.response_time = response_time
        self.success = success

class AlphaVantageClient:
    """Client for Alpha Vantage stock market API"""
    
    def __init__(self, api_key: str = "demo"):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = api_key
    
    def get_stock_price(self, symbol: str) -> APIResponse:
        """Get current stock price"""
        start_time = time.time()
        
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response_time = time.time() - start_time
            
            return APIResponse(
                status_code=response.status_code,
                data=response.json(),
                headers=dict(response.headers),
                response_time=response_time,
                success=response.status_code == 200
            )
        except Exception as e:
            return APIResponse(
                status_code=500,
                data={"error": str(e)},
                headers={},
                response_time=time.time() - start_time,
                success=False
            )

class MockBankingAPI:
    """Mock banking API for testing financial transactions"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"  # Mock server
        self.accounts = self._generate_mock_accounts()
        self.transactions = []
    
    def _generate_mock_accounts(self) -> List[Dict]:
        """Generate mock bank accounts"""
        return [
            {
                "account_id": "ACC001",
                "account_number": "1234567890",
                "account_type": "checking",
                "balance": 5000.00,
                "currency": "USD",
                "status": "active"
            },
            {
                "account_id": "ACC002", 
                "account_number": "2345678901",
                "account_type": "savings",
                "balance": 15000.00,
                "currency": "USD",
                "status": "active"
            }
        ]
    
    def get_account_balance(self, account_id: str) -> APIResponse:
        """Get account balance"""
        start_time = time.time()
        
        account = next((acc for acc in self.accounts if acc["account_id"] == account_id), None)
        
        if account:
            return APIResponse(
                status_code=200,
                data={
                    "account_id": account_id,
                    "balance": account["balance"],
                    "currency": account["currency"],
                    "timestamp": time.time()
                },
                headers={"Content-Type": "application/json"},
                response_time=time.time() - start_time,
                success=True
            )
        else:
            return APIResponse(
                status_code=404,
                data={"error": "Account not found"},
                headers={"Content-Type": "application/json"},
                response_time=time.time() - start_time,
                success=False
            )
    
    def transfer_funds(self, from_account: str, to_account: str, amount: float) -> APIResponse:
        """Transfer funds between accounts"""
        start_time = time.time()
        
        # Validate accounts exist
        from_acc = next((acc for acc in self.accounts if acc["account_id"] == from_account), None)
        to_acc = next((acc for acc in self.accounts if acc["account_id"] == to_account), None)
        
        if not from_acc:
            return APIResponse(
                status_code=404,
                data={"error": "Source account not found"},
                headers={"Content-Type": "application/json"},
                response_time=time.time() - start_time,
                success=False
            )
        
        if not to_acc:
            return APIResponse(
                status_code=404,
                data={"error": "Destination account not found"},
                headers={"Content-Type": "application/json"},
                response_time=time.time() - start_time,
                success=False
            )
        
        # Check sufficient balance
        if from_acc["balance"] < amount:
            return APIResponse(
                status_code=400,
                data={"error": "Insufficient funds"},
                headers={"Content-Type": "application/json"},
                response_time=time.time() - start_time,
                success=False
            )
        
        # Perform transfer
        from_acc["balance"] -= amount
        to_acc["balance"] += amount
        
        transaction_id = f"TXN{random.randint(100000, 999999)}"
        transaction = {
            "transaction_id": transaction_id,
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "status": "completed",
            "timestamp": time.time()
        }
        
        self.transactions.append(transaction)
        
        return APIResponse(
            status_code=200,
            data=transaction,
            headers={"Content-Type": "application/json"},
            response_time=time.time() - start_time,
            success=True
        )
    
    def get_transaction_history(self, account_id: str, limit: int = 10) -> APIResponse:
        """Get transaction history for account"""
        start_time = time.time()
        
        account_transactions = [
            txn for txn in self.transactions 
            if txn["from_account"] == account_id or txn["to_account"] == account_id
        ]
        
        return APIResponse(
            status_code=200,
            data={
                "account_id": account_id,
                "transactions": account_transactions[-limit:],
                "total_count": len(account_transactions)
            },
            headers={"Content-Type": "application/json"},
            response_time=time.time() - start_time,
            success=True
        )

class CurrencyExchangeClient:
    """Client for currency exchange rate API"""
    
    def __init__(self):
        self.base_url = "https://api.fixer.io/latest"
        # Using mock data since fixer.io requires API key
        self.mock_rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GBP": 0.73,
            "JPY": 110.0,
            "CAD": 1.25
        }
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> APIResponse:
        """Get exchange rate between currencies"""
        start_time = time.time()
        
        if from_currency in self.mock_rates and to_currency in self.mock_rates:
            # Calculate rate via USD
            from_rate = self.mock_rates[from_currency]
            to_rate = self.mock_rates[to_currency]
            exchange_rate = to_rate / from_rate
            
            return APIResponse(
                status_code=200,
                data={
                    "from": from_currency,
                    "to": to_currency,
                    "rate": round(exchange_rate, 4),
                    "timestamp": time.time()
                },
                headers={"Content-Type": "application/json"},
                response_time=time.time() - start_time,
                success=True
            )
        else:
            return APIResponse(
                status_code=400,
                data={"error": "Unsupported currency"},
                headers={"Content-Type": "application/json"},
                response_time=time.time() - start_time,
                success=False
            )
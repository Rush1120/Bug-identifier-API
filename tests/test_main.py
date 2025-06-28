import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

class MockGeminiResponse:
    def __init__(self, text: str):
        self.text = text

@patch('main.model')
def test_find_bug_success(mock_model):
    """Test successful bug detection."""
    # Mock the Gemini response
    mock_response = MockGeminiResponse(
        "Bug Type: Logical Bug\n"
        "Description: The function is meant to check if a number is even, but it incorrectly returns True for odd numbers.\n"
        "Suggestion: Use `n % 2 == 0` instead."
    )
    mock_model.generate_content.return_value = mock_response
    
    # Test data
    test_data = {
        "language": "python",
        "code": "def is_even(n): return n % 2 == 1"
    }
    
    response = client.post("/find-bug", json=test_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["bug_type"] == "Logical Bug"
    assert "even" in data["description"].lower()
    assert "n % 2 == 0" in data["suggestion"]

def test_find_bug_invalid_language():
    """Test error handling for invalid language."""
    test_data = {
        "language": "invalid_lang",
        "code": "print('hello')"
    }
    
    response = client.post("/find-bug", json=test_data)
    assert response.status_code == 422

def test_find_bug_empty_code():
    """Test error handling for empty code."""
    test_data = {
        "language": "python",
        "code": ""
    }
    
    response = client.post("/find-bug", json=test_data)
    assert response.status_code == 422

def test_find_bug_too_long_code():
    """Test error handling for code that's too long."""
    long_code = "\n".join([f"print({i})" for i in range(31)])
    test_data = {
        "language": "python",
        "code": long_code
    }
    
    response = client.post("/find-bug", json=test_data)
    assert response.status_code == 422

def test_sample_cases():
    """Test the sample cases endpoint."""
    response = client.get("/sample-cases")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 5
    assert all("language" in case for case in data)
    assert all("code" in case for case in data)
    assert all("bug_type" in case for case in data)

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "AI-Powered Bug Identifier API"
    assert data["version"] == "1.0.0"

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"

@patch('main.model')
def test_find_bug_with_mode_parameter(mock_model):
    """Test bug detection with different tone modes."""
    mock_response = MockGeminiResponse(
        "Bug Type: Runtime Error\n"
        "Description: Division by zero will cause an error.\n"
        "Suggestion: Add a check for zero."
    )
    mock_model.generate_content.return_value = mock_response
    
    test_data = {
        "language": "python",
        "code": "def divide(a, b): return a / b"
    }
    
    # Test with casual mode
    response = client.post("/find-bug?mode=casual", json=test_data)
    assert response.status_code == 200
    
    # Test with educational mode
    response = client.post("/find-bug?mode=educational", json=test_data)
    assert response.status_code == 200

@patch('main.model')
def test_find_bug_ai_error_handling(mock_model):
    """Test error handling when AI model fails."""
    mock_model.generate_content.side_effect = Exception("AI model error")
    
    test_data = {
        "language": "python",
        "code": "print('hello')"
    }
    
    response = client.post("/find-bug", json=test_data)
    assert response.status_code == 500
    assert "Error analyzing code" in response.json()["detail"] 
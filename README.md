# AI-Powered Bug Identifier 

An intelligent API that analyzes code snippets to identify potential bugs using Google's Gemini AI. Perfect for code reviews, learning, and catching common programming mistakes.

## Features 

- **Smart Bug Detection**: Identifies logic, runtime, off-by-one, edge-case, and syntax errors
- **Multi-language Support**: Python, JavaScript, Java, C, C++, C#, Go, Rust, PHP, Ruby
- **Flexible Tone Options**: Developer-friendly, casual, or educational explanations
- **Input Validation**: Ensures code snippets are ≤30 lines and properly formatted
- **Rate Limiting**: Built-in protection against abuse
- **Sample Cases**: Pre-built examples for testing and learning
- **Comprehensive Testing**: Unit tests with mocked AI responses

## Quick Start 

### 1. Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-bug-finder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints 

### POST /find-bug

Analyze a code snippet for potential bugs.

**Request:**
```json
{
  "language": "python",
  "code": "def is_even(n): return n % 2 == 1"
}
```

**Response:**
```json
{
  "bug_type": "Logical Bug",
  "description": "The function is meant to check if a number is even, but it incorrectly returns True for odd numbers.",
  "suggestion": "Use `n % 2 == 0` instead."
}
```

**Query Parameters:**
- `mode`: Tone of response (`developer-friendly`, `casual`, `educational`)

### GET /sample-cases

Get pre-built examples of buggy code with explanations.

### GET /

API information and available endpoints.

### GET /health

Health check endpoint.

## Test Cases Included 

The API includes these classic bug examples:

1. **Logic Error**: `def is_even(n): return n % 2 == 1`
2. **Runtime Error**: `def divide(a, b): return a / b`
3. **Off-by-One**: `for i in range(1, len(arr)): process(arr[i])`
4. **Syntax Error**: `if x = 5: print('x is 5')`
5. **Edge Case**: `if not arr: process(arr)`

## Running Tests 

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py
```

## Project Structure 

```
ai-bug-finder/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── gemini_client.py  # Gemini AI integration
│   └── middleware/
│       ├── __init__.py
│       └── rate_limiter.py   # Rate limiting
└── tests/
    ├── __init__.py
    └── test_main.py          # Unit tests
```

## API Documentation 

Once the server is running, visit:
- **Interactive Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Usage Examples 

### Python Example
```python
import requests


response = requests.post("http://localhost:8000/find-bug", json={
    "language": "python",
    "code": "def divide(a, b): return a / b"
})

print(response.json())
```

### JavaScript Example
```javascript

const response = await fetch("http://localhost:8000/find-bug", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        language: "javascript",
        code: "function getElement(arr, index) { return arr[index]; }"
    })
});

const result = await response.json();
console.log(result);
```

### cURL Example
```bash
curl -X POST "http://localhost:8000/find-bug" \
     -H "Content-Type: application/json" \
     -d '{
       "language": "python",
       "code": "for i in range(1, len(arr)):\n    print(arr[i])"
     }'
```

## Error Handling 

The API gracefully handles:
- **Invalid languages**: Returns 422 with supported languages list
- **Empty code**: Returns 422 with validation error
- **Code too long**: Returns 422 if >30 lines
- **AI model errors**: Returns 500 with error details
- **Rate limiting**: Returns 429 when limit exceeded

## Deployment 

### Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Deploy: `vercel`





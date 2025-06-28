from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from app.core.gemini_client import get_model
import re

# initializing fastapi app
app = FastAPI(
    title="AI-Powered Bug Identifier",
    description="An API that identifies bugs in code snippets using AI",
    version="1.0.0"
)

# Get the configured model
model = get_model()

# Requesting the model
class CodeSnippet(BaseModel):
    language: str = Field(..., description="Programming language of the code snippet")
    code: str = Field(..., description="Code snippet to analyze (max 30 lines)")
    
    @field_validator('code')
    @classmethod
    def validate_code_length(cls, v):
        lines = v.strip().split('\n')
        if len(lines) > 30:
            raise ValueError("Code snippet must be 30 lines or less")
        if not v.strip():
            raise ValueError("Code snippet cannot be empty")
        return v
    
    @field_validator('language')
    @classmethod
    def validate_language(cls, v):
        supported_languages = ['python', 'javascript', 'java', 'c', 'cpp', 'csharp', 'go', 'rust', 'php', 'ruby']
        if v.lower() not in supported_languages:
            raise ValueError(f"Unsupported language. Supported: {', '.join(supported_languages)}")
        return v.lower()

# Response of the model
class BugReport(BaseModel):
    bug_type: str = Field(..., description="Type of bug identified")
    description: str = Field(..., description="Detailed description of the bug")
    suggestion: str = Field(..., description="Suggestion to fix the bug")

class SampleCase(BaseModel):
    language: str
    code: str
    bug_type: str
    description: str
    suggestion: str

# Sample buggy code cases in here
SAMPLE_CASES = [
    SampleCase(
        language="python",
        code="def is_even(n):\n    return n % 2 == 1",
        bug_type="Logical Bug",
        description="The function is meant to check if a number is even, but it incorrectly returns True for odd numbers.",
        suggestion="Use `n % 2 == 0` instead."
    ),
    SampleCase(
        language="python",
        code="def divide(a, b):\n    return a / b",
        bug_type="Runtime Error",
        description="Division by zero will cause a runtime error when b is 0.",
        suggestion="Add a check: `if b == 0: raise ValueError('Division by zero')`"
    ),
    SampleCase(
        language="python",
        code="for i in range(1, len(arr)):\n    process(arr[i])",
        bug_type="Off-by-One Error",
        description="The loop starts from index 1, skipping the first element at index 0.",
        suggestion="Use `range(len(arr))` to process all elements."
    ),
    SampleCase(
        language="python",
        code="if x = 5:\n    print('x is 5')",
        bug_type="Syntax Error",
        description="Using assignment operator (=) instead of comparison operator (==).",
        suggestion="Use `if x == 5:` for comparison."
    ),
    SampleCase(
        language="python",
        code="if not arr:\n    process(arr)",
        bug_type="Logic Error",
        description="Processing an empty array when the condition checks for emptiness.",
        suggestion="Move `process(arr)` outside the if block or add an else clause."
    )
]

def analyze_code_with_tone(code: str, language: str, tone: str = "developer-friendly") -> BugReport:
    """Analyze code with specified tone."""
    
    tone_prompts = {
        "developer-friendly": "Analyze the following {language} code for potential bugs. Provide a professional, technical explanation.",
        "casual": "Look at this {language} code and tell me what's wrong with it in a casual, friendly way.",
        "educational": "Explain what's wrong with this {language} code as if teaching a beginner programmer."
    }
    
    base_prompt = tone_prompts.get(tone, tone_prompts["developer-friendly"])
    
    prompt = f"""{base_prompt}

Analyze the following {language} code for any potential bugs (logic, runtime, off-by-one, edge-case, syntax). 
Return your response in this exact format (no headings, no extra explanation): 
Bug Type: <bug_type>
Description: <description>
Suggestion: <fix_or_improvement>

Code:
{code}
"""
    
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().splitlines()
        
        if len(lines) < 3:
            raise ValueError("Invalid response format from AI model")
            
        bug_type = lines[0].replace("Bug Type:", "").strip()
        description = lines[1].replace("Description:", "").strip()
        suggestion = lines[2].replace("Suggestion:", "").strip()
        
        return BugReport(
            bug_type=bug_type,
            description=description,
            suggestion=suggestion
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing code: {str(e)}")

@app.post("/find-bug", response_model=BugReport)
async def find_bug(
    snippet: CodeSnippet,
    mode: Optional[str] = Query("developer-friendly", description="Tone mode: developer-friendly, casual, or educational")
):
    """
    Analyze a code snippet for potential bugs.
    
    - **language**: Programming language of the code
    - **code**: Code snippet to analyze (max 30 lines)
    - **mode**: Tone of the response (developer-friendly, casual, educational)
    """
    try:
        return analyze_code_with_tone(snippet.code, snippet.language, mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/sample-cases", response_model=List[SampleCase])
async def get_sample_cases():
    """
    Get sample buggy code cases with explanations.
    Useful for testing and understanding the API.
    """
    return SAMPLE_CASES

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI-Powered Bug Identifier API",
        "version": "1.0.0",
        "endpoints": {
            "POST /find-bug": "Analyze code snippets for bugs",
            "GET /sample-cases": "Get sample buggy code cases",
            "GET /docs": "API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "bug-identifier"}

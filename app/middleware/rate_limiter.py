from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from typing import Dict, Tuple
import time

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, client_ip: str) -> bool:
        """Check if the client is allowed to make a request."""
        now = datetime.now()
        
        # Clean old requests (older than 1 minute)
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if now - req_time < timedelta(minutes=1)
            ]
        
        # Check if client has exceeded the limit
        if client_ip in self.requests and len(self.requests[client_ip]) >= self.requests_per_minute:
            return False
        
        # Add current request
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip].append(now)
        
        return True

# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=60)

async def rate_limit_middleware(request: Request, call_next):
    """Middleware to apply rate limiting."""
    client_ip = request.client.host
    
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )
    
    response = await call_next(request)
    return response 
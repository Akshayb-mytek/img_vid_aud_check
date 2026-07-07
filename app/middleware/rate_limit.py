import time
from collections import defaultdict
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit=10, window=60):
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.requests = defaultdict(list)

    def get_client_ip(self, request: Request):
        forwarded = request.headers.get("x-forwarded-for")

        if forwarded:
            # first IP = original client
            return forwarded.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")

        if real_ip:
            return real_ip

        return request.client.host

    async def dispatch(self, request: Request, call_next):
        ip = self.get_client_ip(request)

        now = time.time()

        # cleanup old timestamps
        self.requests[ip] = [
            t for t in self.requests[ip]
            if now - t < self.window
        ]

        if len(self.requests[ip]) >= self.limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )

        self.requests[ip].append(now)

        return await call_next(request)
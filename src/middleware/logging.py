# src/middleware/logging.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger("api")

SENSITIVE_PATHS = ("/auth/token", "/login", "/password")

class SafeLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()

        response = await call_next(request)

        duration = (time.time() - start) * 1000

        path = request.url.path

        if any(path.startswith(p) for p in SENSITIVE_PATHS):
            logger.info(
                "%s %s -> %s (%.2f ms)",
                request.method,
                path,
                response.status_code,
                duration,
            )
        else:
            logger.info(
                "%s %s -> %s (%.2f ms)",
                request.method,
                path,
                response.status_code,
                duration,
            )

        return response

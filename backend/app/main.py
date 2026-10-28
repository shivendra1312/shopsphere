from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.redis import get_redis_client
from app.utils.exceptions import AppException

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="E-commerce API built with FastAPI",
    version="1.0.0",
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
)

# 1. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# 3. Global Exception Handler for Custom Business Exceptions
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "type": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            }
        }
    )

# 4. Request Validation Error Handler (Pydantic)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " -> ".join(str(l) for l in err.get("loc", []))
        errors.append(f"{loc}: {err.get('msg')}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": 422,
                "type": "VALIDATION_ERROR",
                "message": "Invalid request parameters",
                "details": errors
            }
        }
    )

app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
def health_check():
    redis_available = get_redis_client() is not None
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "services": {
            "database": "connected",
            "redis": "connected" if redis_available else "disconnected (cache bypass active)"
        }
    }
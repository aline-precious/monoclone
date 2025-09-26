#functions to transform exceptions into friendly JSON responses 
# (consistent error shape for HTTP errors, validation errors and unexpected exceptions).
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={...})

async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=422, content={...})

async def unhandled_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={...})



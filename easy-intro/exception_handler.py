from litestar import MediaType, Request, Response
from litestar.exceptions import HTTPException
from openai import RateLimitError


def app_exception_handler(request: Request, exc: HTTPException) -> Response:
    return Response(
        content={
            "error": "server error",
            "path": request.url.path,
            "detail": exc.detail,
            "status_code": exc.status_code,
        },
        status_code=500,
    )


def router_handler_exception_handler(request: Request, exc: RateLimitError) -> Response:
    return Response(
        content={
            "error": "OpenAI error",
            "path": request.url.path,
            "details": exc.message,
        },
        status_code=exc.status_code,
    )

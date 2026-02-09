from starlette.middleware.base import BaseHTTPMiddleware
from time import perf_counter

class ResponseTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = perf_counter()
        response = await call_next(request)
        process_time = perf_counter() - start_time
        response.headers["x-response-time-seconds"] = f"{process_time:.4f}"
        # print(f"⏱️  {request.method} {request.url.path} - {process_time:.6f}s")
        return response
from fastapi import Request, FastAPI
from pyinstrument import Profiler
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from ..config import get_settings

settings = get_settings()


def register_performance_middleware(app: FastAPI):

    if settings.profiling == False:
        return

    @app.middleware("http")
    async def performance_profiling(
        request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        profiler = Profiler(interval=0.001, async_mode="enabled")
        profiler.start()
        response = await call_next(request)
        profiler.stop()
        # Write result to html file
        profiler.write_html("profile.html")
        return response

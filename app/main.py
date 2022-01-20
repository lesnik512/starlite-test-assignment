from starlite import Starlite
from starlite.exceptions import ValidationException

from app.apps.metrics.views import router
from app.config import settings
from app.db.middleware import SQLAlchemySessionMiddleware
from app.exceptions import request_validation_exception_handler


app = Starlite(
    route_handlers=[router],
    debug=settings.DEBUG,
    middleware=[] if settings.IS_TESTING else [SQLAlchemySessionMiddleware],
    exception_handlers={ValidationException: request_validation_exception_handler},  # type: ignore
)

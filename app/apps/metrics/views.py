import datetime
from typing import Any, Dict, List, Optional

from pydantic import parse_obj_as
from starlite import Parameter, Router
from starlite.handlers import get

from app.apps.metrics import models, schemas


@get(path="/metrics")
async def filter_metrics(
    sort_field: schemas.SortField = schemas.SortField.date,
    sort_direction: schemas.SortDirection = schemas.SortDirection.asc,
    channel: Optional[schemas.Channel] = Parameter(default=None),
    country: Optional[schemas.Country] = Parameter(default=None),
    os: Optional[schemas.OS] = Parameter(default=None),
    from_date: Optional[datetime.date] = Parameter(default=None),
    to_date: Optional[datetime.date] = Parameter(default=None),
    group_by: Optional[str] = Parameter(default=None),
) -> schemas.Metrics:
    filters: Dict[str, Any] = {}
    if channel:
        filters["channel"] = channel.value
    if country:
        filters["country"] = country.value
    if os:
        filters["os"] = os.value
    if from_date:
        filters["date__ge"] = from_date
    if to_date:
        filters["date__le"] = to_date

    grouping = []
    if group_by:
        for field in parse_obj_as(List[schemas.GroupField], group_by.split(",")):
            grouping.append(field.value)

    objects = await models.Metric.filter(filters, {sort_field.value: sort_direction.value}, grouping)
    return schemas.Metrics.parse_obj({"items": objects})


router = Router(path="/api", route_handlers=[filter_metrics])

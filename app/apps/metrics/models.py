from typing import Any, Dict, List, Optional, Type

import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property

from app.db.middleware import get_db
from app.db.models import BaseModel, TBase


class Metric(BaseModel):
    __tablename__ = "metrics"

    date = sa.Column(sa.Date, nullable=False, index=True)
    channel = sa.Column(sa.String, nullable=False, index=True)
    country = sa.Column(sa.String, nullable=False, index=True)
    os = sa.Column(sa.String, nullable=False, index=True)
    impressions = sa.Column(sa.Integer, nullable=False)
    clicks = sa.Column(sa.Integer, nullable=False)
    installs = sa.Column(sa.Integer, nullable=False)
    spend = sa.Column(sa.Float, nullable=False)
    revenue = sa.Column(sa.Float, nullable=False)

    @hybrid_property
    def cpi(self):
        return self.spend / self.installs

    @classmethod
    async def filter(
        cls: Type[TBase],
        filters: Dict[str, Any],
        sorting: Optional[Dict[str, str]] = None,
        grouping: Optional[List[str]] = None,
    ) -> List[TBase]:
        if grouping:
            query = sa.select(
                cls.date,
                cls.channel,
                cls.country,
                cls.os,
                sa.func.sum(cls.impressions).label("impressions"),
                sa.func.sum(cls.clicks).label("clicks"),
                sa.func.sum(cls.installs).label("installs"),
                sa.func.sum(cls.spend).label("spend"),
                sa.func.sum(cls.revenue).label("revenue"),
                cls.cpi,
            )
        else:
            query = sa.select(cls)
        db = get_db()
        if sorting is not None:
            query = query.order_by(*cls._build_sorting(sorting))
        if grouping is not None:
            query = query.group_by(*cls._build_grouping(grouping))
        if filters:
            query = query.where(sa.and_(True, *cls._build_filters(filters)))
        db_execute = await db.execute(query)
        if grouping:
            return [x._asdict() for x in db_execute.fetchall()]
        return db_execute.scalars().all()

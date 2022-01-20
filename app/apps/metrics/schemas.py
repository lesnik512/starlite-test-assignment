import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Channel(Enum):
    adcolony = "adcolony"
    apple_search_ads = "apple_search_ads"
    chartboost = "chartboost"
    facebook = "facebook"
    google = "google"
    unityads = "unityads"
    vungle = "vungle"


class Country(Enum):
    CA = "CA"
    DE = "DE"
    FR = "FR"
    GB = "GB"
    US = "US"


class OS(Enum):
    android = "android"
    ios = "ios"


class GroupField(Enum):
    date = "date"
    channel = "channel"
    country = "country"
    os = "os"


class SortField(Enum):
    date = "date"
    channel = "channel"
    country = "country"
    os = "os"
    impressions = "impressions"
    clicks = "clicks"
    installs = "installs"
    spend = "spend"
    revenue = "revenue"
    cpi = "cpi"


class SortDirection(Enum):
    desc = "desc"
    asc = "asc"


class Base(BaseModel):
    class Config:
        orm_mode = True


class Metric(Base):
    date: datetime.date
    channel: Channel
    country: Country
    os: OS
    impressions: int
    clicks: int
    installs: int
    spend: float
    revenue: float
    cpi: Optional[float] = None


class Metrics(Base):
    items: List[Metric]

from typing import List

from pydantic import BaseModel

from .models import DeviceType


class SiteBase(BaseModel):
    name: str
    address: str
    city: str
    state: str
    country: str
    zipcode: str


class DeviceBase(BaseModel):
    name: str
    type: DeviceType
    serial_number: str
    mac_address: str


class SiteCreate(SiteBase):
    pass


class DeviceCreate(DeviceBase):
    site_id: int


class Device(DeviceCreate):
    id: int

    class Config:
        orm_mode = True


class Site(SiteBase):
    id: int
    has: List[Device] = []

    class Config:
        orm_mode = True

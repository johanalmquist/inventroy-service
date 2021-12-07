import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class DeviceType(enum.Enum):
    ap: str = "ap"
    sw: str = "sw"
    gw: str = "gw"


class Site(Base):
    __tablename__ = "sites"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, index=True, nullable=False)
    address = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    zipcode = Column(String(10), nullable=True)

    has = relationship("Device", back_populates="site")


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, index=True, nullable=False)
    type = Column(Enum(DeviceType), index=True)
    serial_number = Column(String(50), unique=True, index=True, nullable=False)
    mac_address = Column(String(50), unique=True, index=True, nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"))
    site = relationship("Site", back_populates="has")

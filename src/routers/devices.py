from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..core import models, schemas
from ..core.database import get_database

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/")
async def list_devices(
    device: schemas.DeviceCreate, db: Session = Depends(get_database)
):
    db_device = models.Device(
        name=device.name,
        type=device.type,
        serial_number=device.serial_number,
        mac_address=device.mac_address,
        site_id=device.site_id,
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


@router.get("/device", response_model=schemas.Device)
async def view_device(
    serial: Optional[str] = None,
    mac_address: Optional[str] = None,
    db: Session = Depends(get_database),
):
    if serial and mac_address is None:
        q = serial
    if mac_address and serial is None:
        q = mac_address
    if serial and mac_address is not None:
        return "Will come soon"
    if serial is None and mac_address is None:
        raise HTTPException(
            status_code=422, detail="Pleace enter a serial or mac address"
        )

    device = (
        db.query(models.Device).filter(
            or_(models.Device.serial_number == q, models.Device.mac_address == q)
        )
    ).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found!")
    return device

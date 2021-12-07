from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core import schemas
from ..core.database import get_database
from ..crud import device, site

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", response_model=schemas.Device)
async def create_device(
    deviceData: schemas.DeviceCreate, db: Session = Depends(get_database)
):
    if await device.find_by_serial(deviceData.serial_number, db):
        raise HTTPException(
            status_code=400,
            detail=f"A device with serial number {deviceData.serial_number} already exists!",
        )
    if await device.find_by_mac(deviceData.mac_address, db):
        raise HTTPException(
            status_code=400,
            detail=f"A device with serial number {deviceData.mac_address} already exists!",
        )

    if await site.find(deviceData.site_id, db=db) is None:
        raise HTTPException(
            status_code=404,
            detail="Site not found!",
        )
    return await device.create(device=deviceData, db=db)


@router.get("/device", response_model=schemas.Device)
async def view_device(
    serial: Optional[str] = None,
    mac_address: Optional[str] = None,
    db: Session = Depends(get_database),
):
    if serial and mac_address is None:
        db_device = await device.find_by_serial(serial=serial, db=db)
    if mac_address and serial is None:
        db_device = await device.find_by_mac(mac=mac_address, db=db)
    if serial and mac_address is not None:
        return "Will come soon"
    if serial is None and mac_address is None:
        raise HTTPException(
            status_code=422, detail="Pleace enter a serial or mac address"
        )

    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found!")
    return db_device

from fastapi import APIRouter, Depends
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

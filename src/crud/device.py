from sqlalchemy.orm import Session

from ..core import models, schemas


async def create(device: schemas.DeviceCreate, db: Session):
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


async def find_by_serial(serial: str, db: Session):
    return db.query(models.Device).filter(models.Device.serial_number == serial).first()


async def find_by_mac(mac: str, db: Session):
    return db.query(models.Device).filter(models.Device.mac_address == mac).first()

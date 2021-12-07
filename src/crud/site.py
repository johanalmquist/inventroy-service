from sqlalchemy.orm import Session

from ..core import models, schemas


async def create(site: schemas.SiteCreate, db: Session):
    db_site = models.Site(
        name=site.name,
        address=site.address,
        city=site.city,
        state=site.state,
        country=site.country,
        zipcode=site.zipcode,
    )
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site


async def find_by_name(name: str, db: Session):
    db_site = db.query(models.Site).filter(models.Site.name == name).first()
    return db_site


async def get_all(db: Session):
    return db.query(models.Site).all()

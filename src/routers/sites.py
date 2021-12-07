from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core import models, schemas
from ..core.database import get_database

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get("/", response_model=List[schemas.Site])
async def list_sites(db: Session = Depends(get_database)):
    return db.query(models.Site).all()


@router.post("/")
async def create_site(site: schemas.SiteCreate, db: Session = Depends(get_database)):
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

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core import schemas
from ..core.database import get_database
from ..crud import site

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get("/", response_model=List[schemas.Site])
async def list_sites(db: Session = Depends(get_database)):
    return await site.get_all(db=db)


@router.get("/site/{id}", response_model=schemas.Site)
async def find_site(id: int, db: Session = Depends(get_database)):
    db_site = await site.find(id=id, db=db)
    if db_site is None:
        raise HTTPException(status_code=404, detail="No site found!")

    return db_site


@router.get("/site/", response_model=schemas.Site)
async def find_site_by_name(name: str, db: Session = Depends(get_database)):
    db_site = await site.find_by_name(name=name, db=db)
    if db_site is None:
        raise HTTPException(status_code=404, detail="No site found!")

    return db_site


@router.post("/", response_model=schemas.Site)
async def create_site(
    siteData: schemas.SiteCreate, db: Session = Depends(get_database)
):
    if await site.find_by_name(name=siteData.name, db=db):
        raise HTTPException(
            status_code=400, detail=f"Site with name {siteData.name} already exists!"
        )
    return await site.create(siteData, db=db)

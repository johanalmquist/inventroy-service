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


@router.get("/site/{site_name}", response_model=schemas.Site)
async def find_site(site_name, db: Session = Depends(get_database)):
    return await site.find_by_name(site_name, db=db)


@router.post("/", response_model=schemas.Site)
async def create_site(
    siteData: schemas.SiteCreate, db: Session = Depends(get_database)
):
    if await site.find_by_name(name=siteData.name, db=db):
        raise HTTPException(
            status_code=400, detail=f"Site with name {siteData.name} already exists!"
        )
    return await site.create(siteData, db=db)

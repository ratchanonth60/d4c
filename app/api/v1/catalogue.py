from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db.connect import get_db
from app.models.catalogue import Catalogue
from app.schemas.base import Failed, Successfully
from app.schemas.catalogue import CatalogueCreate, CatalogueUpdate
from app.services.catalogue import CatalogueService

router = APIRouter(prefix="/catalogues", tags=["Catalogue"])


@router.get("/catalogues/{catalogue_id}", response_model=Successfully[Catalogue])
def get_catalogue(catalogue_id: int, db: Session = Depends(get_db)):
    service = CatalogueService(db)
    catalogue = service.get(catalogue_id)
    if not catalogue:
        return Failed(code=404, msg="Catalogue not found")
    return Successfully(
        data=catalogue, msg="Catalogue retrieved successfully", code=200
    )


@router.get("/catalogues/", response_model=Successfully[List[Catalogue]])
def get_catalogues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = CatalogueService(db)
    obj = service.get_multi(skip, limit)
    return Successfully(data=obj, msg="Catalogues retrieved successfully", code=200)


@router.post("/catalogues/", response_model=Successfully[Catalogue])
def create_catalogue(catalogue: CatalogueCreate, db: Session = Depends(get_db)):
    service = CatalogueService(db)
    obj = service.create(catalogue)
    return Successfully(data=obj, msg="Catalogue created successfully", code=201)


@router.put("/catalogues/{catalogue_id}", response_model=Successfully[Catalogue])
def update_catalogue(
    catalogue_id: int, catalogue: CatalogueUpdate, db: Session = Depends(get_db)
):
    service = CatalogueService(db)
    db_catalogue = service.get(catalogue_id)
    if not db_catalogue:
        return Failed(code=404, msg="Catalogue not found")
    obj = service.update(db_catalogue, catalogue)
    return Successfully(data=obj, msg="Catalogue updated successfully", code=200)


@router.delete("/catalogues/{catalogue_id}", response_model=Successfully[Catalogue])
def delete_catalogue(catalogue_id: int, db: Session = Depends(get_db)):
    service = CatalogueService(db)
    catalogue = service.remove(catalogue_id)
    if not catalogue:
        return Failed(code=404, msg="Catalogue not found")
    return Successfully(data=catalogue, msg="Catalogue deleted successfully", code=200)

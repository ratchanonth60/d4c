from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db.connect import get_db
from app.models.checkout import Checkout
from app.schemas.checkout import CheckoutCreate, CheckoutUpdate
from app.services.checkout import CheckoutService
from app.schemas.base import Failed, Successfully

router = APIRouter(prefix="/checkouts", tags=["Checkout"])


@router.get("/checkouts/{checkout_id}", response_model=Successfully[Checkout])
def get_checkout(checkout_id: int, db: Session = Depends(get_db)):
    service = CheckoutService(db)
    checkout = service.get(checkout_id)
    if not checkout:
        return Failed(code=404, msg="Checkout not found")
    return Successfully(
        status="success", code=200, msg="Checkout retrieved", data=checkout
    )


@router.get("/checkouts/", response_model=Successfully[List[Checkout]])
def get_checkouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = CheckoutService(db)
    obj = service.get_multi(skip, limit)
    return Successfully(data=obj, msg="Checkouts retrieved successfully", code=200)


@router.post("/checkouts/", response_model=Successfully[Checkout])
def create_checkout(checkout: CheckoutCreate, db: Session = Depends(get_db)):
    service = CheckoutService(db)
    obj = service.create(checkout)
    return Successfully(data=obj, msg="Checkout created successfully", code=201)


@router.put("/checkouts/{checkout_id}", response_model=Successfully[Checkout])
def update_checkout(
    checkout_id: int, checkout: CheckoutUpdate, db: Session = Depends(get_db)
):
    service = CheckoutService(db)
    db_checkout = service.get(checkout_id)
    if not db_checkout:
        return Failed(code=404, msg="Checkout not found")
    obj = service.update(db_checkout, checkout)
    return Successfully(data=obj, msg="Checkout updated successfully", code=200)


@router.delete("/checkouts/{checkout_id}", response_model=Successfully[Checkout])
def delete_checkout(checkout_id: int, db: Session = Depends(get_db)):
    service = CheckoutService(db)
    checkout = service.remove(checkout_id)
    if not checkout:
        return Failed(code=404, msg="Checkout not found")
    return Successfully(data=checkout, msg="Checkout deleted successfully", code=200)

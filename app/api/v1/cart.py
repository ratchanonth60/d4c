from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.db.connect import get_db
from app.models.cart import Cart, CartLine
from app.models.user import User, UserRole
from app.schemas.base import Failed, Successfully
from app.services.cart import (
    CartCreate,
    CartLineCreate,
    CartLineService,
    CartLineUpdate,
    CartService,
    CartUpdate,
)

router = APIRouter(prefix="/carts", tags=["Cart"])


def get_current_user(request: Request) -> User:
    """Dependency to get the current user from request.state."""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure the user is an admin."""
    if current_user.role != UserRole.ADMIN:  # type: ignore[comparison-overlap]
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/carts/{cart_id}", response_model=Successfully[Cart])
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    service = CartService(db)
    cart = service.get(cart_id)
    if not cart:
        return Failed(msg="Cart not found", code=404)
    return Successfully(data=cart, msg="Cart retrieved successfully", code=200)


@router.get("/carts/", response_model=Successfully[List[Cart]])
def get_carts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = CartService(db)
    list_cart = service.get_multi(skip, limit)
    return Successfully(data=list_cart, msg="Carts retrieved successfully", code=200)


@router.post("/carts/", response_model=Successfully[Cart])
def create_cart(cart: CartCreate, db: Session = Depends(get_db)):
    service = CartService(db)
    obj = service.create(cart)
    return Successfully(data=obj, msg="Cart created successfully", code=201)


@router.put("/carts/{cart_id}", response_model=Successfully[Cart])
def update_cart(cart_id: int, cart: CartUpdate, db: Session = Depends(get_db)):
    service = CartService(db)
    db_cart = service.get(cart_id)
    if not db_cart:
        return Failed(msg="Cart not found", code=404)
    obj = service.update(db_cart, cart)
    return Successfully(data=obj, msg="Cart updated successfully", code=200)


@router.delete("/carts/{cart_id}", response_model=Successfully[Cart])
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    service = CartService(db)
    cart = service.remove(cart_id)
    if not cart:
        return Failed(msg="Cart not found", code=404)
    return Successfully(data=cart, msg="Cart deleted successfully", code=200)


@router.get("/carts/{cart_id}/total/")
def get_cart_total(cart_id: int, tax_rate: float = 0.07, db: Session = Depends(get_db)):
    service = CartService(db)
    total = service.calculate_total(cart_id, tax_rate)
    json = {"cart_id": cart_id, "total_amount": total}
    return Successfully(data=json, msg="Cart total retrieved successfully", code=200)


@router.post("/carts/{cart_id}/apply-discount/")
def apply_cart_discount(
    cart_id: int, discount_rate: float, db: Session = Depends(get_db)
):
    service = CartService(db)
    total_discount = service.apply_discount(cart_id, discount_rate)
    json = {"cart_id": cart_id, "total_discount": total_discount}
    return Successfully(data=json, msg="Cart discount applied successfully", code=200)


# 4. CartLine Endpoints
@router.get("/cart-lines/{cart_line_id}", response_model=Successfully[CartLine])
def get_cart_line(cart_line_id: int, db: Session = Depends(get_db)):
    service = CartLineService(db)
    cart_line = service.get(cart_line_id)
    if not cart_line:
        return Failed(msg="CartLine not found", code=404)
    return Successfully(data=cart_line, msg="CartLine retrieved successfully", code=200)


@router.get("/cart-lines/", response_model=Successfully[List[CartLine]])
def get_cart_lines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = CartLineService(db)
    obj = service.get_multi(skip, limit)
    return Successfully(data=obj, msg="CartLines retrieved successfully", code=200)


@router.post("/cart-lines/", response_model=Successfully[CartLine])
def create_cart_line(cart_line: CartLineCreate, db: Session = Depends(get_db)):
    service = CartLineService(db)
    obj = service.create(cart_line)
    return Successfully(data=obj, msg="CartLine created successfully", code=201)


@router.put("/cart-lines/{cart_line_id}", response_model=Successfully[CartLine])
def update_cart_line(
    cart_line_id: int, cart_line: CartLineUpdate, db: Session = Depends(get_db)
):
    service = CartLineService(db)
    db_cart_line = service.get(cart_line_id)
    if not db_cart_line:
        return Failed(msg="CartLine not found", code=404)
    obj = service.update(db_cart_line, cart_line)
    return Successfully(data=obj, msg="CartLine updated successfully", code=200)


@router.delete("/cart-lines/{cart_line_id}", response_model=Successfully[CartLine])
def delete_cart_line(cart_line_id: int, db: Session = Depends(get_db)):
    service = CartLineService(db)
    cart_line = service.remove(cart_line_id)
    if not cart_line:
        return Failed(msg="CartLine not found", code=404)
    return Successfully(data=cart_line, msg="CartLine deleted successfully", code=200)


@router.post("/cart-lines/{cart_line_id}/apply-discount/")
def apply_cart_line_discount(
    cart_line_id: int, discount_rate: float, db: Session = Depends(get_db)
):
    service = CartLineService(db)
    discount = service.apply_discount(cart_line_id, discount_rate)
    json = {"cart_line_id": cart_line_id, "discount": discount}
    return Successfully(
        data=json, msg="CartLine discount applied successfully", code=200
    )


@router.get("/cart-lines/{cart_line_id}/tax/")
def get_cart_line_tax(
    cart_line_id: int, tax_rate: float = 0.07, db: Session = Depends(get_db)
):
    service = CartLineService(db)
    tax = service.calculate_tax(cart_line_id, tax_rate)
    json = {"cart_line_id": cart_line_id, "tax": tax}
    return Successfully(data=json, msg="CartLine tax calculated successfully", code=200)

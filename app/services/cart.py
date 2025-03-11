from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseError
from app.models.cart import Cart, CartLine
from app.schemas.cart import CartCreate, CartUpdate, CartLineCreate, CartLineUpdate
from app.services.base import BaseService


class CartService(BaseService[Cart, CartCreate, CartUpdate]):
    """Service class for managing cart-related operations."""

    def __init__(self, db: Session):
        super().__init__(model=Cart, db=db)

    def create(self, obj_in: CartCreate) -> Cart:
        """Create a new cart for a customer."""
        try:
            self.logger.info(f"Creating cart for customer_id: {obj_in.customer_id}")
            create_data = obj_in.model_dump()
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except Exception as e:
            self.logger.error(f"Cart creation failed: {str(e)}")
            raise DatabaseError(f"Failed to create cart: {str(e)}")

    def calculate_total(self, cart_id: int, tax_rate: float = 0.07) -> float:
        """Calculate the total amount for the cart including tax."""
        cart = self.get(cart_id)
        if not cart:
            raise DatabaseError(f"Cart with id {cart_id} not found")
        return cart.calculate_cart_total(tax_rate)

    def apply_discount(self, cart_id: int, discount_rate: float) -> float:
        """Apply a discount to all cart lines and return the total discount."""
        cart = self.get(cart_id)
        if not cart:
            raise DatabaseError(f"Cart with id {cart_id} not found")
        total_discount = cart.apply_cart_discount(discount_rate)
        with self._session_scope() as session:
            session.add(cart)
        return total_discount


class CartLineService(BaseService[CartLine, CartLineCreate, CartLineUpdate]):
    """Service class for managing cart line-related operations."""

    def __init__(self, db: Session):
        super().__init__(model=CartLine, db=db)

    def create(self, obj_in: CartLineCreate) -> CartLine:
        """Create a new cart line for a cart."""
        try:
            create_data = obj_in.model_dump()
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)

                # อัปเดตยอดรวมของ Cart
                cart = session.query(Cart).filter(Cart.id == db_obj.cart_id).first()
                if cart:
                    cart.calculate_cart_total(tax_rate=0.0)  # อัปเดต total_amount
                    session.add(cart)

            return db_obj
        except Exception as e:
            self.logger.error(f"CartLine creation failed: {str(e)}")
            raise DatabaseError(f"Failed to create cart line: {str(e)}")

    def apply_discount(self, cart_line_id: int, discount_rate: float) -> float:
        """Apply a discount to a cart line."""
        cart_line = self.get(cart_line_id)
        if not cart_line:
            raise DatabaseError(f"CartLine with id {cart_line_id} not found")
        discount = cart_line.apply_discount(discount_rate)
        with self._session_scope() as session:
            session.add(cart_line)
            # อัปเดตยอดรวมของ Cart
            cart = session.query(Cart).filter(Cart.id == cart_line.cart_id).first()
            if cart:
                cart.calculate_cart_total(tax_rate=0.0)
                session.add(cart)
        return discount

    def calculate_tax(self, cart_line_id: int, tax_rate: float) -> float:
        """Calculate tax for a cart line."""
        cart_line = self.get(cart_line_id)
        if not cart_line:
            raise DatabaseError(f"CartLine with id {cart_line_id} not found")
        return cart_line.calculate_tax(tax_rate)

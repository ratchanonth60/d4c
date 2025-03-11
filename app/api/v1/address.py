from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.db.connect import get_db
from app.models.address import Address
from app.models.user import User, UserRole
from app.schemas.address import AddressCreate, AddressResponse, AddressUpdate
from app.schemas.base import Failed, Successfully
from app.services.address import AddressService

router = APIRouter(prefix="/addresses", tags=["Addresses"])


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


@router.post("/", response_model=Successfully[AddressResponse])
async def create_address(
    address: AddressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new address for the authenticated user."""
    address_service = AddressService(db)
    address.user_id = current_user.id
    new_address = address_service.create(address)
    return Successfully(
        code=201,
        msg="Address created successfully",
        data=AddressResponse.from_orm(new_address),
    )


@router.get("/me", response_model=Successfully[list[AddressResponse]])
async def get_my_addresses(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    addresses = (
        db.query(Address)
        .filter(Address.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return Successfully(
        code=200,
        msg="Addresses retrieved successfully",
        data=[AddressResponse.from_orm(addr) for addr in addresses],
    )


@router.get("/{address_id}", response_model=Successfully[AddressResponse])
async def get_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific address by ID (restricted to owner or admin)."""
    address_service = AddressService(db)
    address = address_service.get(address_id)
    if not address:
        return Failed(code=404, msg="Address not found")
    if address.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this address"
        )
    return Successfully(
        code=200,
        msg="Address retrieved successfully",
        data=AddressResponse.from_orm(address),
    )


@router.put("/{address_id}", response_model=Successfully[AddressResponse])
async def update_address(
    address_id: int,
    address_update: AddressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an address (restricted to owner or admin)."""
    address_service = AddressService(db)
    address = address_service.get(address_id)
    if not address:
        return Failed(code=404, msg="Address not found")
    if address.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this address"
        )
    updated_address = address_service.update(address, address_update)
    return Successfully(
        code=200,
        msg="Address updated successfully",
        data=AddressResponse.from_orm(updated_address),
    )


@router.delete("/{address_id}", response_model=Successfully[None])
async def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an address (restricted to owner or admin)."""
    address_service = AddressService(db)
    address = address_service.get(address_id)
    if not address:
        return Failed(code=404, msg="Address not found")
    if address.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this address"
        )
    address_service.remove(address_id)
    return Successfully(
        code=200,
        msg="Address deleted successfully",
        data=None,
    )

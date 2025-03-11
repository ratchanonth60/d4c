from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.db.connect import get_db
from app.models.user import User, UserRole
from app.schemas.base import Failed, Successfully
from app.schemas.user import UserResponse, UserUpdate
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_current_user(request: Request) -> User:
    """Dependency to get the current user from request.state."""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure the user is an admin."""
    if bool(current_user.role) != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/me", response_model=Successfully[UserResponse])
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get the profile of the currently authenticated user."""
    user_service = UserService(db)
    user = user_service.get(int(current_user.id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return Successfully(
        status="success",
        code=200,
        msg="User profile retrieved successfully",
        data=UserResponse.from_orm(user),
    )


@router.get("/{user_id}", response_model=Successfully[UserResponse])
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user),
):
    """Get a user's profile by ID (admin only)."""
    user_service = UserService(db)
    user = user_service.get(user_id)
    if not user:
        return Failed(status="fail", code=404, msg="User not found")
    return Successfully(
        status="success",
        code=200,
        msg="User retrieved successfully",
        data=UserResponse.from_orm(user),
    )


@router.get("/", response_model=Successfully[list[UserResponse]])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user),
):
    """Get all users with pagination (admin only)."""
    user_service = UserService(db)
    users = user_service.get_multi(skip=skip, limit=limit)
    return Successfully(
        status="success",
        code=200,
        msg="Users retrieved successfully",
        data=[UserResponse.from_orm(user) for user in users],
    )


@router.put("/me", response_model=Successfully[UserResponse])
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update the profile of the currently authenticated user."""
    user_service = UserService(db)
    updated_user = user_service.update(current_user, user_update)
    return Successfully(
        status="success",
        code=200,
        msg="User updated successfully",
        data=UserResponse.from_orm(updated_user),
    )


@router.put("/{user_id}", response_model=Successfully[UserResponse])
async def update_user_by_id(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user),
):
    """Update a user by ID (admin only)."""
    user_service = UserService(db)
    user = user_service.get(user_id)
    if not user:
        return Failed(status="fail", code=404, msg="User not found")
    updated_user = user_service.update(user, user_update)
    return Successfully(
        status="success",
        code=200,
        msg="User updated successfully",
        data=UserResponse.from_orm(updated_user),
    )


@router.delete("/me", response_model=Successfully[None])
async def delete_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete the currently authenticated user."""
    user_service = UserService(db)
    user_service.remove(current_user.id)
    return Successfully(
        status="success",
        code=200,
        msg="User deleted successfully",
        data=None,
    )


@router.delete("/{user_id}", response_model=Successfully[None])
async def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user),
):
    """Delete a user by ID (admin only)."""
    user_service = UserService(db)
    user = user_service.remove(user_id)
    if not user:
        return Failed(status="fail", code=404, msg="User not found")
    return Successfully(
        status="success",
        code=200,
        msg="User deleted successfully",
        data=None,
    )


@router.post("/{user_id}/verify", response_model=Successfully[UserResponse])
async def verify_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user),
):
    """Mark a user as verified (admin only)."""
    user_service = UserService(db)
    user = user_service.get(user_id)
    if not user:
        return Failed(status="fail", code=404, msg="User not found")
    user_update = UserUpdate(is_verified=True)
    updated_user = user_service.update(user, user_update)
    return Successfully(
        status="success",
        code=200,
        msg="User verified successfully",
        data=UserResponse.from_orm(updated_user),
    )

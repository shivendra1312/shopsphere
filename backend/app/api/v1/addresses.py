from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.address import AddressCreate, AddressResponse
from app.services import address_service

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.get("", response_model=List[AddressResponse])
def get_addresses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all saved addresses for the logged-in user.
    """
    return address_service.get_user_addresses(db, current_user.id)

@router.post("", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def add_address(address_in: AddressCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Save a new address for checkout.
    """
    return address_service.create_address(db, current_user.id, address_in)

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete a saved address.
    """
    address_service.delete_address(db, current_user.id, address_id)
    return None

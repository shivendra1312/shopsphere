from sqlalchemy.orm import Session
from app.models.address import Address
from app.schemas.address import AddressCreate
from fastapi import HTTPException

def get_user_addresses(db: Session, user_id: int):
    return db.query(Address).filter(Address.user_id == user_id).all()

def create_address(db: Session, user_id: int, address_in: AddressCreate):
    # Agar user pehli baar address daal raha hai (ya is_default true bheja hai), 
    # toh baaki sabhi addresses ko non-default kardo
    if address_in.is_default:
        db.query(Address).filter(Address.user_id == user_id).update({"is_default": False})
        
    new_address = Address(
        user_id=user_id,
        full_name=address_in.full_name,
        street=address_in.street,
        city=address_in.city,
        state=address_in.state,
        zip_code=address_in.zip_code,
        phone=address_in.phone,
        is_default=address_in.is_default
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

def delete_address(db: Session, user_id: int, address_id: int):
    address = db.query(Address).filter(Address.id == address_id, Address.user_id == user_id).first()
    if address:
        db.delete(address)
        db.commit()
    return True

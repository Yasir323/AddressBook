from typing import List

from fastapi import FastAPI, HTTPException, APIRouter

from address_book.db import get_db
from address_book.db_models import Address
from address_book.schema import AddressRequest, AddressResponse
from address_book.utils import calculate_distance

address_book_route = APIRouter()
Number = int | float


@address_book_route.post("/", response_model=AddressResponse)
def create_address(address: AddressRequest):
    db = get_db()
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


@address_book_route.get("/{address_id}", response_model=AddressResponse)
def get_address(address_id: int):
    db = get_db()
    address = db.query(Address).filter(Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@address_book_route.put("/{address_id}", response_model=AddressResponse)
def update_address(address_id: int, address: AddressRequest):
    db = get_db()
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in address.dict().items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address


@address_book_route.delete("/{address_id}")
def delete_address(address_id: int):
    db = get_db()
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return {"message": "Address deleted successfully"}


# API endpoint to retrieve addresses within a given distance from a location
@address_book_route.get("/search/", response_model=List[AddressResponse])
def search_addresses(latitude: Number, longitude: Number, distance: Number):
    db = get_db()
    addresses = db.query(Address).all()
    nearby_addresses = []
    for addr in addresses:
        dist = calculate_distance(latitude, longitude, addr.latitude, addr.longitude)
        if dist <= distance:
            nearby_addresses.append(addr)
    if not nearby_addresses:
        raise HTTPException(status_code=404, detail="No nearby coordinates found in the given radius")
    return nearby_addresses

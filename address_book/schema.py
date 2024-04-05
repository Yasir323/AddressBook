from pydantic import BaseModel


class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float


class AddressResponse(AddressBase):
    id: int


class AddressRequest(AddressBase):
    pass

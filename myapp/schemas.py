from pydantic import BaseModel


class CustomerBase(BaseModel):
    id: int
    name: str
    contact_number: str
    is_active: bool

    class Config:
        orm_mode = True


class AddressBase(BaseModel):
    customer_id: int
    present_address: str
    permenent_address: str

    class Config:
        orm_mode = True


class Address(AddressBase):
    pass


class CustomerFull(BaseModel):
    id: int
    name: str
    contact_number: str
    is_active: bool
    addresses: Address

    class Config:
        orm_mode = True

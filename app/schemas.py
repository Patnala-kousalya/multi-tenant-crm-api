from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    organization_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ContactCreate(BaseModel):
    name: str
    email: str

class ContactOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

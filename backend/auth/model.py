from pydantic import BaseModel, EmailStr

class admin(BaseModel):
    role: str
    email: EmailStr
    password: str

class regular(admin):
    slug: str
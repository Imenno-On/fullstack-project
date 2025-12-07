from pydantic import BaseModel, EmailStr

# ----- request / response -----
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr

# ----- JWT -----
class Token(BaseModel):
    access_token: str
    token_type: str

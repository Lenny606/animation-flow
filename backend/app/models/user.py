from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The user's email address", examples=["user@example.com"])

class UserCreate(UserBase):
    password: str = Field(..., description="The user's password", min_length=8, examples=["secretpassword123"])

class UserLogin(UserBase):
    password: str = Field(..., description="The user's password", examples=["secretpassword123"])

class UserInDB(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    hashed_password: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class User(UserBase):
    id: Optional[str] = Field(alias="_id", default=None, description="The unique identifier of the user", examples=["60d5ecb8b392d011f8871123"])
    
    class Config:
        populate_by_name = True
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "60d5ecb8b392d011f8871123",
                "email": "user@example.com"
            }
        }

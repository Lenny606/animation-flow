from pydantic import BaseModel, EmailStr, Field, GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import Optional, List, Any
from bson import ObjectId
from enum import Enum

class UserRole(str, Enum):
    FREE = "free"
    PRO = "pro"
    ADMIN = "admin"

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x), when_used='json'
            ),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The user's email address", examples=["user@example.com"])
    role: UserRole = Field(default=UserRole.FREE, description="The user's role", examples=["free"])

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
    id: Optional[PyObjectId] = Field(alias="_id", default=None, description="The unique identifier of the user", examples=["60d5ecb8b392d011f8871123"])
    
    class Config:
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "60d5ecb8b392d011f8871123",
                "email": "user@example.com",
                "role": "free"
            }
        }

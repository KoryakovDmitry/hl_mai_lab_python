from pydantic import BaseModel
from typing import List
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    first_name: str
    last_name: str
    email: str


class UserResponse(UserBase):
    # id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


# Service schemas
class ServiceBase(BaseModel):
    name: str


class ServiceCreate(ServiceBase):
    description: str
    cost: float


class ServiceResponse(ServiceBase):
    id: int
    description: str
    cost: float

    class Config:
        orm_mode = True


class OrderServiceAdd(BaseModel):
    service_ids: List[int]  # Changed from service_id to service_ids


# Order schemas
class OrderBase(BaseModel):
    user_id: int
    date_created: datetime


class OrderCreate(BaseModel):
    user_id: int
    service_ids: List[int]  # New field to list service IDs


# Assuming you have a schema for Service
class ServiceInOrder(BaseModel):
    id: int
    name: str
    description: str
    cost: float

    class Config:
        orm_mode = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    date_created: datetime
    services: List[ServiceInOrder]  # New field to include services

    class Config:
        orm_mode = True

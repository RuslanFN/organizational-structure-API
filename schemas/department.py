from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class Department(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=200)
    parent_id: Optional[int] = None
    created_at: datetime

class DepartmentResponse(BaseModel):
    status: int
    data: Department

    
class CreateDepartment(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    parent_id: Optional[int] = None

class GetDepartment(BaseModel):
    depth: int = Field(1, ge=1, le=5)
    include_employees: bool = True

class MoveDepartment(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=200)
    parent_id: Optional[int] = None

class DeleteDepartment(BaseModel):
    mode: Literal['cascade', 'reassign']
    reassign_to_department_id: Optional[int] = None 
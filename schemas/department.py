from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class DepartmentResponse(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=200)
    parent_id: Optional[int] = Field(default=None)  
    created_at: datetime

class CreateDepartment(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    parent_id: Optional[int] = Field(default=None)  
    model_config = {
        "str_strip_whitespace": True 
    }
class GetDepartment(BaseModel):
    depth: int = Field(1, ge=1, le=5)
    include_employees: bool = True
    model_config = {
        "str_strip_whitespace": True 
    }
class MoveDepartment(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    parent_id: Optional[int] = Field(default=None)  
    model_config = {
        "str_strip_whitespace": True 
    }
class DeleteDepartment(BaseModel):
    mode: Literal['cascade', 'reassign']
    reassign_to_department_id: Optional[int] = None 
    model_config = {
        "str_strip_whitespace": True 
    }
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class ResponseEmployee(BaseModel):
    id: int
    full_name: str
    position: str
    department_id: int
    hired_at: Optional[datetime] = Field(default=None)
    created_at: datetime
    
class CreateEmployee(BaseModel):
    full_name: str
    position: str
    hired_at: Optional[datetime] = Field(default=None)
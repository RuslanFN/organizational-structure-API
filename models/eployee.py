from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from sqlalchemy import DateTime, ForeignKey
from datetime import datetime
from typing import TYPE_CHECKING
from .base import Base
if TYPE_CHECKING:
    from .department import Department

class Employee(Base):
    __tablename__ = 'employee'
    department_id: Mapped[int] = mapped_column(ForeignKey('department.id', ondelete='CASCADE'))
    full_name: Mapped[str]
    position: Mapped[str]
    hired_at: Mapped[datetime|None] = mapped_column(DateTime)
    department: Mapped['Department'] = relationship(back_populates='employees')
    

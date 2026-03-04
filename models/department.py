from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from typing import List, Optional, TYPE_CHECKING
from .base import Base
if TYPE_CHECKING:
    from .employee import Employee

class Department(Base):
    __tablename__ = 'department'
    name: Mapped[str]
    parent_id: Mapped[int|None] = mapped_column(ForeignKey('department.id'))
    parent: Mapped[Optional['Department']] = relationship(back_populates='children')
    children: Mapped[List['Department']] = relationship(back_populates='parent')
    epployee: Mapped[List['Employee']] = relationship(back_populates='department')
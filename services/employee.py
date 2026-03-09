from sqlalchemy.orm import Session
from sqlalchemy import select, exists, and_, update
from models import Department, Employee
from datetime import datetime
from . import DepartmentService

class EmployeeService:
    def __init__(self, session:Session):
        self.session = session

    def create_employee(self, department_id: int, full_name: str, position: str, hired_at: datetime|None = None) -> Employee:
        service = DepartmentService(session=self.session)
        department = service.get_department(department_id)
        if not department:
            raise ValueError('Непрвильный id депортамента')
        employee = Employee(department_id=department_id, full_name=full_name, position=position)
        if hired_at:
            employee.hired_at = hired_at
        self.session.add(employee)
        self.session.commit()
        return employee
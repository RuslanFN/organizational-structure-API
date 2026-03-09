from fastapi import APIRouter, Depends, HTTPException, status, Query
from db import get_session
from services import EmployeeService
from schemas import CreateEmployee, ResponseEmployee
router = APIRouter()

@router.post('/departments/{id}/employees/', response_model=ResponseEmployee)
def create_employee(id: int, data: CreateEmployee, session = Depends(get_session)):
    service = EmployeeService(session)
    try:
        department_id = id
        full_name = data.full_name
        position = data.position
        hired_at = data.hired_at
        employee = service.create_employee(department_id, full_name, position, hired_at)
        return employee
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
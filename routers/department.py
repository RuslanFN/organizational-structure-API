from fastapi import APIRouter, Depends, HTTPException, status, Query
from db import get_session
from schemas import CreateDepartment, GetDepartment, MoveDepartment, DeleteDepartment, DepartmentResponse
from services import DepartmentService
router = APIRouter()

@router.post('/departments/', response_model=DepartmentResponse)
def create_department(data: CreateDepartment, session=Depends(get_session)):
    service = DepartmentService(session)
    name = data.name
    parent_id = data.parent_id
    try:
        department = service.create_department(name, parent_id)
        response = {
            'status': status.HTTP_200_OK,
            'data': department}
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))

@router.get('/department/{id}')
def get_department(id: int, data: GetDepartment=Query(), session=Depends(get_session)):
    service = DepartmentService(session)
    depth = data.depth
    include_employees = data.include_employees
    try:
        department = service.get_department_dept(id, depth, include_employees)
        response = {
            'status': status.HTTP_200_OK,
            'data': department}
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))

@router.patch('/department/{id}', response_model=DepartmentResponse)
def move_depatment(id: int, data: MoveDepartment, session=Depends(get_session)):
    service = DepartmentService(session)
    name = data.name
    parent_id = data.parent_id
    try:
        department = service.edit_parent(id, name, parent_id)
        response = {
            'status': status.HTTP_200_OK,
            'data': department}
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e)
    
@router.delete('/department/{id}', response_model=DepartmentResponse)
def delete_department(id: int, data: DeleteDepartment, session=Depends(get_session)):
    service = DepartmentService(session)
    try:
        mode = data.mode
        resighn = data.reassign_to_department_id
        service.delete_department(id, mode, resighn)
        return status.HTTP_204_NO_CONTENT
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e)
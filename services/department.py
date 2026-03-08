from sqlalchemy.orm import Session
from sqlalchemy import select, exists, and_, update
from sqlalchemy.exc import NoResultFound
from models import Department, Employee
class DepartmentService:
    def __init__(self, session: Session):
        self.session = session
    
    def get_department(self, id: int) -> Department|None:
        return self.session.get(Department, id)
    
    def create_department(self, name: str, parent_id: int|None = None) -> Department:
        '''
        Создать подразделение
        '''
        try:
            if parent_id:
                stmt = select(Department).where(Department.id == parent_id)
                department = self.session.execute(stmt).scalar_one()
                if not self.is_name_unique(parant_id=parent_id, name=name):
                    raise ValueError('Имя депортамента должно быть уникальным среди потомков')
                new_department = Department(name=name, parent=department)
            else:
                new_department = Department(name=name)
            self.session.add(new_department)
            self.session.commit()
        except NoResultFound:
            raise ValueError('Департамент с таким ID не найден')
        return new_department
    
    def contain_in_children(self, id: int, parant_id: int) -> bool:
        children_ids = select(Department.id).where(Department.id == id).cte(recursive=True)
        children_ids = children_ids.union_all(
            select(Department.id).where(Department.parent_id == children_ids.c.id)
            )
        stmt = select(exists().where(children_ids.c.id == parant_id))
        return self.session.execute(stmt).scalar()
    
    def is_name_unique(self, parant_id, name) -> bool:
        stmt = select(Department.name).where(Department.parent_id == parant_id, Department.name == name)
        return self.session.execute(stmt).scalar() is None
        
    def edit_parent(self, id: int, name:str|None, parant_id: int|None) -> Department:
        ''' 
        Переместить подразделение в другое (изменить parent)
        '''
        department = self.get_department(id)
        if not department:
            raise ValueError('Отсутствует департамент с таким id')
        if parant_id:
            if id == parant_id:
                raise ValueError('Нельзя сделать депортамент потомком самого себя')
            if self.contain_in_children(id, parant_id):
                raise ValueError('Нельзя сделать департамент родителем департамента, который входит в него')
            department.parent_id = parant_id
        if name:
            if parant_id:
                if not self.is_name_unique(parant_id, department.name):
                    ValueError('Имя депортамента должно быть уникальным среди потомков')
            else:
                if not self.is_name_unique(id, department.name):
                    ValueError('Имя депортамента должно быть уникальным среди потомков')
            department.name = name    
        self.session.add(department)
        self.session.commit()
        self.session.refresh(department)
        return department
        
    def delete_department(self, id: int, mode: str, reassign_to_department_id: int|None = None):
        if mode == 'reassign' and not reassign_to_department_id:
            raise ValueError('Не указан id депортамента для перевода сотрудников')
        if mode not in ['reassign', 'cascade']:
            raise ValueError('Неправильная опция mode. Доступны только reassign и cascade')
        department = self.get_department(id)
        if department is None:
            raise ValueError('Депортамента с таким id не существует')
        if mode == 'reassign':
            stmt = (update(Department)
                        .where(Department.parent_id == department.id)
                        .values(parent_id = department.parent_id))
            self.session.execute(stmt)
            stmt = (update(Employee)
                        .where(Employee.department_id == department.id)
                        .values(department_id = reassign_to_department_id))
            self.session.execute(stmt)
        self.session.delete(department)
        self.session.commit()
    
    def get_department_dept(self, id: int, depth: int=1, include_employees: bool=True): 
        '''
        Получить подразделение (детали + сотрудники + поддерево)
        '''
        department = self.get_department(id)
        if not department:
            raise ValueError('Депортамент не найден')
        def make_response_by_depth(department, depth):
            response_dict = {
                'id': department.id,
                'name': department.name,
                'parent_id': department.parent_id,
                'created_at': department.created_at,
                'employees': [],
                'children': [],
            }
            if include_employees:
                response_dict['employees'] = sorted(department.employees, key=lambda e:e.full_name)
            if depth == 1 or not department.children:
                return response_dict
            if department.children:
                response_dict['children'] = []
                for child in department.children:
                    (response_dict['children']
                                    .append(
                                        make_response_by_depth(child, 
                                                            depth=depth-1)))
            return response_dict
        return make_response_by_depth(department, depth)


        
        
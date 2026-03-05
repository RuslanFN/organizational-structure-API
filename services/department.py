from sqlalchemy.orm import Session
from sqlalchemy import select, exists, and_
from sqlalchemy.exc import NoResultFound
from models import Department, Employee
class DepartmentService:
    def __init__(self, session: Session):
        self.session = session
    
    def get_departments(self, id: int) -> Department|None:
        return self.session.get(Department, id)
    
    def create_department(self, name: str, id: int|None) -> Department:
        try:
            if id:
                stmt = select(Department).where(Department.id == id)
                department = self.session.execute(stmt).scalar_one()
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
        
    def edit_parent(self, id: int, parant_id: int) -> Department:
        department = self.get_departments(id)
        if not department:
            raise ValueError('Отсутствует департамент с таким id')
        if id == parant_id:
            raise ValueError('Нельзя сделать депортамент потомком самого себя')
        if not self.contain_in_children(id, parant_id):
            if not self.is_name_unique(parant_id, department.name):
                ValueError('Имя депортамента должно быть уникальным среди потомков')
            department.parent_id = parant_id
            self.session.add(department)
            self.session.commit()
            self.session.refresh(department)
            return department
        else:
            raise ValueError('Нельзя сделать департамент родителем департамента, который входит в него')

    

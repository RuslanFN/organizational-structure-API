import pytest
from fastapi import status

def test_create_and_cycle(client):
    # Создаем A
    a = client.post("/departments/", json={"name": "A"}).json()
    # Создаем B (ребенок A)
    b = client.post("/departments/", json={"name": "B", "parent_id": a["id"]}).json()
    # Пытаемся сделать A ребенком B (Цикл!)
    res = client.patch(f"/departments/{a['id']}", json={"parent_id": b["id"]})
    print(a, b)
    assert res.status_code == 400

def test_unique_name_constraint(client):
    # 1. Создаем родителя
    parent = client.post("/departments/", json={"name": "IT"}).json()
    parent_id = parent["id"]
    
    # 2. Создаем первый отдел "Backend"
    client.post("/departments/", json={"name": "Backend", "parent_id": parent_id})
    
    # 3. Пытаемся создать второй "Backend" там же (должна быть ошибка)
    response = client.post("/departments/", json={"name": "Backend", "parent_id": parent_id})
    assert response.status_code == 400
    assert "должно быть уникальным" in response.json()["detail"]

    # 4. Проверяем, что в другом родителе (или в корне) имя "Backend" разрешено
    response_root = client.post("/departments/", json={"name": "Backend", "parent_id": None})
    assert response_root.status_code == 201 or response_root.status_code == 200

def test_get_tree_depth(client):
    # Создаем цепочку: A -> B -> C
    dep_a = client.post("/departments/", json={"name": "A"}).json()
    dep_b = client.post("/departments/", json={"name": "B", "parent_id": dep_a["id"]}).json()
    dep_c = client.post("/departments/", json={"name": "C", "parent_id": dep_b["id"]}).json()

    # Запрашиваем A с depth=1 (только A, без вложенных детей)
    res_d1 = client.get(f"/departments/{dep_a['id']}?depth=1").json()
    print(dep_a, dep_b, dep_c)
    assert len(res_d1["children"]) == 0

    # Запрашиваем A с depth=2 (A и его прямой ребенок B)
    res_d2 = client.get(f"/departments/{dep_a['id']}?depth=2").json()
    print(res_d2)
    assert len(res_d2["children"]) == 1
    assert res_d2["children"][0]["name"] == "B"
    assert len(res_d2["children"][0]["children"]) == 0 # C не должен попасть

def test_delete_reassign_employees(client):
    # 1. Создаем два отдела
    old_dept = client.post("/departments/", json={"name": "Old"}).json()
    new_dept = client.post("/departments/", json={"name": "New"}).json()
    
    # 2. Создаем сотрудника в старом отделе
    emp_res = client.post(f"/departments/{old_dept['id']}/employees/", json={
        "full_name": "Ivan Ivanov",
        "position": "Developer"
    }).json()

    # 3. Удаляем старый отдел с переназначением в новый
    delete_res = client.delete(
        f"/departments/{old_dept['id']}?mode=reassign&reassign_to_department_id={new_dept['id']}"
    )
    assert delete_res.status_code == 204

    # 4. Проверяем, что сотрудник теперь в новом отделе
    # (Зависит от того, как ты получаешь данные, например через GET /departments/{id})
    check_res = client.get(f"/departments/{new_dept['id']}?include_employees=true").json()
    assert len(check_res["employees"]) == 1
    assert check_res["employees"][0]["full_name"] == "Ivan Ivanov"


def test_invalid_data_validation(client):
    # Пустое имя (min_length=1)
    res = client.post("/departments/", json={"name": ""})
    assert res.status_code == 422 # Ошибка валидации FastAPI

    # Слишком длинное имя
    res = client.post("/departments/", json={"name": "a" * 201})
    assert res.status_code == 422

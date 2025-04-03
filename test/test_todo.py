from routers.todos import get_db, get_current_user
from fastapi import status
from .utils import *

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db




def test_read_all(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"title": "Learn FastAPI",
                                "description": "It is nice",
                                "priority": 5,
                                "complete": False,
                                "owner_id": 1, "id": 1}]
def test_read_one_todo(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"title": "Learn FastAPI",
                                "description": "It is nice",
                                "priority": 5,
                                "complete": False,
                                "owner_id": 1, "id": 1}


def test_read_one_failed(test_todo):
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "todo not found"}

def test_create_new_todo(test_todo):
    request_data = {
        "title": "New Todo",
        "description": "New Todo Description",
        "priority": 5,
        "complete": False
    }
    response = client.post("/todos/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 2).first()

    assert todo.title == request_data.get("title")
    assert todo.description == request_data.get("description")
    assert todo.priority == request_data.get("priority")
    assert todo.complete == request_data.get("complete")

def test_update_todo(test_todo):
    request_data = {"title": "Learn faster FastAPI",
     "description": "It is nice",
     "priority": 5,
     "complete": False}
    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db= TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo.title == "Learn faster FastAPI"

def test_update_todo_not_found(test_todo):
    request_data = {"title": "Learn faster FastAPI",
     "description": "It is nice",
     "priority": 5,
     "complete": False}
    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "todo not found"}


def test_delete_todo(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo is None

def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "todo not found"}

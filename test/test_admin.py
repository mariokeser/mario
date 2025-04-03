from routers.admin import get_db, get_current_user
from fastapi import status
from .utils import *

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"title": "Learn FastAPI",
                                "description": "It is nice",
                                "priority": 5,
                                "complete": False,
                                "owner_id": 1, "id": 1}]
def test_admin_delete(test_todo):
    response = client.delete("/admin/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_admin_delete_not_found(test_todo):
    response = client.delete("/admin/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "todo not found"}
from fastapi import status
from .utils import *
from routers.users import get_current_user, get_db

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "mariocoding"
    assert response.json()["email"] == "mariocoding@email.com"
    assert response.json()["first_name"] == "Mario"
    assert response.json()["last_name"] =="Keser"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "(11)-111-1111"

def test_change_password_success(test_user):
    passwords = {"password":"testpassword","new_password": "newpassword"}
    response = client.put("/user/password", json=passwords)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_failed(test_user):
    passwords = {"password": "wrongpassword", "new_password": "newpassword"}
    response = client.put("/user/password", json=passwords)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "error on password change"}


def change_phone_number(test_user):
    response = client.put("/user/phonenumber", json={"phone_number": "099-111"})
    assert response.status_code == status.HTTP_204_NO_CONTENT




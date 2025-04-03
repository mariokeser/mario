from fastapi import HTTPException, status
from jose import jwt
from .utils import *
from datetime import timedelta
from routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user


app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    user = authenticate_user(test_user.username, "testpassword", db)
    assert user is not None
    assert user.username == test_user.username
    non_existing_user = authenticate_user("mario", "testpassword", db)
    assert non_existing_user is None
    wrong_password_user = authenticate_user(test_user.username, "wrongpassword", db)
    assert  wrong_password_user is None

def test_create_access_token(test_user):
    token = create_access_token(test_user.username, test_user.id, test_user.role,
                                timedelta(minutes=20))
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM,
                         options={"verify_signature": False})
    assert payload.get("sub") == test_user.username
    assert payload.get("id") == test_user.id
    assert payload.get("role") == test_user.role

def test_create_access_token2():
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(minutes=20)
    token = create_access_token(username, user_id, role, expires_delta)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],
                               options={"verify_signature": False})
    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": "testuser", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token=token)
    assert user == {"username": "testuser", "id": 1, "user_role": "admin"}

@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    encode = {"sub": "testuser", "id": 1}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not validate credentials"


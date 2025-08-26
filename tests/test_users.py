import pytest
from jose import jwt
from app import schemas
from app.config import settings

def test_root(client): 
    res = client.get("/")
    assert res.json().get("message") == "Hello world!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={
        "email":"acctest123@gmail.com" ,"password":"password123"})
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "acctest123@gmail.com"

def test_login(client,test_user):
    res = client.post("/login",data = {"username":test_user["email"] ,"password":test_user["password"]})
    token = schemas.Token(**res.json())
    payload = jwt.decode(token.access_token,settings.secret_key,algorithms = [settings.algorithm])
    id = payload.get("user_id")
    assert res.status_code == 200
    assert id == test_user["id"]
    assert token.token_type == "bearer"

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 401),  # 錯誤 Email
    ("acctest123@gmail.com", "wrongpassword", 401),  # 錯誤密碼
    ("wrongemail@gmail.com", "wrongpassword", 401),  # Email+密碼都錯
    (None, "password123", 422),  # 缺少 Email
    ("acctest123@gmail.com", None, 422),  # 缺少密碼
    (None, None, 422),  # 都缺
])

def test_login_invalid_cases(client,email,password,status_code):
    data = {}
    if email is not None:
        data["username"] = email
    if password is not None:
        data["password"] = password 
    res = client.post("/login", data = data)
    assert res.status_code == status_code

def test_get_user(authorized_client,test_user):
    res = authorized_client.get(f"/users/{test_user['id']}")
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 200
    assert new_user.id == test_user["id"]
    assert new_user.email == test_user["email"]

def test_unauthorized_user_get_user(client,test_user):
    res = client.get(f"/users/{test_user['id']}")
    assert res.status_code == 401

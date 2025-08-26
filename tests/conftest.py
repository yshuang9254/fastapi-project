from fastapi.testclient import TestClient
from app.main import app
from app import models,schemas,database
from .database import TestingSessionlocal,engine
from app.oauth2 import create_access_token
import pytest
from datetime import datetime, timedelta, timezone


@pytest.fixture(scope="function")
def session():
    models.Base.metadata.drop_all(bind = engine)
    models.Base.metadata.create_all(bind = engine)
    db = TestingSessionlocal()
    try:
        yield db 
    finally: 
        db.close()


@pytest.fixture
def client(session):
    def overrid_get_db():
        try:
            yield session 
        finally: 
            session.close()
    app.dependency_overrides[database.get_db] = overrid_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email":"acctest456@gmail.com" ,
                 "password":"password456"}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    new_user = {**schemas.UserOut(**res.json()).model_dump(), "password": user_data["password"]}
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email":"acctest789@gmail.com" ,
                 "password":"password789"}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    new_user = {**schemas.UserOut(**res.json()).model_dump(), "password": user_data["password"]}
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user["id"]})

@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_post(test_user,test_user2,session):
    now =datetime.now(timezone.utc)
    posts_data = [
        {"title":"first title","content":"first content","owner_id":test_user["id"],"created_at":now},
        {"title":"second title","content":"second content","owner_id":test_user["id"],"created_at":now + timedelta(seconds=1)},
        {"title":"third title","content":"third content","owner_id":test_user["id"],"created_at":now + timedelta(seconds=2)},
        {"title":"fourth title","content":"fourth content","owner_id":test_user2["id"],"created_at":now + timedelta(seconds=3)}
    ]
    posts = [models.Post(**post) for post in posts_data]
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts

@pytest.fixture
def test_vote(test_user,session,test_post):
    votes_data = {"post_id":test_post[3].id,"user_id":test_user["id"]}
    votes = models.Vote(**votes_data)
    session.add(votes)
    session.commit()
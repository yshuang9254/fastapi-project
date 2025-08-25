import pytest
from app import schemas
from app.config import settings

@pytest.mark.parametrize("title, content",
    [   ("第一篇貼文", "這是第一篇貼文的內容"),
    ("第二篇貼文", "這是第二篇貼文的內容"),
    ("第三篇貼文", "這是第三篇貼文的內容"),])
def test_create_post(authorized_client,test_user,title,content):
    post = {"title":title,"content":content}
    res = authorized_client.post("/posts/", json = post)
    new_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.owner_id == test_user["id"]
    assert new_post.published == True

def test_unauthorized_create_post(client):
    post = {"title":"unauthorized_create","content":"unauthorized_create"}
    res = client.post("/posts/", json = post)
    assert res.status_code == 401

def test_get_all_posts(authorized_client,test_post):
    res = authorized_client.get("/posts/")
    posts = [schemas.PostOut(**p) for p in res.json()]
    assert res.status_code == 200
    assert len(res.json()) == len(test_post)
    ids = [p.Post.id for p in posts]
    for post in test_post:
        assert post.id in ids

def test_unauthorized_user_get_all_posts(client,test_post):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_get_latest_post(authorized_client,test_post):
    res = authorized_client.get("/posts/latest")
    latest_post = schemas.PostOut(**res.json())
    tpost = max(test_post, key = lambda p:p.created_at)
    assert res.status_code == 200
    assert latest_post.Post.id == tpost.id
    assert latest_post.Post.title == tpost.title
    assert latest_post.Post.content == tpost.content

def test_unauthorized_get_latest_post(client,test_post):
    res = client.get("/posts/latest")
    assert res.status_code == 401

def test_get_latest_post_not_exist(authorized_client):
    res = authorized_client.get("/posts/latest")
    assert res.status_code == 404
    assert res.json().get("detail") == "沒有最新貼文"

def test_get_one_post(authorized_client,test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_post[0].id
    assert post.Post.title == test_post[0].title
    assert post.Post.content == test_post[0].content

def test_unauthorized_get_one_post(client,test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client,test_post):
    id = 9999999999999999999
    res = authorized_client.get(f"/posts/{id}")
    assert res.status_code == 404
    assert res.json().get("detail") == f"id為{id}的貼文不存在。"

def test_delete_post(authorized_client,test_post):
    res = authorized_client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 204    

def test_delete_other_user_post(authorized_client,test_post):
    res = authorized_client.delete(f"/posts/{test_post[3].id}")
    assert res.status_code == 403
    assert res.json().get("detail") == "Not authorized to perform requested action."

def test_unauthorized_delete_post(client,test_post):
    res = client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_delete_post_not_exist(authorized_client):
    id = 99999999999999999
    res = authorized_client.get(f"/posts/{id}")
    assert res.status_code == 404
    assert res.json().get("detail") == f"id為{id}的貼文不存在。"


def test_update_post(authorized_client,test_post):
    post = {"title":"更新貼文","content":"更新貼文"}
    res = authorized_client.put(f"/posts/{test_post[0].id}",json = post)
    update_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert update_post.title == post["title"]
    assert update_post.content == post["content"]

def test_update_other_user_post(authorized_client,test_post):
    post = {"title":"更新貼文","content":"更新貼文"}
    res = authorized_client.put(f"/posts/{test_post[3].id}",json = post)
    assert res.status_code == 403
    assert res.json().get("detail") == "Not authorized to perform requested action."

def test_unauthorized_update_post(client,test_post):
    post = {"title":"更新貼文","content":"更新貼文"}
    res = client.put(f"/posts/{test_post[0].id}",json = post)
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client):
    id = 99999999999999999
    post = {"title":"更新貼文","content":"更新貼文"}
    res = authorized_client.put(f"/posts/{id}",json = post)
    assert res.status_code == 404
    assert res.json().get("detail") == f"id為{id}的貼文不存在。"

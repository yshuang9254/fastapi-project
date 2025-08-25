def test_vote_on_post(authorized_client,test_post):
    vote = {"post_id":test_post[0].id,"dir":1}
    res = authorized_client.post("/vote/",json = vote)
    assert res.status_code == 201
    assert res.json().get("訊息") == "投票成功!"

def test_vote_twice_post(authorized_client,test_post,test_vote):
    vote = {"post_id":test_post[3].id,"dir":1}
    res = authorized_client.post("/vote/",json = vote)
    assert res.status_code == 409
    assert res.json().get("detail") == "已經投過囉~"

def test_delete_vote(authorized_client,test_post,test_vote):
    vote = {"post_id":test_post[3].id,"dir":0}
    res = authorized_client.post("/vote/",json = vote)
    assert res.status_code == 201
    assert res.json().get("訊息") == "已成功取消投票!"

def test_delete_vote_not_exist(authorized_client,test_post,test_vote):
    vote = {"post_id":test_post[0].id,"dir":0}
    res = authorized_client.post("/vote/",json = vote)
    assert res.status_code == 404
    assert res.json().get("detail") == "您尚未投過票喔!"

def test_delete_post_not_exist(authorized_client,test_post,test_vote):
    vote = {"post_id":99999999999999,"dir":0}
    res = authorized_client.post("/vote/",json = vote)
    assert res.status_code == 404
    assert res.json().get("detail") == "此貼文並不存在!"

def test_vote_unauthorized_user(client,test_post,test_vote):
    vote = {"post_id":test_post[0].id,"dir":1}
    res = client.post("/vote/",json = vote)
    assert res.status_code == 401


    
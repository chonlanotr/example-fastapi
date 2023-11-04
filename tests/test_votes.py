import pytest
from app import models
from app import schemas


@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    # print(f"*********************test_vote: {test_user['id']}")
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts, test_user):
    payload =  {"post_id": test_posts[3].id, "dir": 1}
    res = authorized_client.post(
        "/vote/", json=payload)
    assert res.status_code == 201

def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409
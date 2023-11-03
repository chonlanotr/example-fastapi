from app import schemas
from .database import client, session


def test_root(client):

# ทำแบบนี้ทำให้สามารถ access เข้า DB ได้ในตอน TEST เช่น
# def test_root(client, session):
#     session.query(models.P....)



    res = client.get("/")
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200


def test_create_user(client):

    # /users ต้องใส่เป็น /users/ ไม่งั้น pytest จะ error
    res = client.post("/users/", json={"email": "user5@example.com", "password": "string"})
    # print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "user5@example.com"
    assert res.status_code == 201
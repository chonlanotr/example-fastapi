from app import schemas
import pytest
from jose import jwt
from app.config import setting



def test_root(client):

# ทำแบบนี้ทำให้สามารถ access เข้า DB ได้ในตอน TEST เช่น
# def test_root(client, session):
#     session.query(models.P....)



    res = client.get("/")
    assert res.json().get('message') == 'Hello World successfully deployed from CI/CD pipeline.'
    assert res.status_code == 200


def test_create_user(client):
    # /users ต้องใส่เป็น /users/ ไม่งั้น pytest จะ error
    res = client.post("/users/", json={"email": "user5@example.com", "password": "string"})
    # print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "user5@example.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
        # เปลีย่นจาก json -> form data ใช้ data เลย
        res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})

        login_res = schemas.Token(**res.json())

        payload = jwt.decode(login_res.access_token, setting.secret_key, algorithms=[setting.algorithm])
        id = payload.get("user_id")
        assert id == test_user['id']
        assert login_res.token_type == "bearer"

        # print(res.json())
        assert res.status_code == 200





@pytest.mark.parametrize("email, password, status_code", [
          ('wrongemail@gamil.com', 'password123', 403),
          ('user@example.com', 'wrongPassword', 403),
          ('wrongemail@gmail.com', 'wrongPassword', 403),
          (None, "string", 422),
          ('user@example.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
     res = client.post("/login", data={"username": email, "password": password})

     assert res.status_code == status_code
    #  assert res.json().get('detail') == 'Invalid Credentials'
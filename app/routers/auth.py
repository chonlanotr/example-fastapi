from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # credential
    # {
    #     "username": "xxx"
    #     "password": "yyyy"
    # }

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    #username =
    #password =
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
    # if not user_credentials.password == user.password:
        # pass
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    print(user_credentials.password)
    print(user.password)
    # create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    # return token
    return{"access_token": access_token, "token_type": "bearer"}
    

    
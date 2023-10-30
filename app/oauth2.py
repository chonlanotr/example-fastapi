from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config  import setting

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')
#SECRET_KEY
#Algorithm
#Expriation time


# to get a string like this run:
# openssl rand -hex 32

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire })

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        # id เป็น str แต่จริงๆ เป็น integer !!!
        # token_data = schemas.TokenData(id=id)
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception

    return token_data

    
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials.", headers={"WWW-Authenitace": "Bearer"})


    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id ).first()


    return user

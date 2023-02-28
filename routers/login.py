from fastapi import APIRouter,status,HTTPException,Depends
from schemas import Login,TokenData
from database import get_db
import models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm



SECRET_KEY = "d4eddcb328090ff8b1bf1740f52336802bda5ed2264d5fd5c777476e595b3115"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES = 20
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    tags=["login"]
)

def generate_token(data:dict):
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES)
    to_encode.update({"exp":expires})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password,hash_password):
    return bcrypt_context.verify(plain_password,hash_password)

@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if not verify_password(request.password,user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    access_token = generate_token(
        data={"sub":user.username}
    )
    
    return {"access_token":access_token}
    

def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        token_data = TokenData(username=username)

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
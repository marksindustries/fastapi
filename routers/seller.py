from fastapi import APIRouter,HTTPException,Depends,status
from schemas import CreateSeller,Seller,TokenData
import models
from database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm


SECRET_KEY = "d4eddcb328090ff8b1bf1740f52336802bda5ed2264d5fd5c777476e595b3115"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES = 20
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(
    tags=["product"],
    prefix="/product"
)

def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        token_data = TokenData(username=username)

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hashed(password):
    return bcrypt_context.hash(password)

router = APIRouter(
    tags=["seller"],
    prefix="/seller"
)


@router.get("/getSeller")
async def getSeller(db:Session = Depends(get_db)):
    return db.query(models.Seller).all()



@router.get("/getSeller/{id}")
async def getSellerId(id:int,db:Session = Depends(get_db)):
    sel = db.query(models.Seller).filter(models.Seller.seller_unique_id == id).first()
    if sel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return sel
    


@router.post("/createSeller")
async def createSeller(seller:CreateSeller,db:Session = Depends(get_db),current_user:Seller = Depends(get_current_user)):
    sel_model = models.Seller()
    sel_model.seller_unique_id = seller.seller_unique_id
    sel_model.username = seller.username
    sel_model.email = seller.email
    sel_model.hashed_password = get_password_hashed(seller.hashed_password)

    db.add(sel_model)
    db.commit()

    return {
        HTTPException(status_code=status.HTTP_201_CREATED)
    }
    
@router.put("/updateSeller/{id}")
async def updateSeller(id:int,seller:CreateSeller,db:Session =Depends(get_db),current_user:Seller = Depends(get_current_user)):
    sel = db.query(models.Seller).filter(models.Seller.seller_unique_id == id).first()
    if sel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    sel_model = db.query(models.Seller).filter(models.Seller.seller_unique_id == id).first()

    sel_model.seller_unique_id = seller.seller_unique_id
    sel_model.username = seller.username
    sel_model.email = seller.email
    sel_model.hashed_password = get_password_hashed(seller.hashed_password)
    
    db.add(sel_model)
    db.commit()
    return {
         HTTPException(status_code=status.HTTP_201_CREATED)
    }

@router.delete("/deleteSeller")
async def updateSeller(id:int,db:Session =Depends(get_db),current_user:Seller = Depends(get_current_user)):
    sel = db.query(models.Seller).filter(models.Seller.seller_unique_id == id).first()
    if sel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    db.query(models.Seller).filter(models.Seller.seller_unique_id == id).delete()
    db.commit()

    return{
        HTTPException(status_code=status.HTTP_200_OK)
    }
from fastapi import APIRouter,HTTPException,Depends,status
from schemas import CreateProducts,Seller,TokenData
import models
from database import get_db
from sqlalchemy.orm import Session
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

@router.get("/getProduct")
async def getSeller(db:Session = Depends(get_db)):
    return db.query(models.Product).all()



@router.get("/getProduct/{id}")
async def getSellerId(id:int,db:Session = Depends(get_db)):
    sel = db.query(models.Product).filter(models.Product.id == id).first()
    if sel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return sel
    


@router.post("/createProduct")
async def createProduct(product:CreateProducts,db:Session = Depends(get_db),current_user:Seller = Depends(get_current_user)):
    pro_model = models.Product()
    pro_model.name = product.name
    pro_model.description = product.description
    pro_model.price = product.price
    pro_model.seller_id = product.seller_id
    

    db.add(pro_model)
    db.commit()

    return {
        HTTPException(status_code=status.HTTP_201_CREATED)
    }
    
@router.put("/updateProduct/{id}")
async def updateProduct(id:int,product:CreateProducts,db:Session = Depends(get_db),current_user:Seller = Depends(get_current_user)):
    pro = db.query(models.Product).filter(models.Product.id == id).first()
    if pro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    pro_model = db.query(models.Product).filter(models.Product.id == id).first()
    pro_model.name = product.name
    pro_model.description = product.description
    pro_model.price = product.price
    pro_model.seller_id = product.seller_id
    
    
    db.add(pro_model)
    db.commit()
    return {
         HTTPException(status_code=status.HTTP_201_CREATED)
    }

@router.delete("/deleteProduct")
async def updateProduct(id:int,db:Session =Depends(get_db),current_user:Seller = Depends(get_current_user)):
    pro = db.query(models.Product).filter(models.Product.id == id).first()
    if pro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    db.query(models.Product).filter(models.Product.id == id).delete()
    db.commit()

    return{
        HTTPException(status_code=status.HTTP_200_OK)
    }
from fastapi import APIRouter, Depends,  HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from models import Users
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


class ChangePassword(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

class PhoneNumber(BaseModel):
    phone_number: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(db:db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed")
    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/password/", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(db:db_dependency, user: user_dependency, change_password: ChangePassword):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed")
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt_context.verify(change_password.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="error on password change")
    user_model.hashed_password = bcrypt_context.hash(change_password.new_password)
    db.add(user_model)
    db.commit()

@router.put("/phonenumber", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(db:db_dependency, user: user_dependency, new_number: PhoneNumber):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed")
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_model.phone_number = new_number.phone_number
    db.add(user_model)
    db.commit()






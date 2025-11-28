from datetime import datetime, timedelta,timezone
from passlib.context import CryptContext 
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import databasemodels
from dbconnection import get_db

passwContext = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
oauth2Scheme = OAuth2PasswordBearer(tokenUrl = "/login")

key = "secret"
algorithm = "HS256"
accessTokenExpireTime = 60 

def hashPassw(password: str):
    return passwContext.hash(password)

def verifyPassword(toBeCheckedPassw: str, hashedPassw: str):
    return passwContext.verify(toBeCheckedPassw, hashedPassw)

def createToken(data: dict):
    toEncode = data.copy()
    toEncode["exp"] = timezone.utc() + timedelta(minutes = accessTokenExpireTime)
    return jwt.encode(toEncode, key, algorithm = algorithm)

def decodeAccessToken(token: str):
    return jwt.decode(token, key, algorithm = [algorithm])

def getCurrentUser(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    try:
        payload = decodeAccessToken(token)
        user_id: int = payload.get("user_id")
    except:
        raise HTTPException(status_code = 401, detail = "Invalid token.")
    
    user = db.query(databasemodels.User).filter(databasemodels.User.id == user_id).first()

    if user == None:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    return user

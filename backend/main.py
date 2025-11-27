from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Literal
from passlib.hash import pbkdf2_sha256

import models
import schemas
from database import engine, get_db

app = FastAPI()



@app.get("/")
def root():
    return {"message": "backend API working as intended !"}

@app.post("/users", response_model = schemas.UserResponse)
def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = models.User(
        email = user.email,
        password_hash = pbkdf2_sha256.hash(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.get("/users/{user_email}", response_model = schemas.UserResponse)
def getUser(user_email: str, db: Session = Depends(get_db)):
    pass

@app.delete("/users/{user_email}")
def delUser(user_email: str, db: Session = Depends(get_db)):
    pass

@app.post("/categories", response_model = schemas.CategoryResponse)
def createCategory(category: schemas.CategoryCreate, db: Session = Depends(get_db)):

    db_category = models.Category(
        name = category.name,
        type = category.type
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category

@app.get("/categories/{category_id}", response_model = schemas.CategoryResponse)
def getCategory(category_id: int, db: Session = Depends(get_db)):
    pass

@app.get("/categories/by-type/{category_type}", response_model = List[schemas.CategoryResponse])
def getCategory(category_type: Literal['income', 'expense'], db: Session = Depends(get_db)):
    pass

@app.delete("/categories/{category_id}")
def delCategory(category_id: int, db: Session = Depends(get_db)):
    pass

@app.post("/transactions", response_model = schemas.TransactionResponse)
def createTransaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):

    db_transaction = models.Transaction(
        name = transaction.name,
        category_id = transaction.category_id,
        amount = transaction.amount,
        transaction_date = transaction.transaction_date,
        description = transaction.description
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction

@app.get("/transactions/{transaction_id}", response_model = schemas.TransactionResponse)
def getTransaction(transaction_id: int, db: Session = Depends(get_db)):
    pass

if (__name__ == "__main__"):
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from sqlalchemy.orm import Session
from typing import List, Literal

import databasemodels
import pydanticmodels
import auth
from dbconnection import engine, get_db


app = FastAPI()

@app.get("/")
def root():
    return {"message": "backend API working as intended !"}

@app.post("/register", response_model = pydanticmodels.UserResponse)
def registerUser(user: pydanticmodels.UserCreate, db: Session = Depends(get_db)):

    if (db.query(databasemodels.User).filter(databasemodels.User.email == user.email).first() != None):
        raise HTTPException(status_code = 404, detail = "User already exists with that email.")
    
    dbuser = databasemodels.User(
        email = user.email,
        password_hash = auth.hashPassw(user.password)
    )

    db.add(dbuser)
    db.commit()
    db.refresh(dbuser)

    return dbuser

@app.post("/login")
def login(user: pydanticmodels.UserCreate, db: Session = Depends(get_db)):

    dbuser = db.query(databasemodels.User).filter(databasemodels.User.email == user.email).first()

    if not dbuser or auth.verifyPassword(user.password, dbuser.password_hash):
        raise HTTPException(status_code = 401, detail = "Incorrect login.")
    
    token =  auth.createToken(data = {"user_id": user.id})
    return {"access_token": token, "token_type" : "bearer"}

@app.delete("/user/by-email/{user_email}")
def delUser(currentUser = Depends(auth.getCurrentUser), db: Session = Depends(get_db)):

    user = db.query(databasemodels.User).filter(databasemodels.User.email == currentUser.email)

    if (user.first() == None):
        raise HTTPException(status_code = 404, detail = "User not found.")
    
    user.delete()
    db.commit()

@app.delete("/user/by-id/{user_id}")
def delUser(currentUser = Depends(auth.getCurrentUser), db: Session = Depends(get_db)):

    user = db.query(databasemodels.User).filter(databasemodels.User.id == currentUser.id)

    if (user.first() == None):
        raise HTTPException(status_code = 404, detail = "User not found.")

    user.delete()
    db.commit()

@app.post("/categories", response_model = pydanticmodels.CategoryResponse)
def createCategory(category: pydanticmodels.CategoryCreate, db: Session = Depends(get_db)):

    dbcategory = databasemodels.Category(
        name = category.name,
        type = category.type
    )

    db.add(dbcategory)
    db.commit()
    db.refresh(dbcategory)

    return dbcategory

@app.delete("/categories/{category_id}")
def delCategory(category_id: int, db: Session = Depends(get_db)):
    
    category = db.query(databasemodels.Category).filter(databasemodels.Category.id == category_id)

    if (category.first() == None):
        raise HTTPException(status_code = 404, detail = "Category not found.")
    
    category.delete()
    db.commit()


@app.get("/categories/by-id/{category_id}", response_model = pydanticmodels.CategoryResponse)
def getCategory(category_id: int, db: Session = Depends(get_db)):
    
    category = db.query(databasemodels.Category).filter(databasemodels.Category.id == category_id).first()

    if category == None:
        raise HTTPException(status_code = 404, detail = "Category not found.")
    
    return category

@app.get("/categories/by-type/{category_type}", response_model = List[pydanticmodels.CategoryResponse])
def getCategory(category_type: Literal['income', 'expense'], db: Session = Depends(get_db)):

    return db.query(databasemodels.Category).filter(databasemodels.Category.type == category_type).all()


@app.post("/transactions")
def createTransaction(transaction: pydanticmodels.TransactionCreate, db: Session = Depends(get_db)):

    dbtransaction = databasemodels.Transaction(
        name = transaction.name,
        category_id = transaction.category_id,
        amount = transaction.amount,
        transaction_date = transaction.transaction_date,
        description = transaction.description
    )

    db.add(dbtransaction)
    db.commit()
    db.refresh(dbtransaction)

    return dbtransaction

@app.delete("/transactions/by-id/{transaction_id}")
def delTransaction(transaction_id: int, db: Session = Depends(get_db)):
    
    transaction = db.query(databasemodels.Transaction).filter(databasemodels.Transaction.id == transaction_id)

    if (transaction.first() == None):
        raise HTTPException(status_code = 404, detail = "Transaction not found.")
    
    transaction.delete()
    db.commit()

@app.get("/transactions/by-id/{transaction_id}", response_model = pydanticmodels.TransactionResponse)
def getTransaction(transaction_id: int, db: Session = Depends(get_db)):
    
    transaction = db.query(databasemodels.Transaction).filter(databasemodels.Transaction.id == transaction_id).first()

    if transaction == None:
        raise HTTPException(status_code = 404, detail = "Transaction not found.")
    
    return transaction

if (__name__ == "__main__"):

    uvicorn.run(app, host = "0.0.0.0", port = 8000)
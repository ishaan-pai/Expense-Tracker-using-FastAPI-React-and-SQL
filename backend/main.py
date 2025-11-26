from fastapi import FastAPI
import mysql.connector

"""mysql connections"""
expensetrackerdb = mysql.connector.connect(
    host = "localhost",
    user = "expensetrackerpython",
    password = "1Sh44n@))%",
    database = 'expense_tracker'
)

"""mysql cursor init and fastapi app init"""
etdbcursor = expensetrackerdb.cursor()
app = FastAPI()

"""
3 different object classes to make:
User class

    features:
    - User authentification
    - Sign in
    - Create an account

    attributes:
    - user_id           INT
    - email             STR         [255 char limit]
    - password_hash     STR         [255 char limit]
    - created_at        TIMESTAMP

Category class
    
    features:
    - 

    attributes:
    - id                INT
    - user_id           INT         [tied to user class]
    - name              STR         [255 char limit]
    - type              ENUM        [either 'expense' or 'income']
    - created_at        TIMESTAMP

Transaction class
    
    features:
    - 

    attributes:
    - id                INT
    - user_id           INT
    - category_id       INT
    - name              STR         [255 char limit]
    - amount            DEC/FLT     [12 digits left of the decimal, 2 digits right of the decimal]
    - transaction_date  DATE
    - description       STR         [255 char limit]
    - created_at        TIMESTAMP

"""

class User():
    pass

class Category():
    pass

class Transaction():
    pass

@app.get("/")
def root():
    return {"Hello" : "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
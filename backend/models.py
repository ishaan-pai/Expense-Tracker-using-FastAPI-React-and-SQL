from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Enum, DECIMAL, Date
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable = False, primary_key = True, autoincrement = True)
    email = Column(String(255), nullable = False, unique = True)
    password_hash = Column(String(255), nullable = False)
    created_at = Column(DateTime, nullable = True, server_default = func.now())

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, nullable = False, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    name = Column(String(255), nullable = False)
    type = Column(Enum('income', 'expense', name = "category_type"), nullable = False)
    created_at = Column(DateTime, nullable = True, server_default = func.now())

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, nullable = False, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable = False)
    name = Column(String(255), nullable = False)
    amount = Column(DECIMAL(12,2), nullable = False)
    transaction_date = Column(Date, nullable = False)
    description = Column(String(255), nullable = True)
    created_at = Column(DateTime, nullable = True, server_default = func.now())
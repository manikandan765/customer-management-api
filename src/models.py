from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from .database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)  # Bonus: index on email
    phone = Column(String, nullable=True)
    city = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
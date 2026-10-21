from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import engine, get_db, Base
from . import models, schemas, dependencies

# Create tables (fallback, though Alembic is the primary method)
Base.metadata.create_all(bind=engine)

# THIS IS THE LINE UVICORN IS LOOKING FOR:
app = FastAPI(title="Customer Management API")

# --- Task 1: Health Check ---
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# --- Task 2: CRUD Endpoints ---

# 1. POST /customers
@app.post("/customers", response_model=schemas.CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer: schemas.CustomerCreate, 
    db: Session = Depends(get_db), 
    api_key: str = Depends(dependencies.verify_api_key)
):
    db_customer = models.Customer(**customer.model_dump())
    try:
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

# 2. GET /customers (with Pagination & Bonus Search)
@app.get("/customers", response_model=list[schemas.CustomerOut])
def get_customers(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str = Query(None, description="Search customers by name"),
    db: Session = Depends(get_db),
    api_key: str = Depends(dependencies.verify_api_key)
):
    query = db.query(models.Customer)
    
    # Bonus: Search by name (case-insensitive)
    if search:
        query = query.filter(models.Customer.name.ilike(f"%{search}%"))
        
    # Pagination
    offset = (page - 1) * per_page
    return query.offset(offset).limit(per_page).all()

# 3. GET /customers/{id}
@app.get("/customers/{customer_id}", response_model=schemas.CustomerOut)
def get_customer(
    customer_id: int, 
    db: Session = Depends(get_db), 
    api_key: str = Depends(dependencies.verify_api_key)
):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

# 4. PUT /customers/{id}
@app.put("/customers/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(
    customer_id: int, 
    customer_update: schemas.CustomerUpdate, 
    db: Session = Depends(get_db), 
    api_key: str = Depends(dependencies.verify_api_key)
):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    update_data = customer_update.model_dump(exclude_unset=True)
    try:
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

# 5. DELETE /customers/{id}
@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int, 
    db: Session = Depends(get_db), 
    api_key: str = Depends(dependencies.verify_api_key)
):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    db.delete(db_customer)
    db.commit()
    return None
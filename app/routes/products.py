from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db



router = APIRouter()

@router.get("/products", response_model=list[schemas.ProductOut])
def all_products(db: Session = Depends(get_db)):
    return db.query(models.Products).all()

@router.get("/products/{product_id}", response_model=schemas.ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail=f"Product Not Found with {product_id}")
    return product

# @router.get("/products/{name}", response_model=schemas.ProductOut)
# def get_product_by_name(name:str, db: Session=Depends(get_db)):


@router.post("/add_product", response_model=schemas.ProductOut)
def add_new_product(product: schemas.ProductCreate, db: Session=Depends(get_db)):
    new_product = models.Products(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/updateProduct/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int,
    updated_product: schemas.ProductCreate,  # Or better, a separate Update schema
    db: Session = Depends(get_db)
):
    product = db.query(models.Products).get(product_id)

    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    for field, value in updated_product.dict().items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product

@router.delete("/deleteProduct/{product_id}")
def delete_by_id(product_id: int, db: Session=Depends(get_db)):
    product = db.query(models.Products).get(product_id)

    if not product:
        raise HTTPException(status_code=404, detail=f"oriduct with id {product_id} not found")      
    
    db.delete(product)      
    db.commit()
    return {"message": f"Product with id {product_id} deleted successfully"}    

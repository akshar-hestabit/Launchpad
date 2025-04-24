from fastapi import APIRouter, Depends
from fastapi import APIRouter, Depends
from app import dependencies, models

router = APIRouter()

@router.get("/dashboard")
def get_dashboard(user: models.User = Depends(dependencies.get_current_user)):
    if user.role == "admin":
        return {"message": "Welcome Admin!"}
    elif user.role == "vendor":
        return {"message": "Vendor Dashboard"}
    else:
        return {"message": "Customer Area"}

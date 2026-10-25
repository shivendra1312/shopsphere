from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, UserRole
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, "ADMIN"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """Admin only: Get dashboard statistics"""
    return dashboard_service.get_dashboard_stats(db)

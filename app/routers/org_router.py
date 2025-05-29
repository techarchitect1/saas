from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.org_schemas import OrganizationCreate, OrganizationRead
from app.services import org_service
from app.models.central_models import User # Import User model
from app.core.security import get_current_active_user # Import the dependency

router = APIRouter()

@router.post("/", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
def create_new_organization(
    org_in: OrganizationCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # Protect endpoint
):
    organization = org_service.create_organization(db=db, org_in=org_in, owner=current_user)
    return organization

@router.get("/", response_model=List[OrganizationRead])
def read_user_organizations(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # Protect endpoint
):
    organizations = org_service.get_user_organizations(db=db, owner_id=current_user.id)
    return organizations

@router.get("/{org_id}", response_model=OrganizationRead)
def read_specific_organization(
    org_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # Protect endpoint
):
    organization = org_service.get_organization_by_id(db=db, org_id=org_id, owner_id=current_user.id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found or not owned by user")
    return organization

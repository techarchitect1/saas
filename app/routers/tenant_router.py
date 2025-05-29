from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.tenant_schemas import TenantCreate, TenantRead
from app.services import tenant_service, org_service # org_service for checking org ownership
from app.models.central_models import User # Import User model
from app.core.security import get_current_active_user # Import the dependency
import logging # Import logging

router = APIRouter()
logger = logging.getLogger(__name__) # Get logger for this module

@router.post(
    "/organizations/{org_id}/tenants/", 
    response_model=TenantRead, 
    status_code=status.HTTP_201_CREATED
)
def create_new_tenant(
    tenant_in: TenantCreate,
    org_id: int = Path(..., title="The ID of the organization to create the tenant under"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Verify organization exists and is owned by the current user
    organization = org_service.get_organization_by_id(db=db, org_id=org_id, owner_id=current_user.id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found or you do not have permission to access it."
        )
    
    try:
        tenant = tenant_service.create_tenant(db=db, tenant_in=tenant_in, organization=organization)
        return tenant
    except ValueError as ve: # Catch specific error for duplicate subdomain
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except HTTPException as http_exc: # Re-raise HTTPExceptions from service layer
        raise http_exc
    except Exception as e: # Catch broader exceptions from DB creation or other unexpected issues
        # logger.error(f"Tenant creation failed for org_id {org_id} by user {current_user.email}: {e}", exc_info=True) # Commented out as per prompt
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Tenant creation failed due to an unexpected error.")


@router.get(
    "/organizations/{org_id}/tenants/", 
    response_model=List[TenantRead]
)
def read_organization_tenants(
    org_id: int = Path(..., title="The ID of the organization to list tenants for"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # First, check if the organization exists and is owned by the user.
    # This is a more explicit check before calling the tenant service.
    organization = org_service.get_organization_by_id(db=db, org_id=org_id, owner_id=current_user.id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found or you do not have permission to access it."
        )
        
    # Service function get_tenants_for_organization already checks ownership but might return [] if org not found.
    # The check above makes the 404 for the organization explicit.
    tenants = tenant_service.get_tenants_for_organization(db=db, organization_id=org_id, owner_id=current_user.id)
    return tenants

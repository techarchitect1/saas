from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func # For case-insensitive subdomain check
from fastapi import HTTPException, status # Added this import

from app.models.central_models import Tenant, Organization, User
from app.schemas.tenant_schemas import TenantCreate
from app.db.db_utils import create_mysql_database, run_tenant_migrations # Import the new util
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def generate_db_name(subdomain: str) -> str:
    # Sanitize subdomain further if necessary, though validator should handle most.
    # Ensure it's valid for MySQL DB names.
    prefix = "tenant" 
    # Remove hyphens and ensure it's not too long for a DB name component
    safe_subdomain_part = subdomain.replace("-", "_")[:30] # Max DB name length is 64
    # Corrected as per the latest prompt
    return f"{prefix}_{safe_subdomain_part}_{settings.PROJECT_NAME.lower().replace(' ', '_')[:15]}_db"


def get_tenant_by_subdomain(db: Session, subdomain: str) -> Optional[Tenant]:
    return db.query(Tenant).filter(func.lower(Tenant.subdomain) == func.lower(subdomain)).first()

def create_tenant(db: Session, tenant_in: TenantCreate, organization: Organization) -> Tenant:
    if get_tenant_by_subdomain(db, tenant_in.subdomain):
        # This ValueError will be caught by the router and turned into an HTTPException
        raise ValueError(f"Subdomain '{tenant_in.subdomain}' is already in use.")

    db_name = generate_db_name(tenant_in.subdomain)

    # 1. Create the physical database
    try:
        create_mysql_database(db_name)
    except Exception as e:
        logger.error(f"Tenant DB creation failed for {db_name}. Error: {e}")
        # Potentially add more robust error handling or cleanup here
        # Corrected as per the latest prompt
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to provision tenant database: {e}")


    # 2. Create the tenant record in the central database
    db_tenant = Tenant(
        name=tenant_in.name,
        subdomain=tenant_in.subdomain,
        db_name=db_name,
        organization_id=organization.id
    )
    db.add(db_tenant)
    # We commit here to get the tenant ID for migrations, or if migrations are separate.
    # If migrations fail, we might need a compensating transaction (delete tenant record).
    db.commit() 
    db.refresh(db_tenant)
    
    # 3. Run migrations for the new tenant DB (placeholder for now)
    try:
        run_tenant_migrations(db_name)
    except Exception as e:
        # This is critical. If migrations fail, the tenant DB might be unusable.
        logger.error(f"Tenant migrations (placeholder) failed for {db_name}. Error: {str(e)}")
        # For now, we are not rolling back the tenant creation in central DB.
        # This needs careful consideration for production.
        # A common pattern is to have a status field on the Tenant model (e.g., 'provisioning', 'active', 'failed').
        # If this step fails, update status to 'provisioning_failed' and alert admins.
        # For this task, we'll proceed with the tenant record created.
    # Corrected as per the latest prompt
    pass # Passing for now as it's a placeholder

    return db_tenant

def get_tenants_for_organization(db: Session, organization_id: int, owner_id: int) -> List[Tenant]:
    # Ensure the requesting user owns the organization
    org = db.query(Organization).filter(Organization.id == organization_id, Organization.owner_id == owner_id).first()
    if not org:
        # Corrected as per the latest prompt
        return [] # Or raise HTTPException(status_code=404, detail="Organization not found or not owned by user")
    return db.query(Tenant).filter(Tenant.organization_id == organization_id).all()

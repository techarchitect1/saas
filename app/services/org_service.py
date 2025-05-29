from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.central_models import Organization, User
from app.schemas.org_schemas import OrganizationCreate

def create_organization(db: Session, org_in: OrganizationCreate, owner: User) -> Organization:
    db_org = Organization(**org_in.model_dump(), owner_id=owner.id)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def get_user_organizations(db: Session, owner_id: int) -> List[Organization]:
    return db.query(Organization).filter(Organization.owner_id == owner_id).all()

def get_organization_by_id(db: Session, org_id: int, owner_id: int) -> Optional[Organization]:
    return db.query(Organization).filter(Organization.id == org_id, Organization.owner_id == owner_id).first()

from pydantic import BaseModel, validator
import re

class TenantBase(BaseModel):
    name: str
    subdomain: str

    @validator('subdomain')
    def validate_subdomain(cls, v):
        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", v):
            raise ValueError('Subdomain must be lowercase alphanumeric with optional hyphens, and cannot start/end with a hyphen.')
        if len(v) < 3 or len(v) > 63: # Typical length limits
            raise ValueError('Subdomain must be between 3 and 63 characters long.')
        return v

class TenantCreate(TenantBase):
    pass

class TenantRead(TenantBase):
    id: int
    db_name: str
    organization_id: int

    class Config:
        from_attributes = True

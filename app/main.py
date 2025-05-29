from fastapi import FastAPI
from app.core.config import settings # Ensure settings is imported if used directly
from app.routers import auth_router # Import the auth router
from app.routers import org_router # Import the org router
from app.routers import tenant_router # Import the tenant router

app = FastAPI(
    title=settings.PROJECT_NAME,
    # Add other FastAPI parameters like version, description if needed
)

# Include routers
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
app.include_router(org_router.router, prefix="/organizations", tags=["Organizations"])
app.include_router(tenant_router.router, tags=["Tenants"]) # Add this line (prefix is part of endpoint paths)

@app.get("/")
async def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

# Other global configurations or event handlers can go here

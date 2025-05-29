from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Multi-Tenant SaaS"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+mysqlclient://user:password@localhost/saas_central_db")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-please-change")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MYSQL_ROOT_USER: str = os.getenv("MYSQL_ROOT_USER", "root")
    MYSQL_ROOT_PASSWORD: str = os.getenv("MYSQL_ROOT_PASSWORD", "rootpassword")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", 3306)) # Ensure port is int

    class Config:
        env_file = ".env"
        extra = 'ignore'

settings = Settings()

import sqlalchemy
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def create_mysql_database(db_name: str):
    '''
    Creates a new MySQL database.
    Uses root credentials from settings to connect to the MySQL server (not a specific DB).
    '''
    try:
        # Connect to MySQL server (without specifying a database initially)
        engine = sqlalchemy.create_engine(
            f"mysql+mysqlclient://{settings.MYSQL_ROOT_USER}:{settings.MYSQL_ROOT_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}",
            isolation_level="AUTOCOMMIT" # Autocommit needed for CREATE DATABASE
        )
        with engine.connect() as connection:
            # Check if database exists
            result = connection.execute(sqlalchemy.text(f"SHOW DATABASES LIKE '{db_name}'"))
            if result.fetchone():
                logger.warning(f"Database {db_name} already exists.")
                # Depending on policy, could raise error or return success
                # For now, let's allow it to proceed if it exists, assuming it's benign or for idempotency
                return True 
            
            # Create the database
            connection.execute(sqlalchemy.text(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            logger.info(f"Successfully created database: {db_name}")
        return True
    except sqlalchemy.exc.SQLAlchemyError as e:
        logger.error(f"Error creating database {db_name}: {e}")
        raise Exception(f"Could not create database {db_name}: {e}") # Re-raise to be caught by service layer

def run_tenant_migrations(db_name: str):
    '''
    Placeholder for running Alembic migrations on the newly created tenant database.
    This will be fully implemented in a later step (Phase 2, Step 7) when tenant models and tenant-specific Alembic are set up.
    For now, it can just log or do nothing.
    '''
    logger.info(f"Placeholder: Tenant migrations would run for database: {db_name}")
    # Example of what might go here later:
    # alembic_cfg = Config("alembic_tenant.ini") # Assuming a separate ini for tenant migrations
    # alembic_cfg.set_main_option("sqlalchemy.url", f"mysql+mysqlclient://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}/{db_name}")
    # command.upgrade(alembic_cfg, "head")
    pass

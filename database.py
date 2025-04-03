from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



URL = "postgresql://database_deployment_user:sQVwuvwqQO5Y8SZ8ev1xedN5pnzzmq1f@dpg-cvars6qj1k6c7390nheg-a.frankfurt-postgres.render.com/database_deployment"
engine = create_engine(URL)
Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False, autocommit= False, bind=engine)
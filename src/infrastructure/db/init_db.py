from .database import Base, engine
from .models.models import Idea, WorkItem # Ensure models are imported and known to Base

def init_db():
    """
    Initializes the database by creating all tables defined in the models.
    """
    print("Creating database tables...")
    print(f"Tables registered with Base.metadata: {Base.metadata.tables.keys()}") # Debug print
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()

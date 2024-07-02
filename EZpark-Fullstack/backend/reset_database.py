# reset_database.py

from models import Base, engine

# Drop all tables
Base.metadata.drop_all(bind=engine)

# Recreate all tables
Base.metadata.create_all(bind=engine)

print("Database has been reset.")

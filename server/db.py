import os
from sqlalchemy import create_engine, text

# Get the database URL from environment variables
db_url = os.environ.get("DATABASE_URL")

# Create a new engine instance
engine = create_engine(db_url)

def create_table():
    """Creates the tasks table if it doesn't exist."""
    with engine.connect() as conn:
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """))
            conn.commit()
            print("Table 'tasks' created successfully (if it didn't exist).")
        except Exception as e:
            print(f"An error occurred while creating the table: {e}")

if __name__ == "__main__":
    create_table()

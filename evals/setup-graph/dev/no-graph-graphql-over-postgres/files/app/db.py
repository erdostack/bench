import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get("DATABASE_URL", "postgresql+psycopg://tally@localhost:5432/tally"))
Session = sessionmaker(engine, expire_on_commit=False)

"""
============================================================
DATABASE CONNECTION — db.py
============================================================
Responsibility: Creates the SQLAlchemy engine and session that
the rest of the pipeline uses to talk to reddit.db.

This is plumbing, not business logic — you only need to
understand it, not necessarily write all of it from scratch.
Some of it is already done for you. Read the TODOs carefully.
============================================================
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pipeline.models import Base

# The SQLite database file lives at the project root, shared
# between the pipeline and the backend.
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "reddit.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# The engine is the entry point to the database.
# echo=False keeps the console quiet; set True for debugging SQL.
engine = create_engine(DATABASE_URL, echo=False)

# A configured "Session" class. Each instance is a single
# conversation with the database (think: one transaction).
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """
    Creates all tables defined in models.py if they don't already exist.
    Safe to call multiple times — it won't duplicate or wipe tables.

    TODO:
        - Call Base.metadata.create_all(bind=engine)
    """
    Base.metadata.create_all(bind=engine)

def get_session():
    """
    Returns a new SQLAlchemy session for talking to the database.
    Caller is responsible for closing it (or use it in a `with` block
    if you upgrade to that pattern later).

    Returns:
        Session: A new SQLAlchemy session instance.

    TODO:
        - Return SessionLocal()
    """
    return SessionLocal()
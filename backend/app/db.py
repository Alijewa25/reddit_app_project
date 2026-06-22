"""
============================================================
DATABASE CONNECTION — db.py  (Backend)
============================================================
Responsibility: Creates the SQLAlchemy engine and session that the
Flask API uses to READ from lobsters.db.

The backend NEVER writes to the database — that's the Data Engineer's
pipeline's job. The backend only queries (reads) data.

This file points at the SAME lobsters.db file as the pipeline.
============================================================
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Same database file as the pipeline — project root.
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "lobsters.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def get_session():
    """
    Returns a new SQLAlchemy session for querying the database.
    Caller is responsible for closing it when done.

    Returns:
        Session: A new SQLAlchemy session instance.

    TODO:
        - Return SessionLocal()
    """
    return SessionLocal()
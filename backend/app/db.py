"""
============================================================
DATABASE CONNECTION — db.py  (Backend)
============================================================
Responsibility: Creates the SQLAlchemy engine and session that the
Flask API uses to READ from reddit.db.

The backend NEVER writes to the database — that's the Data Engineer's
pipeline's job. The backend only queries (reads) data.

This file points at the SAME reddit.db file as the pipeline.
============================================================
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Same database file as the pipeline — project root.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'lobsters.db')}"

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
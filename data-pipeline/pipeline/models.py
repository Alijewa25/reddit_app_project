"""
============================================================
SHARED DATABASE MODELS — models.py
============================================================
This file defines the database schema using SQLAlchemy ORM.

WHO USES THIS FILE:
  - The Data Engineer imports it to know what columns to fill in
    when saving posts to the database.
  - The Backend Developer imports it to query posts out of the
    database for the API.

This file is SHARED — both the pipeline and the backend point
at the same models.py and the same reddit.db SQLite file.

============================================================
STUDENT TASK (Data Engineer leads this, whole team reviews it)
============================================================
Define ONE table: `posts`

Columns required:
  id            INTEGER, primary key, auto-increment
  post_id       STRING, unique, NOT NULL   (Reddit's own id, e.g. "t3_abc123")
  title         STRING, NOT NULL
  author        STRING, NOT NULL
  score         INTEGER, NOT NULL          (upvotes)
  num_comments  INTEGER, NOT NULL
  url           STRING, NOT NULL           (link the post points to)
  permalink     STRING, NOT NULL           (link to the comments page on reddit.com)
  created_utc   FLOAT, NOT NULL            (original Reddit post timestamp)
  fetched_at    DATETIME, NOT NULL         (when OUR pipeline fetched this row)

Why both created_utc and fetched_at?
  - created_utc tells us when the post was made on Reddit.
  - fetched_at tells us when OUR pipeline pulled it in — useful for
    debugging and for knowing how fresh the data is.

TODO:
  - Define a class `Post(Base)` with `__tablename__ = "posts"`
  - Add a Column for each field listed above with the correct type
  - Add `unique=True, nullable=False` to post_id
  - Add `nullable=False` to all other required fields
  - (Optional but recommended) implement `__repr__` for easier debugging
============================================================
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    # TODO: id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, primary_key=True, autoincrement=True)


    # TODO: post_id = Column(String, unique=True, nullable=False)
    post_id = Column(String, unique=True, nullable=False)

    # TODO: title = Column(String, nullable=False)
    title = Column(String, nullable=False)

    # TODO: author = Column(String, nullable=False)
    author = Column(String, nullable=False)

    # TODO: score = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)

    # TODO: num_comments = Column(Integer, nullable=False)
    num_comments = Column(Integer, nullable=False)

    # TODO: url = Column(String, nullable=False)
    url = Column(String, nullable=False)

    # TODO: permalink = Column(String, nullable=False)
    permalink = Column(String, nullable=False)

    # TODO: created_utc = Column(Float, nullable=False)
    created_utc = Column(Float, nullable=False)

    # TODO: fetched_at = Column(DateTime, nullable=False)
    fetched_at = Column(DateTime, nullable=False)
    
    def __repr__(self):
        # TODO: return something like:
        # f"<Post id={self.id} title={self.title[:30]!r} score={self.score}>"
        return f"<Post id={self.id} title={self.title[:30]!r} score={self.score}>"

"""
============================================================
SHARED DATABASE MODELS — models.py  (Backend copy)
============================================================
⚠️  IMPORTANT: This file MUST define the exact same schema as
data-pipeline/pipeline/models.py — they both describe the SAME
table in the SAME reddit.db file.

In a bigger real-world project, this duplication would usually be
solved by putting models.py in a shared package both services
install. For this student project, we keep two copies side by side
so each team (data engineer vs backend) has the file inside their
own folder — but the Data Engineer's version is the "source of
truth". If you change one, change the other to match!

============================================================
STUDENT TASK (Backend Developer)
============================================================
This should be IDENTICAL to data-pipeline/pipeline/models.py.
Coordinate with your Data Engineer teammate — once they've defined
the schema, copy it here exactly.

TODO: Define the same `Post` class with `__tablename__ = "posts"`
and all 10 columns (id, post_id, title, author, score, num_comments,
url, permalink, created_utc, fetched_at) — see the pipeline's
models.py for the full field list and types.
============================================================
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    num_comments = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    permalink = Column(String, nullable=False)
    created_utc = Column(Float, nullable=False)
    fetched_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Post id={self.id} title={self.title[:30]!r} score={self.score}>"

    def to_dict(self) -> dict:
        """
        Converts this Post row into a plain dict — useful for turning
        SQLAlchemy objects into JSON later in the API layer.

        Returns:
            dict: All fields as plain Python types.

        TODO:
            Return a dict with these keys, pulling values from self:
                {
                    "id": self.id,
                    "post_id": self.post_id,
                    "title": self.title,
                    "author": self.author,
                    "score": self.score,
                    "num_comments": self.num_comments,
                    "url": self.url,
                    "permalink": self.permalink,
                    "created_utc": self.created_utc,
                    "fetched_at": self.fetched_at.isoformat() if self.fetched_at else None,
                }

            Note: fetched_at is a datetime object — JSON can't serialize
            datetimes directly, so we convert it to a string with
            .isoformat() (or None if it's missing).
        """
        return {
            "id": self.id,
            "post_id": self.post_id,
            "title": self.title,
            "author": self.author,
            "score": self.score,
            "num_comments": self.num_comments,
            "url": self.url,
            "permalink": self.permalink,
            "created_utc": self.created_utc,
            "fetched_at": self.fetched_at.isoformat() if self.fetched_at else None,
        }

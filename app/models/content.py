from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=True) # Optional title
    body = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    sentiment = Column(String, nullable=True) # Positive, Negative, Neutral
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", backref="contents")

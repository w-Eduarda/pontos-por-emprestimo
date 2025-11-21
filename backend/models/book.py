from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String)
    condition = Column(String, default="Bom")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    available = Column(Boolean, default=True)

    owner = relationship("User", back_populates="owned_books")

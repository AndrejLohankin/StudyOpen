from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from .database import Base

class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    author = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="open")

    user_id = Column(Integer, ForeignKey("users.id"))

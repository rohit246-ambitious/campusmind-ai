from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum


class UserRole(str, Enum):
    super_admin = "super_admin"
    college_admin = "college_admin"
    teacher = "teacher"
    student = "student"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    role = Column(String, default="student")

    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=True)

    college = relationship("College", back_populates="users")

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    # ⭐ Tenant Ownership
    college_id = Column(Integer, ForeignKey("colleges.id"))

    college = relationship("College")

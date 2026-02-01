from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from db.db_config import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)

    # один до багатьох
    sales = relationship("SalesRecord", back_populates="product")
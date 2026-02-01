from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.db_config import Base

class SalesRecord(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity_ordered = Column(Integer)
    order_date = Column(DateTime)

    # зворотній зв'язок
    product = relationship("Product", back_populates="sales")
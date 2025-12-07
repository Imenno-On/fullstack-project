from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.db.base import Base

class Test(Base):
    __tablename__ = "tests"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String, nullable=False)
    description = Column(Text)
    owner_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
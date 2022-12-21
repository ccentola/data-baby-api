from .database import Base
from sqlalchemy import Column, Integer, String, Date, Time, func, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import relationship


class Bottle(Base):
    __tablename__ = "bottles"

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date, nullable=False, server_default=text("now()"))
    time = Column(Time, nullable=False, server_default=func.now())
    amount = Column(Integer, nullable=False)
    brand = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    created_on = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    # child_id = Column(
    #     Integer, ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    # )
    # child = relationship("Child")
    parent_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    parent = relationship("User")


class Diaper(Base):
    __tablename__ = "diaper"
    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date, nullable=False, server_default=text("now()"))
    time = Column(Time, nullable=False, server_default=func.now())
    soil_type = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    created_on = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    # child_id = Column(
    #     Integer, ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    # )
    # child = relationship("Child")
    parent_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    parent = relationship("User")


class Child(Base):
    __tablename__ = "children"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False, server_default=text("now()"))
    parent_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    parent = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_on = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

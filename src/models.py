from sqlalchemy.orm import relationship

from src.database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, text, Integer, ForeignKey, Date


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    verified = Column(Boolean, nullable=False, server_default='False')
    verification_code = Column(String, nullable=True, unique=True)
    role = Column(String, server_default='user', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class Position(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    company = Column(String, nullable=False)
    job_text = Column(String, nullable=False)
    salary = Column(String, nullable=True)
    status = Column(String, nullable=False, default="Created")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    created_by_id = Column(Integer, ForeignKey("users.id"))

    # TO DO
    candidates = relationship("Candidate", back_populates="position")


class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    github_link = Column(String, nullable=True)
    linkedin_link = Column(String, nullable=True)
    career_site = Column(String, nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id"))
    date_applied = Column(Date, nullable=False, server_default=text("now()"))
    status = Column(String, nullable=False, default="Added")
    created_by_id = Column(Integer, ForeignKey("users.id"))

    position = relationship("Position", back_populates="candidates")


class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    text = Column(String, nullable=True)
    time_start = Column(TIMESTAMP(timezone=True), nullable=False)
    time_end = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(String, nullable=False, default="Planned")
    created_by_id = Column(Integer, ForeignKey("users.id"))

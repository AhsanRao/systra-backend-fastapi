# app/models/template.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Template(Base):
    __tablename__ = "templates"

    templateId = Column(Integer, primary_key=True, index=True)
    templateName = Column(String(100), nullable=False)

    wbs_list = relationship("Wbs", back_populates="template")
    activities = relationship("Activity", back_populates="template")
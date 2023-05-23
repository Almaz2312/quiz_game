from sqlalchemy import Column, String, Integer, Date

from core.base_class import Base


class Quiz(Base):
    id = Column(Integer, primary_key=True, index=True)
    question_number = Column(Integer, unique=True)
    question = Column(String)
    answer = Column(String)
    created_at = Column(Date)

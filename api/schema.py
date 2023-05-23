import datetime

from pydantic import BaseModel


class QuizSchema(BaseModel):
    question_number: int
    question: str
    answer: str
    created_at: datetime.date

    class Config:
        orm_mode = True

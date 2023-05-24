from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.schema import QuizSchema
from api.utils import process_question_list
from core.sessions import get_db

api_router = APIRouter()


@api_router.post("/quiz/question_num/", response_model=QuizSchema | list)
async def quiz_count(question_num: int, db: Session = Depends(get_db)):
    last_saved_quiz = await process_question_list(
        db=db, question_num=question_num
    )
    if not last_saved_quiz:
        return []
    return last_saved_quiz

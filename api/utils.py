import datetime
import requests
from sqlalchemy.orm import Session

from core.config import settings
from api.schema import QuizSchema
from api.models import Quiz


async def get_date(dt: str):
    formatted_dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")
    return formatted_dt.date()


async def fetch_questions(question_num: int):
    params = {"count": question_num}
    response = requests.get(settings.QUIZ_URL, params=params)
    return response.json()


async def check_save_questions(questions: list, db: Session):
    counter = 0
    question_ids = [question["id"] for question in questions]
    existing_questions_ids = db.query(Quiz.question_number).filter(Quiz.question_number.in_(question_ids)).all()
    existing_questions_ids = [qid for qid, in existing_questions_ids]

    questions_to_save = []
    for question in questions:
        if question["id"] in existing_questions_ids:
            counter += 1
        else:
            questions_to_save.append(Quiz(
                question_number=question["id"],
                question=question["question"],
                answer=question["answer"],
                created_at=await get_date(question["created_at"])
            ))

    if questions_to_save:
        db.bulk_save_objects(questions_to_save)
        db.commit()

    return counter


async def process_question_list(db: Session, question_num: int):
    last_save_question = db.query(Quiz).order_by(Quiz.id.desc()).first()
    questions_num_to_post = question_num
    while questions_num_to_post > 0:
        questions = await fetch_questions(question_num)
        questions_num_to_post = await check_save_questions(questions, db)
    return last_save_question

from __future__ import annotations
from typing import List, Optional
from sqlalchemy.engine import Engine
from sqlmodel import Session, select
from ..domain.models import Answer, Attempt, Question

class BaseDAO:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
    def session(self) -> Session:
        return Session(self.engine)
    
class QuestionDAO(BaseDAO):
    def list_all(self) -> List[Question]:
        with self.session() as session:
            return list(session.exec(select(Question).order_by(Question.id)).all())

    def get_by_id(self, question_id: int) -> Optional[Question]:
        with self.session() as session:
            return session.get(Question, question_id)


class AttemptDAO(BaseDAO):
    def create(self, attempt: Attempt) -> Attempt:
        with self.session() as session:
            session.add(attempt)
            session.commit()
            session.refresh(attempt)
        return attempt

    def list_recent(self, limit: int = 200) -> List[Attempt]:
        with self.session() as session:
            statement = select(Attempt).order_by(Attempt.created_at.desc()).limit(limit)
            return list(session.exec(statement).all())

    def get_with_items(self, attempt_id: int) -> Optional[Attempt]:
        with self.session() as session:
            attempt = session.get(Attempt, attempt_id)
            if not attempt:
                return None
            attemptList = list(attempt.answers)
            for answer in attempt.answers:
                attemptList = answer.question
            return attempt

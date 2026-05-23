from __future__ import annotations
from typing import List, Optional
from ..domain.models import Question
from ..data_access.dao import QuestionDAO

class QuestionService:
    def __init__(self, question_dao: QuestionDAO) -> None:
        self.question_dao = question_dao
    def list_questions(self) -> List[Question]:
        return self.question_dao.list_all()
    def get_by_id(self, question_id: int) -> Optional[Question]:
        return self.question_dao.get_by_id(question_id)

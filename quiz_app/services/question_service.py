from __future__ import annotations
from typing import List, Optional
from ..data_access.dao import QuestionDAO
from ..domain.models import Question

class QuestionService:

    def __init__(self, question_dao: QuestionDAO) -> None:
        self.question_dao = question_dao

    # --------------------------------------------------------------------- #
    # Read operations
    # --------------------------------------------------------------------- #
    def list_questions(self) -> List[Question]:
        return self.question_dao.list_all()

    def get_by_id(self, question_id: int) -> Optional[Question]:
        return self.question_dao.get_by_id(question_id)

    # --------------------------------------------------------------------- #
    # Write operations
    # --------------------------------------------------------------------- #
    def create_question(
        self,
        text: str,
        category: str,
        options: List[str],
        correct_index: int,
    ) -> Question:
        question = Question(
            text=text,
            category=category,
            options=options,
            correct_index=correct_index,
        )
        return self.question_dao.create(question)

    def delete_question(self, question_id: int) -> bool:
        return self.question_dao.delete(question_id)

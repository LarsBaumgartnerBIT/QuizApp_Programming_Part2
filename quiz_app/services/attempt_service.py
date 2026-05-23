from __future__ import annotations
from typing import List, Optional, Sequence, Tuple
from ..domain.models import Answer, Attempt, Question
from ..data_access.dao import AttemptDAO
from .certificate_service import CertificateService
from .grading_service import GradingService

class AttemptService:
    def __init__(
        self,
        attempt_dao: AttemptDAO,
        certificate_service: CertificateService,
        grading_service: GradingService,
    ) -> None:
        self.attempt_dao = attempt_dao
        self.certificate_service = certificate_service
        self.grading_service = grading_service

    def submit(
        self, player_name: str, responses: Sequence[Tuple[Question, int]]
    ) -> Tuple[Attempt, str]:
        answers = [
            Answer(
                question=question,
                selected_index=selected_index,
                is_correct=(selected_index == question.correct_index),
            )
            for question, selected_index in responses
        ]
        num_correct, score_percent, grade = self.grading_service.evaluate(
            answer.is_correct for answer in answers
        )
        attempt = Attempt(
            player_name=player_name,
            num_questions=len(answers),
            num_correct=num_correct,
            score_percent=score_percent,
            grade=grade,
            answers=answers,
        )
        created_attempt = self.attempt_dao.create(attempt)
        loaded_attempt = self.attempt_dao.get_with_items(created_attempt.id)
        path = self.certificate_service.generate_pdf(loaded_attempt)
        return created_attempt, str(path)

    def list_recent(self, limit: int = 200) -> List[Attempt]:
        return self.attempt_dao.list_recent(limit=limit)

    def get_with_items(self, attempt_id: int) -> Optional[Attempt]:
        return self.attempt_dao.get_with_items(attempt_id)

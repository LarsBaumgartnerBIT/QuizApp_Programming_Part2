from __future__ import annotations
from typing import Dict, List, Tuple
from ..domain.models import Attempt, Question
from ..services.attempt_service import AttemptService
from ..services.question_service import QuestionService

class AdminController:
    def __init__(self, attempt_service: AttemptService) -> None:
        self.attempt_service = attempt_service

    def list_attempts(self, limit: int = 200) -> List[Attempt]:
        """List the most recent quiz attempts."""
        return self.attempt_service.list_recent(limit=limit)


class QuizController:
    def __init__(
        self, question_service: QuestionService, attempt_service: AttemptService
    ) -> None:
        self.question_service = question_service
        self.attempt_service = attempt_service
        # Maps question id -> selected option index for the quiz in progress.
        self._answers: Dict[int, int] = {}

    def questions(self) -> List[Question]:
        return self.question_service.list_questions()

    def set_answer(self, question_id: int, selected_index: int) -> None:
        question = self.question_service.get_by_id(question_id)
        if question is None:
            raise ValueError(f"Unknown question id: {question_id}")
        if selected_index < 0 or selected_index >= len(question.options):
            raise ValueError("Selected option is out of range.")
        self._answers[question_id] = selected_index

    def clear_answers(self) -> None:
        self._answers.clear()

    def progress(self) -> Tuple[int, int]:
        return len(self._answers), len(self.questions())

    def submit(self, player_name: str) -> Tuple[Attempt, str]:
        name = (player_name or "").strip()
        if len(name) < 2:
            raise ValueError("Please enter your name (at least 2 characters).")
        questions = self.questions()
        if not questions:
            raise ValueError("No questions available.")
        if len(self._answers) < len(questions):
            raise ValueError("Please answer all questions before submitting.")
        responses = [(question, self._answers[question.id]) for question in questions]
        attempt, certificate_path = self.attempt_service.submit(
            player_name=name, responses=responses
        )
        self.clear_answers()
        return attempt, certificate_path

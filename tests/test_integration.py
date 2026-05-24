from __future__ import annotations
from pathlib import Path
from quiz_app.services.attempt_service import AttemptService
from quiz_app.services.question_service import QuestionService


# --------------------------------------------------------------------------- #
# Helper
# --------------------------------------------------------------------------- #
def _all_correct_responses(question_service: QuestionService):
    return [(q, q.correct_index) for q in question_service.list_questions()]


def _all_wrong_responses(question_service: QuestionService):
    return [
        (q, 0 if q.correct_index != 0 else 1)
        for q in question_service.list_questions()
    ]


# --------------------------------------------------------------------------- #
# 10. Submitting a correct quiz creates an attempt + writes the PDF.
# --------------------------------------------------------------------------- #
def test_submit_all_correct_creates_attempt_and_certificate(
    question_service: QuestionService,
    attempt_service: AttemptService,
):
    responses = _all_correct_responses(question_service)

    attempt, certificate_path = attempt_service.submit("Alice", responses)

    # Attempt was persisted with the expected aggregate values.
    assert attempt.id is not None
    assert attempt.player_name == "Alice"
    assert attempt.num_correct == len(responses)
    assert attempt.score_percent == 100.0
    assert attempt.grade == 6.0
    # Certificate file actually exists on disk.
    pdf_path = Path(certificate_path)
    assert pdf_path.exists()
    assert pdf_path.suffix == ".pdf"
    assert pdf_path.stat().st_size > 0


# --------------------------------------------------------------------------- #
# 11. Wrong answers grade down + list_recent returns the new attempt first.
# --------------------------------------------------------------------------- #
def test_submit_all_wrong_grades_to_one_and_appears_in_recent(
    question_service: QuestionService,
    attempt_service: AttemptService,
):
    responses = _all_wrong_responses(question_service)

    attempt, _ = attempt_service.submit("Bob", responses)

    assert attempt.num_correct == 0
    assert attempt.score_percent == 0.0
    assert attempt.grade == 1.0

    recent = attempt_service.list_recent()
    assert recent[0].id == attempt.id
    assert recent[0].player_name == "Bob"


# --------------------------------------------------------------------------- #
# 12. Multiple submits keep ordering newest-first in list_recent.
# --------------------------------------------------------------------------- #
def test_multiple_submits_are_listed_newest_first(
    question_service: QuestionService,
    attempt_service: AttemptService,
):
    first_attempt, _ = attempt_service.submit(
        "Player-1", _all_wrong_responses(question_service)
    )
    second_attempt, _ = attempt_service.submit(
        "Player-2", _all_correct_responses(question_service)
    )
    third_attempt, _ = attempt_service.submit(
        "Player-3", _all_correct_responses(question_service)
    )

    recent = attempt_service.list_recent(limit=10)
    ids_in_order = [a.id for a in recent]
    assert ids_in_order[:3] == [third_attempt.id, second_attempt.id, first_attempt.id]
    assert recent[0].grade == 6.0
    assert recent[2].grade == 1.0

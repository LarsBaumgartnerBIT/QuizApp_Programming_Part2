from __future__ import annotations
import pytest
from quiz_app.services.certificate_service import CertificateService
from quiz_app.services.grading_service import GradingService
from quiz_app.domain.models import Attempt


# --------------------------------------------------------------------------- #
# 1. GradingService all correct
# --------------------------------------------------------------------------- #
def test_grading_all_correct_returns_grade_six():
    service = GradingService()
    flags = [True, True, True, True]
    num_correct, score_percent, grade = service.evaluate(flags)
    assert num_correct == 4
    assert score_percent == 100.0
    assert grade == 6.0


# --------------------------------------------------------------------------- #
# 2. GradingService all wrong
# --------------------------------------------------------------------------- #
def test_grading_all_wrong_returns_grade_one():
    service = GradingService()

    num_correct, score_percent, grade = service.evaluate([False, False, False, False])

    assert num_correct == 0
    assert score_percent == 0.0
    assert grade == 1.0


# --------------------------------------------------------------------------- #
# 3. GradingService partial
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "flags, expected_correct, expected_score, expected_grade",
    [
        ([True, False], 1, 50.0, 3.5),
        ([True, True, False, False], 2, 50.0, 3.5),
        ([True, True, True, False], 3, 75.0, 4.8),
        ([True] * 9 + [False], 9, 90.0, 5.5),
    ],
)
def test_grading_partial_correct(flags, expected_correct, expected_score, expected_grade):
    service = GradingService()

    num_correct, score_percent, grade = service.evaluate(flags)

    assert num_correct == expected_correct
    assert score_percent == pytest.approx(expected_score)
    assert grade == pytest.approx(expected_grade)


# --------------------------------------------------------------------------- #
# 4. GradingService - empty Input
# --------------------------------------------------------------------------- #
def test_grading_empty_input_returns_minimum_grade():
    service = GradingService()

    num_correct, score_percent, grade = service.evaluate([])

    assert num_correct == 0
    assert score_percent == 0.0
    assert grade == service.min_grade


# --------------------------------------------------------------------------- #
# 5. GradingService does 4.0 pass?
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "grade, expected",
    [
        (1.0, False),
        (3.9, False),
        (4.0, True),
        (4.5, True),
        (6.0, True),
    ],
)
def test_grading_is_passing_boundary(grade, expected):
    service = GradingService()
    assert service.is_passing(grade) is expected


# --------------------------------------------------------------------------- #
# 6. CertificateService not finished export
# --------------------------------------------------------------------------- #
def test_certificate_service_requires_persisted_attempt(tmp_path):
    service = CertificateService(str(tmp_path))
    unsaved = Attempt(player_name="Alice", num_questions=0, num_correct=0)

    with pytest.raises(ValueError):
        service.generate_pdf(unsaved)

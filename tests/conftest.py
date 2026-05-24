from __future__ import annotations
import pytest
from sqlmodel import Session, SQLModel, create_engine
from quiz_app.data_access.dao import AttemptDAO, QuestionDAO
from quiz_app.data_access.seed import QuestionSeeder
from quiz_app.services.attempt_service import AttemptService
from quiz_app.services.certificate_service import CertificateService
from quiz_app.services.grading_service import GradingService
from quiz_app.services.question_service import QuestionService


# --------------------------------------------------------------------------- #
# Engine / schema
# --------------------------------------------------------------------------- #
@pytest.fixture
def engine():
    eng = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(eng)
    return eng


@pytest.fixture
def seeded_engine(engine):
    with Session(engine) as session:
        QuestionSeeder().seed(session)
        session.commit()
    return engine


# --------------------------------------------------------------------------- #
# DAOs and services on top of the seeded engine
# --------------------------------------------------------------------------- #
@pytest.fixture
def question_dao(seeded_engine) -> QuestionDAO:
    return QuestionDAO(seeded_engine)


@pytest.fixture
def attempt_dao(seeded_engine) -> AttemptDAO:
    return AttemptDAO(seeded_engine)


@pytest.fixture
def grading_service() -> GradingService:
    return GradingService()


@pytest.fixture
def certificate_service(tmp_path) -> CertificateService:
    return CertificateService(str(tmp_path / "certificates"))


@pytest.fixture
def question_service(question_dao) -> QuestionService:
    return QuestionService(question_dao)


@pytest.fixture
def attempt_service(attempt_dao, certificate_service, grading_service) -> AttemptService:
    return AttemptService(
        attempt_dao=attempt_dao,
        certificate_service=certificate_service,
        grading_service=grading_service,
    )

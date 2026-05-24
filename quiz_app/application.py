from __future__ import annotations

from nicegui import ui

from .data_access.dao import AttemptDAO, QuestionDAO
from .data_access.db import Database
from .services.attempt_service import AttemptService
from .services.certificate_service import CertificateService
from .services.grading_service import GradingService
from .services.question_service import QuestionService
from .ui.controllers import AdminController, QuizController
from .ui.pages import Pages


class QuizApp:
    """Top-level composition root. Wires DB, DAOs, services, controllers and UI."""

    def __init__(
        self,
        *,
        database_url: str | None = None,
        certificate_dir: str = "data/certificates",
    ) -> None:
        self._database = Database(database_url)
        self._certificate_dir = certificate_dir

    def _build_pages(self) -> Pages:
        engine = self._database.engine
        question_dao = QuestionDAO(engine)
        attempt_dao = AttemptDAO(engine)

        grading_service = GradingService()
        certificate_service = CertificateService(self._certificate_dir)
        question_service = QuestionService(question_dao)
        attempt_service = AttemptService(
            attempt_dao=attempt_dao,
            certificate_service=certificate_service,
            grading_service=grading_service,
        )

        quiz_controller = QuizController(question_service, attempt_service)
        admin_controller = AdminController(attempt_service)
        return Pages(quiz_controller, admin_controller)

    def run(self, *, host: str = "127.0.0.1", port: int = 8080) -> None:
        self._database.init_schema_and_seed()
        pages = self._build_pages()
        pages.register()
        ui.run(host=host, port=port, title="QuizRP", reload=False)

from __future__ import annotations
from datetime import timezone
from zoneinfo import ZoneInfo
from nicegui import ui
from .controllers import AdminController, QuizController

class Pages:
    def __init__(
        self, quiz_controller: QuizController, admin_controller: AdminController
    ) -> None:
        self._quiz_controller = quiz_controller
        self._admin_controller = admin_controller
    def register(self) -> None:
        quiz_controller = self._quiz_controller
        admin_controller = self._admin_controller
        @ui.page("/")
        def quiz_page() -> None:
            quiz_controller.clear_answers()
            ui.markdown("# 🧠 QuizApp")
            ui.label(
                "Answer every question and submit to get your grade "
                "on the Swiss scale (1-6)."
            )
            name_input = ui.input(label="Your name", placeholder="e.g. Alex").classes("w-72")
            questions = quiz_controller.questions()
            progress_label = ui.label().classes("text-sm text-grey")
            def refresh_progress() -> None:
                answered, total = quiz_controller.progress()
                progress_label.text = f"Answered {answered} of {total} questions"
            def on_select(question_id: int, value) -> None:
                if value is None:
                    return
                try:
                    quiz_controller.set_answer(question_id, int(value))
                except ValueError as ex:
                    ui.notify(str(ex), type="warning")
                    return
                refresh_progress()
            for index, question in enumerate(questions, start=1):
                with ui.card().classes("w-full max-w-2xl"):
                    ui.label(f"Question {index}: {question.text}").classes(
                        "text-base font-bold"
                    )
                    ui.label(f"Category: {question.category}").classes("text-xs text-grey")
                    options = {i: option for i, option in enumerate(question.options)}
                    ui.radio(
                        options,
                        on_change=lambda e, qid=question.id: on_select(qid, e.value),
                    )
            refresh_progress()
            result_container = ui.column().classes("w-full max-w-2xl")
            def do_submit() -> None:
                try:
                    attempt, certificate_path = quiz_controller.submit(name_input.value)
                except ValueError as ex:
                    ui.notify(str(ex), type="warning")
                    return
                ui.notify(
                    f"Attempt #{attempt.id} saved. Grade: {attempt.grade}",
                    type="positive",
                )
                result_container.clear()
                with result_container:
                    with ui.card().classes("w-full"):
                        ui.label("Your result").classes("text-lg font-bold")
                        ui.label(f"Player: {attempt.player_name}")
                        ui.label(
                            f"Correct answers: {attempt.num_correct} "
                            f"of {attempt.num_questions}"
                        )
                        ui.label(f"Score: {attempt.score_percent:.1f}%")
                        ui.label(f"Grade (1-6): {attempt.grade}").classes(
                            "text-lg font-bold"
                        )
                        if attempt.grade >= 4.0:
                            ui.label("PASSED ✅").classes("text-positive")
                        else:
                            ui.label("NOT PASSED ❌").classes("text-negative")
                        ui.label(f"Certificate saved: {certificate_path}").classes(
                            "text-xs text-grey"
                        )
                        ui.button(
                            "Take the quiz again",
                            on_click=lambda: ui.navigate.to("/"),
                        ).props("outline")

            with ui.row().classes("gap-2 mt-4"):
                ui.button("Submit quiz", on_click=do_submit).props("color=primary")
            ui.link("Admin: Past attempts", "/admin").classes("mt-6")
        @ui.page("/admin")
        def admin_page() -> None:
            ui.markdown("# 🔐Admin")
            ui.link("← Back to the quiz", "/")
            attempts = admin_controller.list_attempts(limit=200)
            if not attempts:
                ui.label("No attempts yet.")
                return
            columns = [
                {"name": "id", "label": "Attempt", "field": "id", "align": "left"},
                {"name": "created_at", "label": "Created", "field": "created_at", "align": "left"},
                {"name": "player", "label": "Player", "field": "player", "align": "left"},
                {"name": "correct", "label": "Correct", "field": "correct", "align": "right"},
                {"name": "score", "label": "Score (%)", "field": "score", "align": "right"},
                {"name": "grade", "label": "Grade", "field": "grade", "align": "right"},
            ]
            rows = []
            for attempt in attempts:
                local_time = attempt.created_at.replace(tzinfo=timezone.utc).astimezone(
                    ZoneInfo("Europe/Zurich")
                )
                rows.append(
                    {
                        "id": attempt.id,
                        "created_at": local_time.strftime("%d.%m.%Y %H:%M"),
                        "player": attempt.player_name,
                        "correct": f"{attempt.num_correct}/{attempt.num_questions}",
                        "score": f"{attempt.score_percent:.1f}",
                        "grade": f"{attempt.grade:.1f}",
                    }
                )
            ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")
            ui.label(
                "Certificates are saved in the local 'data/certificates/' folder "
                "as certificate_<attempt_id>.pdf."
            )

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

        # ---------------- Quiz page ---------------- #
        @ui.page("/")
        def quiz_page() -> None:
            # fresh start 
            quiz_controller.clear_answers()

            with ui.column().classes("w-full items-center p-8 gap-6 bg-gray-50"):
                # big title with gradient text
                ui.label("Quiz App").classes(
                    "text-5xl font-bold text-center bg-gradient-to-r from-blue-600 to-purple-600 "
                    "bg-clip-text text-transparent"
                )
                    "text-xl text-gray-600 text-center mb-4"
                )

                with ui.column().classes("w-full max-w-2xl gap-6"):
                    # name input
                    with ui.card().classes("w-full shadow-md bg-white").style(
                        "border-radius: 12px; border: 1px solid #e5e7eb;"
                    ):
                        name_input = ui.input("Your name").classes("w-full text-lg").props("outlined rounded")

                    # progress bar
                    with ui.card().classes("w-full sticky top-4 z-10 shadow-lg bg-white").style(
                        "border-radius: 12px; border: 2px solid #ddd;"
                    ):
                        progress_label = ui.label().classes("font-semibold text-gray-800")
                        progress_bar = ui.linear_progress(value=0).props("color=blue rounded").style("height: 8px;")

                    questions = quiz_controller.questions()
                    def refresh_progress() -> None:
                        answered, total = quiz_controller.progress()
                        progress_label.text = f"Progress: {answered}/{total} questions"
                        progress_bar.value = answered / total if total > 0 else 0

                    def on_select(question_id: int, value) -> None:
                        if value is None:
                            return
                        try:
                            quiz_controller.set_answer(question_id, int(value))
                        except ValueError as ex:
                            ui.notify(str(ex), type="warning")
                            return
                        refresh_progress()

                    # one card per question
                    for index, question in enumerate(questions, start=1):
                        with ui.card().classes("w-full p-6 shadow-md bg-white").style(
                            "border-radius: 12px; border: 1px solid #d1d5db;"
                        ):
                            with ui.row().classes("items-center gap-4 mb-3"):
                                ui.label(str(index)).classes(
                                    "text-2xl font-bold bg-blue-500 text-white rounded-full "
                                    "w-10 h-10 flex items-center justify-center"
                                )
                                ui.label(question.text).classes("text-lg font-semibold text-gray-900")
                            ui.label(question.category).classes("text-sm text-gray-600 mb-2 font-medium")
                            options = {i: option for i, option in enumerate(question.options)}
                            ui.radio(
                                options,
                                on_change=lambda e, qid=question.id: on_select(qid, e.value),
                            ).props("color=blue").classes("text-gray-800")

                    refresh_progress()

                    # result card gets filled in after submit
                    result_container = ui.column().classes("w-full")

                    def do_submit() -> None:
                        try:
                            attempt, certificate_path = quiz_controller.submit(name_input.value)
                        except ValueError as ex:
                            ui.notify(str(ex), type="warning")
                            return
                        ui.notify(f"Grade: {attempt.grade}", type="positive")
                        result_container.clear()
                        with result_container:
                            # green for pass, red for fail
                            bg = "bg-green-200" if attempt.grade >= 4.0 else "bg-red-200"
                            border = "border-green-400" if attempt.grade >= 4.0 else "border-red-400"
                            with ui.card().classes(f"w-full p-8 {bg} shadow-xl").style(
                                f"border-radius: 16px; border: 2px solid; border-color: {border};"
                            ):
                                ui.label("Your Result").classes("text-3xl font-bold mb-4 text-gray-900")
                                ui.label(f"Player: {attempt.player_name}").classes("text-lg text-gray-900")
                                ui.label(f"Correct: {attempt.num_correct}/{attempt.num_questions}").classes(
                                    "text-lg text-gray-900"
                                )
                                ui.label(f"Score: {attempt.score_percent:.1f}%").classes("text-lg text-gray-900")
                                ui.label(f"Grade: {attempt.grade}").classes(
                                    "text-4xl font-bold text-blue-600 my-4"
                                )
                                status = "✅ PASSED" if attempt.grade >= 4.0 else "❌ NOT PASSED"
                                ui.label(status).classes("text-2xl font-bold text-gray-900")
                                ui.button(
                                    "Try again", icon="refresh",
                                    on_click=lambda: ui.navigate.to("/"),
                                ).props("rounded").classes("mt-4 bg-blue-600")

                    ui.button("Submit Quiz", icon="send", on_click=do_submit).props(
                        "size=lg rounded"
                    ).classes("w-full bg-blue-600 shadow-lg")
                    ui.link("Admin Panel →", "/admin").classes(
                        "text-blue-700 text-center mt-4 font-semibold"
                    )

        # ---------------- Admin page ---------------- #
        @ui.page("/admin")
        def admin_page() -> None:
            with ui.column().classes("w-full items-center p-8 bg-gray-50"):
                ui.label("🔐 Admin Dashboard").classes("text-4xl font-bold mb-4 text-gray-900")
                ui.link("← Back to Quiz", "/").classes("text-blue-700 mb-6 font-semibold")

                with ui.column().classes("w-full max-w-5xl"):
                    attempts = admin_controller.list_attempts(limit=200)
                    if not attempts:
                        ui.label("No attempts yet.").classes("text-xl text-gray-600")
                        return

                    columns = [
                        {"name": "id", "label": "ID", "field": "id"},
                        {"name": "created_at", "label": "Date", "field": "created_at"},
                        {"name": "player", "label": "Player", "field": "player"},
                        {"name": "correct", "label": "Correct", "field": "correct"},
                        {"name": "grade", "label": "Grade", "field": "grade"},
                    ]
                    rows = []
                    for attempt in attempts:
                        local_time = attempt.created_at.replace(tzinfo=timezone.utc).astimezone(
                            ZoneInfo("Europe/Zurich")
                        )
                        rows.append({
                            "id": attempt.id,
                            "created_at": local_time.strftime("%d.%m.%Y %H:%M"),
                            "player": attempt.player_name,
                            "correct": f"{attempt.num_correct}/{attempt.num_questions}",
                            "grade": f"{attempt.grade:.1f}",
                        })
                    with ui.card().classes("w-full shadow-lg bg-white").style(
                        "border-radius: 12px; border: 1px solid #d1d5db;"
                    ):
                        ui.table(columns=columns, rows=rows).classes("w-full")

from __future__ import annotations
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from ..domain.models import Attempt


class CertificateService:

    # --------------------------------------------------------------------- #
    # Construction
    # --------------------------------------------------------------------- #
    def __init__(self, certificate_dir: str) -> None:
        self.certificate_dir = certificate_dir

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def generate_pdf(self, attempt: Attempt) -> Path:
        if attempt.id is None:
            raise ValueError(
                "Error"
            )
        out_dir = Path(self.certificate_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"certificate_{attempt.id}.pdf"
        c = canvas.Canvas(str(out_path), pagesize=A4)
        width, height = A4
        y = height - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "QuizRP - Result Certificate")
        y -= 25

        c.setFont("Helvetica", 10)
        created_str = attempt.created_at.isoformat(timespec="seconds")
        c.drawString(50, y, f"Attempt ID: {attempt.id}")
        y -= 15
        c.drawString(50, y, f"Player: {attempt.player_name}")
        y -= 15
        c.drawString(50, y, f"Date: {created_str}")
        y -= 25

        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Answers")
        y -= 15
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "#")
        c.drawString(75, y, "Result")
        c.drawString(140, y, "Question")
        y -= 12
        c.line(50, y, width - 50, y)
        y -= 15

        for index, answer in enumerate(attempt.answers, start=1):
            if y < 120:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            question_text = (
                answer.question.text if answer.question else f"Question #{answer.question_id}"
            )
            if len(question_text) > 70:
                question_text = question_text[:67] + "..."
            c.drawString(50, y, str(index))
            c.drawString(75, y, "Correct" if answer.is_correct else "Wrong")
            c.drawString(140, y, question_text)
            y -= 14
        y -= 10
        c.line(50, y, width - 50, y)
        y -= 18
        c.drawRightString(
            width - 50, y, f"Correct answers: {attempt.num_correct} of {attempt.num_questions}"
        )
        y -= 14
        c.drawRightString(width - 50, y, f"Score: {attempt.score_percent:.1f}%")
        y -= 18
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(width - 50, y, f"Grade (1-6): {attempt.grade}")
        y -= 16
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(width - 50, y, "PASSED" if attempt.grade >= 4.0 else "NOT PASSED")

        c.showPage()
        c.save()
        return out_path

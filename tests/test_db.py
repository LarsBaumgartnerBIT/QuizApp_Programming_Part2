from __future__ import annotations
from sqlmodel import Session, select
from quiz_app.data_access.dao import AttemptDAO, QuestionDAO
from quiz_app.data_access.seed import QuestionSeeder
from quiz_app.domain.models import Answer, Attempt

# --------------------------------------------------------------------------- #
# 7. Seeder writes the expected default questions
# --------------------------------------------------------------------------- #
def test_question_seeder_inserts_default_questions(engine):
    dao = QuestionDAO(engine)
    assert dao.list_all() == []

    with Session(engine) as session:
        QuestionSeeder().seed(session)
        session.commit()

    questions = dao.list_all()
    assert len(questions) == 9
    assert all(q.category == "Python Basics" for q in questions)
    assert questions[0].text == "What is Python?"


# --------------------------------------------------------------------------- #
# 8. AttemptDAO.create an attempt with answers
# --------------------------------------------------------------------------- #
def test_attempt_dao_create_persists_attempt_and_answers(seeded_engine):
    dao = AttemptDAO(seeded_engine)
    question_dao = QuestionDAO(seeded_engine)
    questions = question_dao.list_all()

    attempt = Attempt(
        player_name="Bob",
        num_questions=2,
        num_correct=1,
        score_percent=50.0,
        grade=3.5,
        answers=[
            Answer(
                question=questions[0],
                selected_index=questions[0].correct_index,
                is_correct=True,
            ),
            Answer(
                question=questions[1],
                selected_index=(questions[1].correct_index + 1) % len(questions[1].options),
                is_correct=False,
            ),
        ],
    )

    saved = dao.create(attempt)

    assert saved.id is not None
    with Session(seeded_engine) as session:
        stored_answers = list(
            session.exec(select(Answer).where(Answer.attempt_id == saved.id)).all()
        )
        assert len(stored_answers) == 2
        assert sum(1 for a in stored_answers if a.is_correct) == 1


# --------------------------------------------------------------------------- #
# 9. Empty-DB behaviour
# --------------------------------------------------------------------------- #
def test_attempt_dao_empty_db_returns_empty_results(engine):
    # engine = fresh schema, *no* attempts and *no* seed.
    dao = AttemptDAO(engine)

    assert dao.list_recent() == []
    assert dao.get_with_items(attempt_id=1) is None

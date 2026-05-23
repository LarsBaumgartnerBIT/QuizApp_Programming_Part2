from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(index=True, min_length=5, max_length=300)
    category: str = Field(default="General", min_length=2, max_length=60)
    options: list[str] = Field(sa_column=Column(JSON))
    correct_index: int = Field(ge=0, le=9)
    answers: list["Answer"] = Relationship(back_populates="question")

class Attempt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_name: str = Field(index=True, min_length=2, max_length=60)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )
    num_questions: int = Field(default=0, ge=0)
    num_correct: int = Field(default=0, ge=0)
    score_percent: float = Field(default=0.0, ge=0, le=100)
    grade: float = Field(default=1.0, ge=1.0, le=6.0)
    answers: list["Answer"] = Relationship(back_populates="attempt")

class Answer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    attempt_id: int = Field(foreign_key="attempt.id", index=True)
    question_id: int = Field(foreign_key="question.id", index=True)
    selected_index: int = Field(ge=0, le=9)
    is_correct: bool = Field(default=False)
    attempt: "Attempt" = Relationship(back_populates="answers")
    question: "Question" = Relationship(back_populates="answers")
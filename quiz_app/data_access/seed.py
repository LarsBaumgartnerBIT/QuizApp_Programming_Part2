from __future__ import annotations
from sqlmodel import Session
from ..domain.models import Question
class QuestionSeeder:
    def seed(self, session: Session) -> None:
        questions = [
            Question(
                text="What is Python?",
                category="Python Basics",
                options=["A type of snake","A programming language","An operating system","A computer game"],
                correct_index=1,
            ),
            Question(
                text="Which function prints text to the console?",
                category="Python Basics",
                options=["echo()", "print()", "write()", "output()"],
                correct_index=1,
            ),
            Question(
                text="How do you assign the value 5 to a variable in Python?",
                category="Python Basics",
                options=["x == 5", "x := 5", "x = 5", "int x = 5"],
                correct_index=2,
            ),
            Question(
                text="Which data type is used to store text?",
                category="Python Basics",
                options=["int", "float", "bool", "str"],
                correct_index=3,
            ),
            Question(
                text="How do you write a comment in Python?",
                category="Python Basics",
                options=["//", "#", "/*", "--"],
                correct_index=1,
            ),
            Question(
                text="Which function is used to get user input?",
                category="Python Basics",
                options=["scan()", "read()", "input()", "get()"],
                correct_index=2,
            ),
            Question(
                text="What is the result of 3 + 2 * 2?",
                category="Python Basics",
                options=["10", "7", "8", "5"],
                correct_index=1,
            ),
            Question(
                text="Which value represents True in Python?",
                category="Python Basics",
                options=["true", "1", "True", "yes"],
                correct_index=2,
            ),
            Question(
                text="Which loop runs as long as a condition is true?",
                category="Python Basics",
                options=["for", "while", "repeat", "loop"],
                correct_index=1,
            ),
        ]
        for question in questions:
            session.add(question)

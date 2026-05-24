# 🧠 Quiz App – Quiz App by Lars Baumgartner, Noel Anton and Joshua Meng

![UI Showcase](docs/ui_Showcase.png)

---

QuizApp (QuizRP) is a browser-based quiz application written in Python with **NiceGUI**. A player enters their name, answers a series of multiple-choice questions, and immediately receives a percentage score, a Swiss-scale grade from **1 to 6**, and a downloadable **PDF certificate** of their attempt. An admin area at `/admin` lets staff manage the question pool and review every attempt that has ever been submitted.

The project is designed as a complete end-to-end demonstration of:

- a full **layered architecture** (domain → data access → services → UI)
- **data validation** declared directly on the domain models
- **persistent storage** through an ORM (SQLModel on top of SQLAlchemy)
- automated **PDF generation** via ReportLab
- a clean **MVC-inspired** split between controllers, services, and views
- a tested, maintainable Python codebase suitable for teamwork

---

## 📝 Application Requirements

### Problem

Most of the times when someone wants to create a Quiz, they do that by hand and a piece of paper. THis takes long and the feedback is written by hand aswell. This leads to a long waiting time and many human errors.

### Scenario

QuizApp solves this by offering a small, self-contained web app where players can:

- take the quiz
- get an instant feedback with a grade on the Swiss 1–6 scale
- see a clear PASSED / NOT PASSED indicator (passing = grade ≥ 4.0)
- download a PDF certificate listing every answer they gave

…and where an admin can:

- add new questions to the pool through a form
- delete obsolete or wrong questions with one click
- review the full history of past attempts

---

## 📖 User Stories

### 1. Play a Quiz
**As a player, I want to answer a set of multiple-choice questions in the browser.**

- **Inputs:** player name (`str`), selected option per question (`int`)
- **Outputs:** list of questions (`list[Question]`)

### 2. Submit and Get Graded
**As a player, I want my answers graded automatically with a percentage score and a 1–6 grade.**

- **Inputs:** submitted answers (`dict[question_id, selected_index]`)
- **Outputs:** number correct, score in percent, grade on the 1–6 scale

### 3. Pass / Fail Indication
**As a player, I want to immediately see whether I passed (grade ≥ 4.0) or not.**

- **Inputs:** grade (`float`)
- **Outputs:** PASSED / NOT PASSED indicator

### 4. Generate Result Certificate
**As a player, I want a certificate to be created and saved as a PDF file.**

- **Inputs:** completed attempt
- **Outputs:** PDF certificate, file path

### 5. View Past Attempts (Admin)
**As an admin, I want to view past attempts ordered by date.**

- **Inputs:** optional limit (`int`)
- **Outputs:** list of attempts (`list[Attempt]`)

### 6. Manage the Question Pool (Admin)
**As an admin, I want to add new questions and delete obsolete ones without touching the source code.**

- **Inputs:** question text, category, options, correct-answer index — or a question ID to delete
- **Outputs:** updated question list in the database

---

## 🧩 Use Cases

![Use Case Diagram](docs/Use%20Case.png)

### Main Use Cases
- Start Quiz (Player)
- Answer Questions (Player)
- View Result & Certificate (Player)
- Manage Questions – Add / Delete (Admin)
- View Past Attempts (Admin)

### Actors
- **Player** – takes the quiz and receives a result
- **Admin** – curates the question pool and reviews attempts

---

### Wireframes / Mockups

![Wireframe – Mock-up 1](docs/mock-up.png)

![Wireframe – Mock-up 2](docs/mock-up%202.png)

---

## 🏛️ Architecture

![UML Class Diagram](docs/uml_class_architecture.png)

### Layers
- **UI** – NiceGUI pages and controllers ([`quiz_app/ui/`](quiz_app/ui/))
- **Application logic** – services for grading, certificates, attempts and questions ([`quiz_app/services/`](quiz_app/services/))
- **Persistence** – SQLite + SQLModel + DAOs ([`quiz_app/data_access/`](quiz_app/data_access/))
- **Domain** – pure ORM models with built-in validation ([`quiz_app/domain/models.py`](quiz_app/domain/models.py))

### Design Decisions
- **MVC-inspired separation:** views (NiceGUI pages) talk only to controllers; controllers orchestrate services; services depend on DAOs; DAOs depend on the ORM. No UI code touches the database directly.
- **Composition root:** the `QuizApp` class in [`application.py`](quiz_app/application.py) is the single place where the database, DAOs, services, controllers and UI are wired together.
- **Stateless services:** services hold no per-request state, which makes them trivial to test with injected fakes or in-memory databases.

### Design Patterns Used
- **Layered MVC variant** – chosen because the application has a GUI, user interactions, business objects, and database access; a clean separation between them is essential.
- **Facade pattern** – the `Database` class hides engine creation, schema setup, and one-time seeding behind a small interface so callers do not need to know about SQLAlchemy details.
- **Data Access Object (DAO)** – `QuestionDAO` and `AttemptDAO` encapsulate every SQL/ORM access per entity, keeping services free of session handling.
- **Composition root** – `QuizApp.__init__` / `_build_pages` is the single wiring point for all dependencies.

---

## 🗄️ Database and ORM

![ER Diagram](docs/er_diagram.png)

The application uses **SQLModel** (built on SQLAlchemy) to map domain objects to a SQLite database. On first launch the schema is created automatically and, if the question table is empty, a default set of nine "Python Basics" questions is seeded.

### Entities
- `Question` – text, category, options, correct-answer index
- `Attempt` – player name, timestamp, totals, score and grade
- `Answer` – the selected option per question for a given attempt

### Relationships
- One `Attempt` → many `Answer`
- Each `Answer` references exactly one `Question`

---

## ✅ Project Requirements

to do Lars

---

## ⚙️ Implementation

to do Lars

---

## 📂 Repository Structure

to do Lars

---

### How to Run

to do Lars

---

## 🧪 Testing

to do Lars

---

## 👥 Team & Contributions

| Name              | Contribution                                                          |
|-------------------|-----------------------------------------------------------------------|
| Joshua Meng       | NiceGUI UI (quiz and admin pages, styling) + documentation            |
| Noel Anton        | Database & ORM (models, DAOs, schema, seeding) + documentation        |
| Lars Baumgartner  | Business logic (services, controllers, grading, certificates), full test suite (`tests/`) + documentation |


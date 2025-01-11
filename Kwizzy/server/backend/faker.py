from random import randint, choice, uniform
from datetime import datetime, timedelta
from . import db
from . import app
from .models import (
    User,
    Subject,
    Chapter,
    Quiz,
    Question,
    Option,
    QuizResult,
    UserAnswer,
)
from faker import Faker
import random

faker = Faker()


def seed_users(num_users=5):
    users = []
    for _ in range(num_users):
        user = User(
            name=faker.name(),
            email=faker.unique.email(),
            dob=faker.date_of_birth(minimum_age=18, maximum_age=25),
            qualification=choice(["High School", "Bachelors", "Masters"]),
            role=choice(["student", "admin"]),
            profile_pic=None,
            password="password123",
        )
        db.session.add(user)
    db.session.commit()
    return User.query.all()


def seed_subjects(num_subjects=2):
    subjects = []
    for _ in range(num_subjects):
        subject = Subject(
            name=faker.unique.word().capitalize(),
            description=faker.text(max_nb_chars=200),
        )
        db.session.add(subject)
    db.session.commit()
    return Subject.query.all()


def seed_chapters(subjects):
    chapters = []
    for subject in subjects:
        for _ in range(random.randint(2, 5)):
            chapter = Chapter(
                name=faker.word().capitalize(),
                description=faker.sentence(),
                subject_id=subject.id,
            )
            db.session.add(chapter)
    db.session.commit()
    return Chapter.query.all()


def seed_quizzes(chapters):
    quizzes = []
    for chapter in chapters:
        for _ in range(random.randint(2, 4)):
            quiz = Quiz(
                name=faker.word().capitalize(),
                description=faker.text(max_nb_chars=200),
                chapter_id=chapter.id,
                price=random.randint(0, 500),
                time_duration=random.randint(20, 60),
            )
            db.session.add(quiz)
    db.session.commit()
    return Quiz.query.all()


def seed_questions(quizzes, num_questions_per_quiz=5):
    questions = []
    for quiz in quizzes:
        for _ in range(num_questions_per_quiz):
            question = Question(
                quiz_id=quiz.id,
                title=faker.sentence(nb_words=5),
                text=faker.sentence(nb_words=15),
            )
            db.session.add(question)
    db.session.commit()
    return Question.query.all()


def seed_options(questions, num_options_per_question=4):
    options = []
    for question in questions:
        correct_option = randint(0, num_options_per_question - 1)
        for i in range(num_options_per_question):
            option = Option(
                question_id=question.id,
                text=faker.sentence(nb_words=5),
                is_correct=(i == correct_option),
            )
            db.session.add(option)
    db.session.commit()
    return Option.query.all()


def seed_quiz_results(users, quizzes):
    results = []
    for user in users:
        num_attempts = random.randint(1, len(quizzes))
        selected_quizzes = random.sample(quizzes, num_attempts)

        for quiz in selected_quizzes:
            result = QuizResult(
                user_id=user.id,
                quiz_id=quiz.id,
                marks_scored=round(random.uniform(0, 100), 2),
                total_marks=100.0,
                completed_at=faker.date_time_between(start_date="+1d", end_date="+7d"),
            )
            db.session.add(result)
    db.session.commit()
    return QuizResult.query.all()


def seed_user_answers(quiz_results, questions, options):
    for result in quiz_results:
        quiz_questions = [q for q in questions if q.quiz_id == result.quiz_id]
        for question in quiz_questions:
            question_options = [o for o in options if o.question_id == question.id]
            if question_options:
                selected_option = random.choice(question_options)
                answer = UserAnswer(
                    result_id=result.id,
                    question_id=question.id,
                    selected_option=selected_option.id,
                    is_correct=selected_option.is_correct,
                )
                db.session.add(answer)
    db.session.commit()
    return UserAnswer.query.all()


def seed_database():
    print("Seeding database...")
    with app.app_context():
        UserAnswer.query.delete()
        QuizResult.query.delete()
        Option.query.delete()
        Question.query.delete()
        Quiz.query.delete()
        Chapter.query.delete()
        Subject.query.delete()
        User.query.delete()
        db.session.commit()

        # Seed new data
        users = seed_users(num_users=10)
        print(f"Seeded {len(users)} users")

        subjects = seed_subjects(num_subjects=2)
        print(f"Seeded {len(subjects)} subjects")

        chapters = seed_chapters(subjects)
        print(f"Seeded {len(chapters)} chapters")

        quizzes = seed_quizzes(chapters)
        print(f"Seeded {len(quizzes)} quizzes")

        questions = seed_questions(quizzes)
        print(f"Seeded {len(questions)} questions")

        options = seed_options(questions)
        print(f"Seeded {len(options)} options")

        quiz_results = seed_quiz_results(users, quizzes)
        print(f"Seeded {len(quiz_results)} quiz results")

        user_answers = seed_user_answers(quiz_results, questions, options)
        print(f"Seeded {len(user_answers)} user answers")

        return {
            "users": users,
            "subjects": subjects,
            "chapters": chapters,
            "quizzes": quizzes,
            "questions": questions,
            "options": options,
            "quiz_results": quiz_results,
            "user_answers": user_answers,
        }

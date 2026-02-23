from pathlib import Path

import pandas as pd


def append_clean_sample_data() -> None:
    base = Path(__file__).resolve().parent.parent / "data"

    learners_path = base / "sample_learners.csv"
    courses_path = base / "sample_courses.csv"
    enrollments_path = base / "sample_enrollments.csv"

    learners = pd.read_csv(learners_path)
    more_learners = pd.DataFrame(
        [
            {"learner_id": "L006", "email": "frank@example.com", "country_code": "AU", "signup_date": "2024-03-20"},
            {"learner_id": "L007", "email": "grace@example.com", "country_code": "US", "signup_date": "2024-03-22"},
            {"learner_id": "L008", "email": "harry@example.com", "country_code": "UK", "signup_date": "2024-03-25"},
            {"learner_id": "L009", "email": "irene@example.com", "country_code": "IN", "signup_date": "2024-03-28"},
            {"learner_id": "L010", "email": "jack@example.com", "country_code": "CA", "signup_date": "2024-04-01"},
        ]
    )
    learners = pd.concat([learners, more_learners], ignore_index=True)
    learners.to_csv(learners_path, index=False)

    courses = pd.read_csv(courses_path)
    more_courses = pd.DataFrame(
        [
            {
                "course_id": "C105",
                "course_name": "Data Visualization with Power BI",
                "category_name": "Data Science",
                "level_code": "Intermediate",
                "duration_minutes": 420,
            },
            {
                "course_id": "C106",
                "course_name": "Advanced SQL Optimization",
                "category_name": "Data Science",
                "level_code": "Advanced",
                "duration_minutes": 480,
            },
            {
                "course_id": "C107",
                "course_name": "Cloud Data Warehousing with Snowflake",
                "category_name": "Data Engineering",
                "level_code": "Intermediate",
                "duration_minutes": 540,
            },
            {
                "course_id": "C108",
                "course_name": "Real-time Analytics with Kafka & Spark",
                "category_name": "Data Engineering",
                "level_code": "Advanced",
                "duration_minutes": 600,
            },
        ]
    )
    courses = pd.concat([courses, more_courses], ignore_index=True)
    courses.to_csv(courses_path, index=False)

    enrollments = pd.read_csv(enrollments_path)
    more_enrollments = pd.DataFrame(
        [
            {
                "enrollment_id": "E007",
                "learner_id": "L006",
                "course_id": "C101",
                "instructor_id": "I001",
                "enroll_date": "2024-03-18",
                "progress_pct": 20,
                "time_spent_minutes": 60,
                "certificate_issued": False,
            },
            {
                "enrollment_id": "E008",
                "learner_id": "L006",
                "course_id": "C105",
                "instructor_id": "I003",
                "enroll_date": "2024-03-22",
                "progress_pct": 40,
                "time_spent_minutes": 120,
                "certificate_issued": False,
            },
            {
                "enrollment_id": "E009",
                "learner_id": "L007",
                "course_id": "C102",
                "instructor_id": "I002",
                "enroll_date": "2024-03-23",
                "progress_pct": 60,
                "time_spent_minutes": 180,
                "certificate_issued": False,
            },
            {
                "enrollment_id": "E010",
                "learner_id": "L007",
                "course_id": "C105",
                "instructor_id": "I003",
                "enroll_date": "2024-03-25",
                "progress_pct": 10,
                "time_spent_minutes": 45,
                "certificate_issued": False,
            },
            {
                "enrollment_id": "E011",
                "learner_id": "L008",
                "course_id": "C103",
                "instructor_id": "I001",
                "enroll_date": "2024-03-26",
                "progress_pct": 80,
                "time_spent_minutes": 300,
                "certificate_issued": True,
            },
            {
                "enrollment_id": "E012",
                "learner_id": "L009",
                "course_id": "C106",
                "instructor_id": "I004",
                "enroll_date": "2024-03-29",
                "progress_pct": 30,
                "time_spent_minutes": 90,
                "certificate_issued": False,
            },
            {
                "enrollment_id": "E013",
                "learner_id": "L009",
                "course_id": "C107",
                "instructor_id": "I004",
                "enroll_date": "2024-03-30",
                "progress_pct": 0,
                "time_spent_minutes": 0,
                "certificate_issued": False,
            },
            {
                "enrollment_id": "E014",
                "learner_id": "L010",
                "course_id": "C108",
                "instructor_id": "I004",
                "enroll_date": "2024-04-02",
                "progress_pct": 15,
                "time_spent_minutes": 75,
                "certificate_issued": False,
            },
            {
                "enrollment_id": "E015",
                "learner_id": "L010",
                "course_id": "C101",
                "instructor_id": "I001",
                "enroll_date": "2024-04-05",
                "progress_pct": 50,
                "time_spent_minutes": 200,
                "certificate_issued": False,
            },
            {
                "enrollment_id": "E016",
                "learner_id": "L005",
                "course_id": "C105",
                "instructor_id": "I003",
                "enroll_date": "2024-03-18",
                "progress_pct": 30,
                "time_spent_minutes": 100,
                "certificate_issued": False,
            },
        ]
    )
    enrollments = pd.concat([enrollments, more_enrollments], ignore_index=True)
    enrollments.to_csv(enrollments_path, index=False)


if __name__ == "__main__":
    append_clean_sample_data()


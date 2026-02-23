"""
Build Power BI data source: same data as localhost dashboard (Streamlit).
Output: powerbi/LearningPlatform_Data.xlsx (and CSVs in powerbi/data/).
Run from project root: python powerbi/build_powerbi_data.py
"""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
OUT = Path(__file__).resolve().parent
OUT_DATA = OUT / "data"


def main():
    OUT_DATA.mkdir(parents=True, exist_ok=True)

    learners = pd.read_csv(DATA / "sample_learners.csv")
    enrollments = pd.read_csv(DATA / "sample_enrollments.csv")
    courses = pd.read_csv(DATA / "sample_courses.csv")

    # Merged table for charts that need course_name, category, etc.
    enr = enrollments.merge(courses, on="course_id", how="left")

    # Pre-aggregated for specific charts (optional; Power BI can aggregate from base tables)
    enrollments["enroll_date"] = pd.to_datetime(enrollments["enroll_date"])
    by_date = enrollments.groupby("enroll_date").size().reset_index(name="count")
    by_course = enr.groupby("course_name").size().reset_index(name="enrollments")
    by_category = courses.groupby("category_name").size().reset_index(name="courses")
    agg_course = enr.groupby("course_name").agg(
        enrollments=("enrollment_id", "count"),
        avg_progress=("progress_pct", "mean"),
    ).reset_index()

    # Write CSVs (Power BI can connect to folder)
    learners.to_csv(OUT_DATA / "Learners.csv", index=False)
    enrollments.to_csv(OUT_DATA / "Enrollments.csv", index=False)
    courses.to_csv(OUT_DATA / "Courses.csv", index=False)
    enr.to_csv(OUT_DATA / "EnrollmentsWithCourses.csv", index=False)
    by_date.to_csv(OUT_DATA / "EnrollmentsByDate.csv", index=False)
    by_course.to_csv(OUT_DATA / "EnrollmentsByCourse.csv", index=False)
    by_category.to_csv(OUT_DATA / "CoursesByCategory.csv", index=False)
    agg_course.to_csv(OUT_DATA / "EnrollmentsByCourseWithProgress.csv", index=False)

    # Write Excel (one workbook, multiple sheets) if openpyxl available
    try:
        excel_path = OUT / "LearningPlatform_Data.xlsx"
        with pd.ExcelWriter(excel_path, engine="openpyxl") as w:
            learners.to_excel(w, sheet_name="Learners", index=False)
            enrollments.to_excel(w, sheet_name="Enrollments", index=False)
            courses.to_excel(w, sheet_name="Courses", index=False)
            enr.to_excel(w, sheet_name="EnrollmentsWithCourses", index=False)
            by_date.to_excel(w, sheet_name="EnrollmentsByDate", index=False)
            by_course.to_excel(w, sheet_name="EnrollmentsByCourse", index=False)
            by_category.to_excel(w, sheet_name="CoursesByCategory", index=False)
            agg_course.to_excel(w, sheet_name="EnrollmentsByCourseWithProgress", index=False)
        print(f"Excel written: {excel_path}")
    except ImportError:
        print("Install openpyxl for Excel output: pip install openpyxl")

    print(f"CSVs in: {OUT_DATA}")


if __name__ == "__main__":
    main()

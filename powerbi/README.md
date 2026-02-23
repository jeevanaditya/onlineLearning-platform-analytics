# Power BI – Same data and graphs as localhost (http://localhost:8501)

## Quick start

1. **Open Power BI Desktop** → Get data → **Excel** → choose **`LearningPlatform_Data.xlsx`** in this folder (or **Folder** → select **`data`** for CSVs).
2. Load the sheets/tables you need (see **`docs/PowerBI_Guide.md`** for which tables map to which visuals).
3. Follow **`docs/PowerBI_Guide.md`** to build each visual (Overview KPIs, histogram, bar/pie/line charts, learner progress, data tables).

## Relationship model

**Where to find the Model:** In Power BI Desktop, click the **Model** icon on the **left sidebar** (third icon: Report | Data | **Model**). There you build relationships between tables.

**Exact relationships to create:** See **`powerbi/Relationship_Model.md`** for the full relationship model (Enrollments → Courses, Enrollments → Learners) and a diagram.

---

## Files

| File | Use in Power BI |
|------|------------------|
| **LearningPlatform_Data.xlsx** | Single workbook: sheets Learners, Enrollments, Courses, EnrollmentsWithCourses, EnrollmentsByDate, EnrollmentsByCourse, CoursesByCategory, EnrollmentsByCourseWithProgress. |
| **data/*.csv** | Same data as CSV; connect via “Get data → Folder” or individual “Text/CSV”. |

## Regenerate data

From project root:

```bash
python powerbi/build_powerbi_data.py
```

This refreshes the Excel and CSVs from **`data/sample_*.csv`** (same source as the Streamlit dashboard).

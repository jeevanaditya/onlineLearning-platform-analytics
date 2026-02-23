# Power BI – Where to Find the Model & How to Build Relationships

## Where to find the Model (relationship view)

1. Open **Power BI Desktop** and load your data (e.g. from **LearningPlatform_Data.xlsx**).
2. On the **left side** you have three icons:
   - **Report** (canvas for visuals)
   - **Data** (table view)
   - **Model** ← **This is where you build relationships.**
3. Click **Model** to open the relationship diagram. You’ll see your tables as boxes; drag between columns to create relationships.

**Path in UI:** Left rail → **Model** (third icon).

---

## Relationship model to create

Use this when you’re in **Model** view. Create these relationships if you’re using the **base tables** (Learners, Enrollments, Courses):

| From table   | From column  | To table | To column  | Cardinality | Cross filter |
|--------------|--------------|----------|------------|--------------|--------------|
| **Enrollments** | course_id   | **Courses**  | course_id   | Many to one (*) | Single      |
| **Enrollments** | learner_id  | **Learners** | learner_id  | Many to one (*) | Single      |

- **Many to one (*):** Many rows in Enrollments can match one row in Courses (or Learners).
- **Cross filter:** Leave as **Single** (filter from “one” side to “many” side).

### Visual summary

```
Learners                    Courses
  learner_id (PK)             course_id (PK)
       ↑                            ↑
       │                            │
       │    Enrollments              │
       └── learner_id                └── course_id
              enrollment_id
              course_id
              learner_id
              enroll_date
              progress_pct
              ...
```

---

## If you only use pre-built sheets

If you load **EnrollmentsWithCourses**, **EnrollmentsByDate**, **EnrollmentsByCourse**, **CoursesByCategory**, **EnrollmentsByCourseWithProgress** and don’t load the base **Learners**, **Enrollments**, **Courses** tables, you **don’t need any relationships**. Each sheet is already flattened or aggregated; use them directly in visuals.

---

## Quick checklist in Model view

- [ ] Open **Model** (left rail in Power BI Desktop).
- [ ] **Enrollments** → **Courses** on **course_id** (Many to one).
- [ ] **Enrollments** → **Learners** on **learner_id** (Many to one).
- [ ] No duplicate or circular relationships.

File location in project: **`powerbi/Relationship_Model.md`** (this file).

# Power BI Guide – Recreate Localhost Dashboard (http://localhost:8501)

This guide shows how to build **the same graphs and data** from the Streamlit dashboard in **Power BI Desktop**. Use the data in **`powerbi/LearningPlatform_Data.xlsx`** (or the **`powerbi/data/`** CSV folder).

---

## Step 1: Get data into Power BI

1. Open **Power BI Desktop**.
2. **Get data** → **Excel** (or **Folder** for CSVs).
   - **Excel:** Select `D:\Project\powerbi\LearningPlatform_Data.xlsx`, then check **Select multiple items** and load these sheets: **Learners**, **Enrollments**, **Courses**, **EnrollmentsWithCourses**, **EnrollmentsByDate**, **EnrollmentsByCourse**, **CoursesByCategory**, **EnrollmentsByCourseWithProgress**.
   - **Folder:** Select `D:\Project\powerbi\data`, combine/transform as needed, then load the tables (Learners, Enrollments, Courses, EnrollmentsWithCourses, etc.).
3. In **Model** view, create relationships (if using base tables only). **Where to find Model:** Left sidebar in Power BI Desktop → click the **Model** icon (third icon). Full relationship instructions: **`powerbi/Relationship_Model.md`**.
   - **Enrollments**\[course_id] → **Courses**\[course_id]
   - **Enrollments**\[learner_id] → **Learners**\[learner_id]
4. Ensure **Enrollments**\[enroll_date] is **Date**; **progress_pct** and **time_spent_minutes** are numeric.

---

## Step 2: Build each visual (same as localhost)

Create **one report** with multiple pages, or one page per section below.

---

### Page: **Overview** (matches localhost Overview)

| # | Visual on localhost | In Power BI |
|---|---------------------|-------------|
| **1** | **KPI cards:** Total Enrollments, Completed, Unique Learners, Unique Courses | **Card** (or **KPI**): Create 4 cards. **Values:** Total Enrollments = `Count(Enrollments[enrollment_id])` or count of rows; Completed = `CountRows(FILTER(Enrollments, Enrollments[certificate_issued] = TRUE))` (or use a measure); Unique Learners = `DISTINCTCOUNT(Enrollments[learner_id])`; Unique Courses = `DISTINCTCOUNT(Enrollments[course_id])`. |
| **2** | **Histogram:** Distribution of Progress % | **Clustered column chart** or **Histogram**: Axis = **EnrollmentsWithCourses**\[progress_pct] (or bin it), Value = **Count of rows**. Or use **Analysis** → **Histogram** (bin progress_pct). |
| **3** | **Bar chart:** Enrollments by Course (color = avg progress %) | **Clustered bar chart**: Axis = **course_name**, Y = **Count of enrollment_id** (or use table **EnrollmentsByCourseWithProgress**: Axis = course_name, Y = enrollments). Legend or **Color saturation** = **avg_progress** (from EnrollmentsByCourseWithProgress) or measure `AVERAGE(Enrollments[progress_pct])` by course. |

---

### Page: **Enrollments**

| # | Visual on localhost | In Power BI |
|---|---------------------|-------------|
| **4** | **Line chart:** Enrollments by Date | **Line chart**: Axis = **Enrollments**\[enroll_date] (or **EnrollmentsByDate**\[enroll_date]), Value = **Count** of enrollments (or **EnrollmentsByDate**\[count]). |
| **5** | **Pie chart:** Share by Course | **Pie chart**: Legend = **course_name** (from EnrollmentsWithCourses or EnrollmentsByCourse), Values = **Count** of enrollments (or **EnrollmentsByCourse**\[enrollments]). |

---

### Page: **Courses & Categories**

| # | Visual on localhost | In Power BI |
|---|---------------------|-------------|
| **6** | **Bar chart:** Courses per Category | **Clustered bar chart**: Axis = **category_name** (from **Courses** or **CoursesByCategory**), Value = **Count** of courses (or **CoursesByCategory**\[courses]). |
| **7** | **Data table:** Courses | **Table** visual: Add columns from **Courses** (course_id, course_name, category_name, level_code, duration_minutes). |

---

### Page: **Learner Progress**

| # | Visual on localhost | In Power BI |
|---|---------------------|-------------|
| **8** | **Slicer:** Select learner | **Slicer**: Field = **EnrollmentsWithCourses**\[learner_id] (or **Enrollments**\[learner_id]). |
| **9** | **Table:** Course, progress %, time spent, certificate | **Table** visual: **course_name**, **progress_pct**, **time_spent_minutes**, **certificate_issued** from **EnrollmentsWithCourses** (filtered by slicer). |
| **10** | **Bar chart:** Progress % by course for selected learner | **Clustered bar chart**: Axis = **course_name**, Value = **progress_pct** (from EnrollmentsWithCourses; will filter by slicer). |

---

### Page: **Data Tables**

| # | Visual on localhost | In Power BI |
|---|---------------------|-------------|
| **11** | **Tables:** Learners, Enrollments, Courses | Three **Table** visuals: one for **Learners**, one for **Enrollments**, one for **Courses** (all columns). |

---

## Step 3: Optional DAX measures (if using base tables only)

Create these in **Enrollments** (or a dedicated table) if you don’t use pre-aggregated sheets:

- **Total Enrollments** = `COUNT(Enrollments[enrollment_id])`
- **Completed** = `CALCULATE(COUNT(Enrollments[enrollment_id]), Enrollments[certificate_issued] = TRUE)`
- **Unique Learners** = `DISTINCTCOUNT(Enrollments[learner_id])`
- **Unique Courses** = `DISTINCTCOUNT(Enrollments[course_id])`
- **Avg Progress** = `AVERAGE(Enrollments[progress_pct])`

Use these in cards and in “color by avg progress” on the bar chart.

---

## Step 4: Data source summary

| Source | Contents |
|--------|----------|
| **Learners** | learner_id, email, country_code, signup_date |
| **Enrollments** | enrollment_id, learner_id, course_id, instructor_id, enroll_date, progress_pct, time_spent_minutes, certificate_issued |
| **Courses** | course_id, course_name, category_name, level_code, duration_minutes |
| **EnrollmentsWithCourses** | Enrollments + course_name, category_name, etc. (for charts that need course/category) |
| **EnrollmentsByDate** | enroll_date, count (for line chart) |
| **EnrollmentsByCourse** | course_name, enrollments (for pie) |
| **CoursesByCategory** | category_name, courses (for category bar) |
| **EnrollmentsByCourseWithProgress** | course_name, enrollments, avg_progress (for overview bar) |

---

## Step 5: Regenerate data (same as localhost)

To refresh the data from the same CSVs that feed the localhost dashboard:

```bash
python powerbi/build_powerbi_data.py
```

Then in Power BI: **Home** → **Transform data** / **Refresh** (or re-load the Excel/folder).

---

You now have the same **graphs and data** in Power BI as on **http://localhost:8501**.

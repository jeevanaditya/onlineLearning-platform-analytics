-- =============================================================================
-- Advanced SQL: CTEs, Window Functions, Indexing, Partitioning
-- (Requirements: CTE, Window Functions, Indexing, Partitioning)
-- =============================================================================
--
-- PARTITIONING (Snowflake): Use CLUSTER BY on fact tables for partition pruning.
--   See schema/ddl_star_schema.sql and ddl_snowflake_objects.sql.
-- WINDOW PARTITION BY: Used below in RANK, ROW_NUMBER, LAG, running totals.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1) CTE: Daily enrollments with course and category
-- -----------------------------------------------------------------------------
WITH daily_enrollments AS (
    SELECT
        d.full_date,
        d.year,
        d.month,
        c.course_id,
        c.course_name,
        cat.category_name,
        f.learner_key,
        f.progress_pct,
        f.certificate_issued
    FROM fact_enrollment f
    JOIN dim_date d ON f.enroll_date_key = d.date_key
    JOIN dim_course c ON f.course_key = c.course_key
    JOIN dim_course_category cat ON c.category_key = cat.category_key
    WHERE d.full_date >= DATEADD(day, -90, CURRENT_DATE())
),
course_totals AS (
    SELECT
        full_date,
        course_id,
        course_name,
        category_name,
        COUNT(*) AS enrollments,
        SUM(CASE WHEN progress_pct >= 100 THEN 1 ELSE 0 END) AS completed
    FROM daily_enrollments
    GROUP BY full_date, course_id, course_name, category_name
)
SELECT * FROM course_totals ORDER BY full_date DESC, enrollments DESC;

-- -----------------------------------------------------------------------------
-- 2) Window: Rank courses by enrollments per month; running total
-- -----------------------------------------------------------------------------
WITH monthly_course AS (
    SELECT
        d.year,
        d.month,
        c.course_name,
        cat.category_name,
        COUNT(*) AS enrollments
    FROM fact_enrollment f
    JOIN dim_date d ON f.enroll_date_key = d.date_key
    JOIN dim_course c ON f.course_key = c.course_key
    JOIN dim_course_category cat ON c.category_key = cat.category_key
    GROUP BY d.year, d.month, c.course_name, cat.category_name
)
SELECT
    year,
    month,
    course_name,
    category_name,
    enrollments,
    RANK() OVER (PARTITION BY year, month ORDER BY enrollments DESC) AS rank_in_month,
    SUM(enrollments) OVER (PARTITION BY year, month ORDER BY enrollments DESC ROWS UNBOUNDED PRECEDING) AS running_total
FROM monthly_course
ORDER BY year DESC, month DESC, rank_in_month;

-- -----------------------------------------------------------------------------
-- 3) Window: Learner progress over time (first/last event per course)
-- -----------------------------------------------------------------------------
WITH learner_events AS (
    SELECT
        learner_key,
        course_key,
        event_date_key,
        event_type,
        duration_seconds,
        ROW_NUMBER() OVER (PARTITION BY learner_key, course_key ORDER BY event_date_key, event_time) AS rn_asc,
        ROW_NUMBER() OVER (PARTITION BY learner_key, course_key ORDER BY event_date_key DESC, event_time DESC) AS rn_desc
    FROM fact_learning_event
)
SELECT
    e.learner_key,
    e.course_key,
    MAX(CASE WHEN e.rn_asc = 1 THEN e.event_date_key END) AS first_event_date_key,
    MAX(CASE WHEN e.rn_desc = 1 THEN e.event_date_key END) AS last_event_date_key
FROM learner_events e
GROUP BY e.learner_key, e.course_key;

-- -----------------------------------------------------------------------------
-- 4) CTE + Window: Completion rate by category (YoY comparison)
-- -----------------------------------------------------------------------------
WITH category_year AS (
    SELECT
        cat.category_name,
        d.year,
        COUNT(DISTINCT f.enrollment_key) AS total_enrollments,
        SUM(CASE WHEN f.progress_pct >= 100 THEN 1 ELSE 0 END) AS completed
    FROM fact_enrollment f
    JOIN dim_course c ON f.course_key = c.course_key
    JOIN dim_course_category cat ON c.category_key = cat.category_key
    JOIN dim_date d ON f.enroll_date_key = d.date_key
    GROUP BY cat.category_name, d.year
),
with_rates AS (
    SELECT
        category_name,
        year,
        total_enrollments,
        completed,
        completed / NULLIF(total_enrollments, 0) * 100 AS completion_pct,
        LAG(completed / NULLIF(total_enrollments, 0) * 100) OVER (PARTITION BY category_name ORDER BY year) AS prev_year_pct
    FROM category_year
)
SELECT
    category_name,
    year,
    total_enrollments,
    completed,
    completion_pct,
    prev_year_pct,
    completion_pct - prev_year_pct AS yoy_change_pct
FROM with_rates
ORDER BY category_name, year DESC;

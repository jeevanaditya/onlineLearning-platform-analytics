-- =============================================================================
-- Snowflake-specific: Warehouses, DB, Schema, Clustering, Time Travel, Semi-structured
-- =============================================================================

-- Create warehouse and database (run with ACCOUNTADMIN or SYSADMIN)
-- CREATE WAREHOUSE IF NOT EXISTS ANALYTICS_WH WITH WAREHOUSE_SIZE = 'SMALL' AUTO_SUSPEND = 300;
-- CREATE DATABASE IF NOT EXISTS LEARNING_PLATFORM_DW DATA_RETENTION_TIME_IN_DAYS = 7;
-- CREATE SCHEMA IF NOT EXISTS LEARNING_PLATFORM_DW.ANALYTICS;

-- Time Travel: default 1 day; can be set per table
-- ALTER TABLE fact_enrollment SET DATA_RETENTION_TIME_IN_DAYS = 7;
-- Query history: SELECT * FROM fact_enrollment AT(OFFSET => -3600);  -- 1 hour ago

-- Semi-structured: raw event log (JSON) staging
CREATE TABLE IF NOT EXISTS raw_learning_events (
    id              VARCHAR(50),
    ingested_at     TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    payload         VARIANT,
    source_file     VARCHAR(255)
);

-- Query semi-structured: payload:level1:level2 or payload['key']
-- SELECT payload:event_type, payload:learner_id, payload:timestamp FROM raw_learning_events;

-- Clustering (run after initial load for large tables)
-- ALTER TABLE fact_enrollment CLUSTER BY (enroll_date_key, course_key);
-- ALTER TABLE fact_learning_event CLUSTER BY (event_date_key, course_key);

-- Materialized view for dashboard (optional performance)
CREATE OR REPLACE VIEW v_enrollment_daily AS
SELECT
    d.full_date,
    d.year,
    d.month,
    c.course_name,
    cat.category_name,
    COUNT(*) AS enrollments,
    SUM(CASE WHEN f.progress_pct >= 100 THEN 1 ELSE 0 END) AS completed
FROM fact_enrollment f
JOIN dim_date d ON f.enroll_date_key = d.date_key
JOIN dim_course c ON f.course_key = c.course_key
JOIN dim_course_category cat ON c.category_key = cat.category_key
GROUP BY d.full_date, d.year, d.month, c.course_name, cat.category_name;

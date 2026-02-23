-- =============================================================================
-- Online Learning Platform Analytics - Star/Snowflake Schema DDL
-- Design: Star schema with fact and dimension tables; snowflake where needed
-- =============================================================================

-- -----------------------------------------------------------------------------
-- DIMENSIONS (Star: denormalized; Snowflake: normalized where hierarchy exists)
-- -----------------------------------------------------------------------------

-- Dim: Time (calendar + fiscal)
CREATE TABLE IF NOT EXISTS dim_date (
    date_key           INTEGER PRIMARY KEY,
    full_date          DATE NOT NULL,
    year               SMALLINT NOT NULL,
    quarter            SMALLINT NOT NULL,
    month              SMALLINT NOT NULL,
    week_of_year       SMALLINT NOT NULL,
    day_of_week        SMALLINT NOT NULL,
    day_name           VARCHAR(9),
    month_name         VARCHAR(9),
    is_weekend         BOOLEAN,
    fiscal_year        SMALLINT,
    fiscal_quarter     SMALLINT
);

-- Dim: Course (snowflake: category as separate dim)
CREATE TABLE IF NOT EXISTS dim_course_category (
    category_key       INTEGER PRIMARY KEY,
    category_name      VARCHAR(100) NOT NULL,
    parent_category_key INTEGER REFERENCES dim_course_category(category_key)
);

CREATE TABLE IF NOT EXISTS dim_course (
    course_key         INTEGER PRIMARY KEY,
    course_id          VARCHAR(50) NOT NULL UNIQUE,
    course_name        VARCHAR(255) NOT NULL,
    category_key       INTEGER NOT NULL REFERENCES dim_course_category(category_key),
    level_code         VARCHAR(20),
    duration_minutes   INTEGER,
    created_at         TIMESTAMP_NTZ,
    updated_at         TIMESTAMP_NTZ
);

-- Dim: User/Learner
CREATE TABLE IF NOT EXISTS dim_learner (
    learner_key        INTEGER PRIMARY KEY,
    learner_id         VARCHAR(50) NOT NULL UNIQUE,
    email_hash         VARCHAR(64),
    country_code       VARCHAR(3),
    signup_date_key    INTEGER REFERENCES dim_date(date_key),
    is_active          BOOLEAN DEFAULT TRUE,
    created_at         TIMESTAMP_NTZ,
    updated_at         TIMESTAMP_NTZ
);

-- Dim: Instructor
CREATE TABLE IF NOT EXISTS dim_instructor (
    instructor_key     INTEGER PRIMARY KEY,
    instructor_id      VARCHAR(50) NOT NULL UNIQUE,
    display_name       VARCHAR(100),
    created_at         TIMESTAMP_NTZ
);

-- Dim: Enrollment (type / status)
CREATE TABLE IF NOT EXISTS dim_enrollment_status (
    status_key         INTEGER PRIMARY KEY,
    status_code        VARCHAR(20) NOT NULL UNIQUE,
    status_label       VARCHAR(50)
);

-- -----------------------------------------------------------------------------
-- FACT TABLES (Star: one fact table per process)
-- -----------------------------------------------------------------------------

-- Fact: Course enrollments (grain: one row per enrollment per day snapshot optional)
CREATE TABLE IF NOT EXISTS fact_enrollment (
    enrollment_key     INTEGER IDENTITY PRIMARY KEY,
    enrollment_id      VARCHAR(50) NOT NULL,
    learner_key        INTEGER NOT NULL REFERENCES dim_learner(learner_key),
    course_key         INTEGER NOT NULL REFERENCES dim_course(course_key),
    instructor_key     INTEGER REFERENCES dim_instructor(instructor_key),
    status_key         INTEGER REFERENCES dim_enrollment_status(status_key),
    enroll_date_key    INTEGER NOT NULL REFERENCES dim_date(date_key),
    complete_date_key  INTEGER REFERENCES dim_date(date_key),
    progress_pct       DECIMAL(5,2),
    time_spent_minutes INTEGER,
    certificate_issued BOOLEAN DEFAULT FALSE,
    created_at         TIMESTAMP_NTZ,
    updated_at         TIMESTAMP_NTZ,
    UNIQUE(enrollment_id)
);

-- Fact: Learning events (video views, quiz attempts, etc.) - optional event grain
CREATE TABLE IF NOT EXISTS fact_learning_event (
    event_key          INTEGER IDENTITY PRIMARY KEY,
    event_id           VARCHAR(50) NOT NULL,
    learner_key        INTEGER NOT NULL REFERENCES dim_learner(learner_key),
    course_key         INTEGER NOT NULL REFERENCES dim_course(course_key),
    event_date_key     INTEGER NOT NULL REFERENCES dim_date(date_key),
    event_time         TIMESTAMP_NTZ,
    event_type         VARCHAR(50),
    module_id          VARCHAR(50),
    duration_seconds   INTEGER,
    score              DECIMAL(5,2),
    payload            VARIANT,
    created_at         TIMESTAMP_NTZ,
    UNIQUE(event_id)
);

-- Fact: Course completions (aggregate/snapshot)
CREATE TABLE IF NOT EXISTS fact_course_completion (
    completion_key     INTEGER IDENTITY PRIMARY KEY,
    learner_key        INTEGER NOT NULL REFERENCES dim_learner(learner_key),
    course_key         INTEGER NOT NULL REFERENCES dim_course(course_key),
    complete_date_key  INTEGER NOT NULL REFERENCES dim_date(date_key),
    final_score        DECIMAL(5,2),
    time_to_complete_days INTEGER,
    created_at         TIMESTAMP_NTZ,
    UNIQUE(learner_key, course_key)
);

-- -----------------------------------------------------------------------------
-- SNOWFLAKE: Clustering for large fact tables (performance)
-- -----------------------------------------------------------------------------
-- ALTER TABLE fact_enrollment CLUSTER BY (enroll_date_key, course_key);
-- ALTER TABLE fact_learning_event CLUSTER BY (event_date_key, course_key);
-- ALTER TABLE fact_course_completion CLUSTER BY (complete_date_key, course_key);

-- -----------------------------------------------------------------------------
-- INDEXING (Snowflake: use clustering; other DBs may use CREATE INDEX)
-- In Snowflake: use CLUSTER BY above; no CREATE INDEX. Micro-partitions + clustering
-- provide partition pruning. For other engines (e.g. Postgres), uncomment:
-- CREATE INDEX idx_fact_enrollment_learner ON fact_enrollment(learner_key);
-- CREATE INDEX idx_fact_enrollment_course ON fact_enrollment(course_key);
-- CREATE INDEX idx_fact_enrollment_date ON fact_enrollment(enroll_date_key);
-- CREATE INDEX idx_fact_event_learner ON fact_learning_event(learner_key);
-- CREATE INDEX idx_fact_event_date ON fact_learning_event(event_date_key);
-- -----------------------------------------------------------------------------

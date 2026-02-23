# Online Learning Platform Analytics – Final Presentation

## 1. Project Goal
Deliver an **analytics solution** for an online learning platform: data warehouse, ETL/ELT, Spark batch/streaming, Snowflake storage and optimization, security, and an interactive dashboard.

## 2. Deliverables Summary

| Requirement | Deliverable |
|-------------|-------------|
| **Data Warehouse Design** | Star/Snowflake schema: `dim_date`, `dim_learner`, `dim_course`, `dim_course_category`, `dim_instructor`, `dim_enrollment_status`, and facts `fact_enrollment`, `fact_learning_event`, `fact_course_completion` (`schema/ddl_star_schema.sql`, `schema/ddl_snowflake_objects.sql`). |
| **Advanced SQL** | CTEs and window functions (rank, row_number, lag, running totals) in `sql/advanced_queries.sql`. |
| **ETL/ELT Pipelines** | Python-based extract/load with optional Snowflake load (`etl/extract_load.py`); sample data in `data/`. |
| **Apache Spark** | Batch job (`spark_jobs/batch_processing.py`) and streaming job (`spark_jobs/streaming_processing.py`) for events. |
| **Snowflake** | Config in `config/settings.yaml`; clustering, time travel, semi-structured (VARIANT) in `snowflake/snowflake_ops.py` and `schema/ddl_snowflake_objects.sql`. |
| **Security** | RBAC (roles, grants), data masking policies, governance tags in `security/rbac_masking.sql`. |
| **Performance Tuning** | Notes in `docs/performance_tuning.md`; Spark AQE and Snowflake clustering. |
| **Interactive Dashboard** | Streamlit app in `dashboard/app.py`: Overview, Enrollments, Courses & Categories, Learner Progress, Data Tables. |
| **Architecture & Presentation** | `docs/architecture.md` and this `docs/FINAL_PRESENTATION.md`. |

## 3. How to Run

### Prerequisites
- Python 3.10+
- Optional: Snowflake account (set `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD` in env or `.env`).

### Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard (uses sample data in data/)
streamlit run dashboard/app.py

# Run ETL (stages CSV from data/raw or uses sample)
python etl/extract_load.py

# Run Spark batch (expects data in data/raw)
python spark_jobs/batch_processing.py
```

### Snowflake Setup
1. Create warehouse, database, schema (see comments in `schema/ddl_snowflake_objects.sql`).
2. Run `schema/ddl_star_schema.sql` and `schema/ddl_snowflake_objects.sql`.
3. Run `security/rbac_masking.sql` for roles and masking (adjust role names as needed).
4. Point ETL/dashboard to Snowflake via `config/settings.yaml` and env vars.

## 4. Schema Overview (Efficient Data Structures)

- **Star:** Facts reference dimension keys (integer surrogate keys); dimensions are denormalized where it helps (e.g. `dim_date` with year, month, week, fiscal fields).
- **Snowflake:** `dim_course_category` is normalized (parent_category_key); `dim_course` references it. This keeps category hierarchy consistent and saves space.
- **Facts:** Grain is explicit (one row per enrollment, per learning event, per completion); integer date keys and FKs support indexing/clustering.

## 5. What You May Need to Provide

- **Snowflake credentials** (account, user, password) if you want live load and dashboard against Snowflake.
- **Sample or production CSV/JSON** schema if it differs from the current `data/sample_*.csv` (we can extend the ETL to map your columns).
- **Kafka/bootstrap servers** if you want Spark streaming to read from Kafka instead of file stream.
- **Preference for dashboard theme** (e.g. dark mode, brand colors) for final UI polish.

---

**Status:** All components are implemented and wired for local/sample data. Connect Snowflake and optional Kafka for a full production-style setup.

---

**Requirements checklist:** See **`docs/REQUIREMENTS_CHECKLIST.md`** for a line-by-line mapping of every screenshot requirement (Data Warehouse, Advanced SQL, ETL/ELT, Spark, Snowflake, Security, Performance, Dashboard, Architecture & Presentation) to the deliverables above.

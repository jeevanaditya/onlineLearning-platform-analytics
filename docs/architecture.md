# Online Learning Platform Analytics – Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SOURCES (CSV, JSON, APIs, Kafka)                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ETL/ELT (Python)          │  Apache Spark (Batch + Streaming)                │
│  • extract_load.py         │  • batch_processing.py                          │
│  • Pandas / Snowflake      │  • streaming_processing.py                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  DATA WAREHOUSE (Snowflake) – Star / Snowflake Schema                         │
│  • dim_date, dim_learner, dim_course, dim_course_category, dim_instructor     │
│  • fact_enrollment, fact_learning_event, fact_course_completion              │
│  • Clustering, Time Travel, Semi-structured (VARIANT)                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐
│  Security              │  │  Advanced SQL          │  │  Dashboard            │
│  RBAC, Masking,        │  │  CTE, Window           │  │  Streamlit + Plotly    │
│  Governance            │  │  Indexing / Clustering │  │  Interactive viz      │
└───────────────────────┘  └───────────────────────┘  └───────────────────────┘
```

## Components

| Component | Purpose |
|-----------|---------|
| **Schema (Star/Snowflake)** | `schema/ddl_*.sql` – dimensions and facts; snowflake for category hierarchy. |
| **ETL/ELT** | Python pipelines to extract, transform (e.g. hash PII), load to staging/Snowflake. |
| **Spark** | Batch aggregation and file-based streaming (Kafka-ready pattern). |
| **Snowflake** | Storage, clustering, time travel, semi-structured (raw_learning_events VARIANT). |
| **Security** | RBAC roles, masking policies, governance tags (`security/rbac_masking.sql`). |
| **Dashboard** | Streamlit app over CSV/Parquet or Snowflake for enrollment, progress, courses. |
| **Advanced SQL** | CTEs and window functions in `sql/advanced_queries.sql`. |

## Data Flow

1. **Ingest:** Raw CSV/JSON → ETL or Spark → Staging / Snowflake raw tables.
2. **Transform:** Spark batch or SQL in Snowflake → fact/dim tables.
3. **Serve:** Dashboard and reports read from DW (or cached Parquet for demo).

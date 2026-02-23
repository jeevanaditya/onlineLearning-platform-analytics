# Online Learning Platform Analytics

Analytics solution for an online learning platform: **Data Warehouse (Star/Snowflake)**, **ETL/ELT**, **Apache Spark (batch + streaming)**, **Snowflake** (clustering, time travel, semi-structured), **Security (RBAC, masking)**, and an **interactive dashboard**.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

Open http://localhost:8501 for the dashboard (uses sample data in `data/`).

## Project Structure

| Path | Description |
|------|-------------|
| `config/settings.yaml` | Snowflake and app config (use env vars for secrets). |
| `schema/ddl_star_schema.sql` | Star/Snowflake dimension and fact DDL. |
| `schema/ddl_snowflake_objects.sql` | Clustering, time travel, semi-structured, views. |
| `sql/advanced_queries.sql` | CTEs, window functions. |
| `etl/extract_load.py` | Python ETL/ELT (CSV → staging/Snowflake). |
| `spark_jobs/batch_processing.py` | Spark batch aggregation. |
| `spark_jobs/streaming_processing.py` | Spark streaming (file or Kafka-ready). |
| `snowflake/snowflake_ops.py` | Clustering, time travel, VARIANT helpers. |
| `security/rbac_masking.sql` | RBAC, data masking, governance. |
| `dashboard/app.py` | Streamlit dashboard. |
| `data/` | Sample CSVs and staging output. |
| `docs/` | Architecture, performance tuning, final presentation. |

## Requirements From You (Optional)

- **Snowflake:** Set `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD` for live load and dashboard.
- **Your data:** If your CSV/JSON columns differ from `data/sample_*.csv`, share the schema to extend the ETL.
- **Kafka:** Bootstrap servers if Spark streaming should read from Kafka.
- **UI:** Theme or brand preferences for the dashboard.

See **`docs/FINAL_PRESENTATION.md`** for the full deliverable summary and **`docs/architecture.md`** for the architecture. An architecture diagram image is in **`assets/architecture_diagram.png`**.

# Performance Tuning & Optimization

## Snowflake
- **Clustering:** Use `CLUSTER BY (enroll_date_key, course_key)` on large fact tables to align micro-partitions with common filters.
- **Time Travel:** Keep retention minimal where not needed to reduce storage.
- **Warehouse size:** Use auto-suspend and scale up only for heavy batch jobs.
- **Query pruning:** Filter on clustering keys (date, course_key) in WHERE to maximize partition pruning.

## Spark
- **Adaptive Query Execution (AQE):** Enabled in `batch_processing.py` (`spark.sql.adaptive.enabled`).
- **Partitioning:** When writing Parquet, partition by `year`, `month` or `date` for fact data.
- **Coalesce:** Use `coalesce`/`repartition` before writes to avoid many small files.

## SQL
- **CTEs:** Used in `sql/advanced_queries.sql` for readability and plan stability.
- **Window functions:** Prefer `ROW_NUMBER()` / `RANK()` over self-joins where appropriate.
- **Indexes:** Snowflake uses clustering keys; traditional indexes are in DDL for documentation (Snowflake may ignore or map to clustering).

## Dashboard
- **Streamlit:** `@st.cache_data` on `load_data()` to avoid re-reading on every interaction.
- **Plotly:** Render only visible charts; limit rows for large datasets.

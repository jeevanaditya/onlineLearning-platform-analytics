"""
ETL/ELT: Extract and Load for Online Learning Platform Analytics.
Reads from CSV/JSON (or DB), validates, and loads into Snowflake or local staging.
"""
import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Iterator, Any

import pandas as pd
import yaml
from dotenv import load_dotenv

load_dotenv()

# Optional: Snowflake (only if credentials set)
try:
    import snowflake.connector
    HAS_SNOWFLAKE = True
except ImportError:
    HAS_SNOWFLAKE = False


def load_config() -> dict:
    config_path = Path(__file__).resolve().parent.parent / "config" / "settings.yaml"
    if not config_path.exists():
        return {}
    with open(config_path) as f:
        raw = f.read()
    for key in ["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER", "SNOWFLAKE_PASSWORD"]:
        raw = raw.replace(f'${{{key}}}', os.environ.get(key, ""))
    return yaml.safe_load(raw) or {}


def extract_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def extract_json(path: str) -> pd.DataFrame:
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, list):
        return pd.DataFrame(data)
    if isinstance(data, dict) and "records" in data:
        return pd.DataFrame(data["records"])
    return pd.DataFrame([data])


def hash_email(email: str) -> str:
    if pd.isna(email) or not str(email).strip():
        return ""
    return hashlib.sha256(str(email).strip().lower().encode()).hexdigest()


def transform_learners(df: pd.DataFrame) -> pd.DataFrame:
    if "email" in df.columns:
        df["email_hash"] = df["email"].astype(str).apply(hash_email)
    return df


def load_to_snowflake(df: pd.DataFrame, table: str, schema: str, conn_params: dict) -> None:
    if not HAS_SNOWFLAKE:
        raise RuntimeError("snowflake-connector-python not installed")
    conn = snowflake.connector.connect(**conn_params)
    try:
        conn.cursor().execute(f"USE SCHEMA {schema}")
        # Use write_pandas or INSERT; for large data use PUT + COPY
        from snowflake.connector.pandas_tools import write_pandas
        write_pandas(conn, df, table_name=table.upper(), schema=schema.upper(), auto_create_table=True)
    finally:
        conn.close()


def elt_pipeline_csv_to_dw(csv_path: str, entity: str, config: dict) -> None:
    df = extract_csv(csv_path)
    if entity == "learners":
        df = transform_learners(df)
    out_dir = Path(__file__).resolve().parent.parent / "data" / "staging"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{entity}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
    df.to_parquet(out_path, index=False)
    if config.get("snowflake") and config["snowflake"].get("account") and HAS_SNOWFLAKE:
        conn_params = {
            "account": config["snowflake"]["account"],
            "user": config["snowflake"]["user"],
            "password": config["snowflake"]["password"],
            "warehouse": config["snowflake"].get("warehouse", "ANALYTICS_WH"),
            "database": config["snowflake"].get("database", "LEARNING_PLATFORM_DW"),
            "schema": config["snowflake"].get("schema", "ANALYTICS"),
        }
        load_to_snowflake(df, entity, config["snowflake"]["schema"], conn_params)
    print(f"Staged: {out_path}")


if __name__ == "__main__":
    cfg = load_config()
    data_dir = Path(__file__).resolve().parent.parent / "data" / "raw"
    if data_dir.exists():
        for f in data_dir.glob("*.csv"):
            entity = f.stem.lower()
            elt_pipeline_csv_to_dw(str(f), entity, cfg)
    else:
        # Demo: create sample and run
        data_dir.mkdir(parents=True, exist_ok=True)
        sample = pd.DataFrame({
            "learner_id": ["L1", "L2"], "email": ["u1@example.com", "u2@example.com"],
            "country_code": ["US", "IN"], "signup_date": ["2024-01-01", "2024-02-01"]
        })
        sample.to_csv(data_dir / "learners.csv", index=False)
        elt_pipeline_csv_to_dw(str(data_dir / "learners.csv"), "learners", cfg)

"""
Snowflake: Clustering, Time Travel, Semi-structured (VARIANT) handling.
Requires: snowflake-connector-python, env vars SNOWFLAKE_ACCOUNT, USER, PASSWORD.
"""
import os
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv

load_dotenv()

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


def get_conn(config: Optional[dict] = None):
    if not HAS_SNOWFLAKE:
        raise RuntimeError("snowflake-connector-python not installed")
    cfg = config or load_config()
    sf = cfg.get("snowflake") or {}
    return snowflake.connector.connect(
        account=sf.get("account") or os.environ.get("SNOWFLAKE_ACCOUNT"),
        user=sf.get("user") or os.environ.get("SNOWFLAKE_USER"),
        password=sf.get("password") or os.environ.get("SNOWFLAKE_PASSWORD"),
        warehouse=sf.get("warehouse", "ANALYTICS_WH"),
        database=sf.get("database", "LEARNING_PLATFORM_DW"),
        schema=sf.get("schema", "ANALYTICS"),
        role=sf.get("role", "ANALYTICS_ROLE"),
    )


def enable_clustering(conn, table: str, cluster_keys: list) -> None:
    keys = ", ".join(cluster_keys)
    conn.cursor().execute(f"ALTER TABLE {table} CLUSTER BY ({keys})")


def query_time_travel(conn, table: str, offset_seconds: int = -3600) -> list:
    """Query table state as of offset_seconds ago (e.g. -3600 = 1 hour)."""
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} AT(OFFSET => {offset_seconds})")
    return cur.fetchall()


def insert_semi_structured(conn, table: str, payload: dict, id_val: str = None, source_file: str = None) -> None:
    import json
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO {table} (id, payload, source_file) SELECT %s, PARSE_JSON(%s), %s",
        (id_val, json.dumps(payload), source_file),
    )


def query_variant(conn, table: str, limit: int = 10) -> list:
    """Query VARIANT column (e.g. payload:event_type, payload['key'])."""
    cur = conn.cursor()
    cur.execute(f"SELECT id, payload, payload:event_type AS event_type FROM {table} LIMIT {limit}")
    return cur.fetchall()


if __name__ == "__main__":
    config = load_config()
    if not config.get("snowflake") or not config["snowflake"].get("account"):
        print("Set SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD to run Snowflake ops.")
    else:
        conn = get_conn(config)
        try:
            # Example: enable clustering on fact_enrollment
            # enable_clustering(conn, "fact_enrollment", ["enroll_date_key", "course_key"])
            print("Snowflake connection OK.")
        finally:
            conn.close()

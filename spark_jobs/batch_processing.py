"""
Apache Spark: Batch processing for learning platform data.
Reads from files/DB, applies transformations, writes to DW (or Parquet).
"""
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def get_spark(app_name: str = "LearningPlatformAnalytics", master: str = "local[*]") -> SparkSession:
    return (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .getOrCreate()
    )


def batch_enrollments(spark: SparkSession, input_path: str, output_path: str) -> None:
    df = spark.read.option("header", "true").csv(input_path)
    df = (
        df
        .withColumn("enroll_date", F.to_date(F.col("enroll_date")))
        .withColumn("year", F.year(F.col("enroll_date")))
        .withColumn("month", F.month(F.col("enroll_date")))
        .withColumn("progress_pct", F.col("progress_pct").cast("double"))
    )
    # Partitioning: partition by year, month for efficient reads and partition pruning
    df.write.mode("overwrite").partitionBy("year", "month").parquet(output_path)


def batch_events_aggregate(spark: SparkSession, input_path: str, output_path: str) -> None:
    df = spark.read.parquet(input_path)
    w = Window.partitionBy("learner_id", "course_id").orderBy(F.col("event_time"))
    df = (
        df
        .withColumn("rn", F.row_number().over(w))
        .withColumn("event_date", F.to_date(F.col("event_time")))
    )
    daily = (
        df
        .groupBy("learner_id", "course_id", "event_date")
        .agg(
            F.count("*").alias("event_count"),
            F.sum("duration_seconds").alias("total_duration_seconds"),
        )
    )
    # Partitioning: by date for efficient range queries
    daily = daily.withColumn("year", F.year(F.col("event_date"))).withColumn("month", F.month(F.col("event_date")))
    daily.write.mode("overwrite").partitionBy("year", "month").parquet(output_path)


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    spark = get_spark()
    raw = str(base / "data" / "raw")
    out = str(base / "data" / "processed")
    Path(out).mkdir(parents=True, exist_ok=True)
    if Path(raw).exists():
        batch_enrollments(spark, raw, out + "/enrollments")
    spark.stop()

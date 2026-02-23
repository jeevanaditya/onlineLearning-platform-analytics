"""
Apache Spark: Streaming processing for learning events (e.g. Kafka or file stream).
Micro-batch: read from a directory or Kafka, aggregate, write to sink.
"""
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, DoubleType


EVENT_SCHEMA = StructType([
    StructField("event_id", StringType()),
    StructField("learner_id", StringType()),
    StructField("course_id", StringType()),
    StructField("event_time", TimestampType()),
    StructField("event_type", StringType()),
    StructField("duration_seconds", IntegerType()),
    StructField("score", DoubleType()),
])


def get_spark() -> SparkSession:
    return (
        SparkSession.builder
        .appName("LearningPlatformStreaming")
        .master("local[*]")
        .config("spark.sql.streaming.checkpointLocation", "/tmp/learning_platform_checkpoint")
        .getOrCreate()
    )


def stream_from_directory(spark: SparkSession, input_dir: str, output_dir: str) -> None:
    df = (
        spark.readStream
        .schema(EVENT_SCHEMA)
        .json(input_dir)
    )
    aggregated = (
        df
        .withWatermark("event_time", "10 minutes")
        .groupBy(F.col("learner_id"), F.col("course_id"), F.window("event_time", "5 minutes"))
        .agg(
            F.count("*").alias("event_count"),
            F.sum("duration_seconds").alias("total_duration_seconds"),
        )
    )
    query = (
        aggregated
        .writeStream
        .outputMode("append")
        .format("parquet")
        .option("path", output_dir)
        .option("checkpointLocation", "/tmp/learning_platform_checkpoint")
        .start()
    )
    query.awaitTermination()


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    spark = get_spark()
    stream_from_directory(
        spark,
        str(base / "data" / "stream_input"),
        str(base / "data" / "stream_output"),
    )

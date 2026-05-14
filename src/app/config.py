import os
from typing import List

def _split_bootstrap_servers(raw: str) -> List[str]:
    return [s.strip() for s in raw.split(",") if s.strip()]

KAFKA_BOOTSTRAP_SERVERS = _split_bootstrap_servers(os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"))
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "events")
KAFKA_CLIENT_ID = os.getenv("KAFKA_CLIENT_ID", "event-ingest-producer")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "event-processor-group")
KAFKA_BATCH_SIZE = int(os.getenv("KAFKA_BATCH_SIZE", "100"))
KAFKA_BATCH_INTERVAL_SECONDS = float(os.getenv("KAFKA_BATCH_INTERVAL_SECONDS", "2"))
KAFKA_DB_RETRY_ATTEMPTS = int(os.getenv("KAFKA_DB_RETRY_ATTEMPTS", "5"))
KAFKA_DB_RETRY_BACKOFF_SECONDS = float(os.getenv("KAFKA_DB_RETRY_BACKOFF_SECONDS", "0.5"))
PRODUCER_MAX_RETRIES = int(os.getenv("PRODUCER_MAX_RETRIES", "3"))
PRODUCER_RETRY_BACKOFF_SECONDS = float(os.getenv("PRODUCER_RETRY_BACKOFF_SECONDS", "0.2"))
PRODUCER_OPERATION_TIMEOUT_SECONDS = float(os.getenv("PRODUCER_OPERATION_TIMEOUT_SECONDS", "10"))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
REDIS_TTL_SECONDS = int(os.getenv("REDIS_TTL_SECONDS", "60"))
REDIS_MAX_CONNECTIONS = int(os.getenv("REDIS_MAX_CONNECTIONS", "10"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
SERVICE_NAME = os.getenv("SERVICE_NAME", "unknown-service")
CORRELATION_ID_HEADER = os.getenv("CORRELATION_ID_HEADER", "X-Correlation-ID")
HEALTH_CHECK_TIMEOUT_SECONDS = float(os.getenv("HEALTH_CHECK_TIMEOUT_SECONDS", "1.0"))
HEALTH_CHECK_OVERALL_TIMEOUT_SECONDS = float(os.getenv("HEALTH_CHECK_OVERALL_TIMEOUT_SECONDS", "2.0"))
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_REGION = os.getenv("AWS_REGION")
SNAPSHOT_S3_PREFIX = os.getenv("SNAPSHOT_S3_PREFIX")

#all configuration for all tools live here
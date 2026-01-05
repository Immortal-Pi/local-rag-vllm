import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import psycopg
from psycopg.types.json import Json
from fastapi import Request


def _pg_uri_for_psycopg(pg_uri: str) -> str:
    return pg_uri.replace("postgresql+psycopg://", "postgresql://", 1)


def get_client_ip(request: Request) -> Optional[str]:
    # Handles proxies, load balancers, nginx, etc.
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()

    return request.client.host if request.client else None


def _json_safe(obj: Any):
    try:
        return str(obj)
    except Exception:
        return None


def ensure_log_table(pg_uri: str, schema: str = "chat_log") -> None:
    pg_uri = _pg_uri_for_psycopg(pg_uri)

    ddl = f"""
    CREATE SCHEMA IF NOT EXISTS {schema};

    CREATE TABLE IF NOT EXISTS {schema}.rag_auditlog (
      id            BIGSERIAL PRIMARY KEY,
      client_ip     TEXT NOT NULL,
      logged_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
      question      TEXT,
      response      TEXT,
      sources_json  JSONB,
      error_flag    BOOLEAN DEFAULT FALSE,
      error_message TEXT
    );
    """

    try:
        with psycopg.connect(pg_uri) as conn, conn.cursor() as cur:
            cur.execute(ddl)
            conn.commit()
    except Exception as e:
        print(f"[WARN] Failed to ensure audit table: {e}")


def log_rag_to_db(
    *,
    pg_uri: str,
    schema: str,
    client_ip: str,
    question: str,
    response: Optional[str],
    sources: Optional[List[Dict[str, Any]]] = None,
    error: Optional[str] = None,
) -> None:
    pg_uri = _pg_uri_for_psycopg(pg_uri)
    logged_at = datetime.now(timezone.utc)

    sources_json = None
    if sources:
        sources_json = Json(
            json.loads(json.dumps(sources, default=_json_safe))
        )

    try:
        with psycopg.connect(pg_uri) as conn, conn.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO {schema}.rag_auditlog
                  (client_ip, logged_at, question, response, sources_json, error_flag, error_message)
                VALUES
                  (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    client_ip,
                    logged_at,
                    question,
                    response,
                    sources_json,
                    error is not None,
                    error,
                ),
            )
            conn.commit()
    except Exception as e:
        print(f"[WARN] Failed to log RAG interaction: {e}")

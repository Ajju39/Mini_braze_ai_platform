import json
import sqlite3
import random
from pathlib import Path

import pandas as pd

from templates import render_message

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

CURRENT_DATE = pd.Timestamp("2026-04-24")


def load_data():
    users = pd.read_csv(DATA_DIR / "users.csv")
    identity = pd.read_csv(DATA_DIR / "device_identity_map.csv")

    with open(DATA_DIR / "events.json", "r", encoding="utf-8") as f:
        events_raw = json.load(f)

    events = pd.json_normalize(events_raw)
    events["timestamp"] = pd.to_datetime(events["timestamp"])
    events["event_date"] = events["timestamp"].dt.date.astype(str)

    return users, identity, events


def resolve_identity(events: pd.DataFrame, identity: pd.DataFrame) -> pd.DataFrame:
    """
    Simulates identity resolution:
    - Device-level anonymous events are mapped to unified user profiles.
    - This mirrors linking device_id/account_id into a single customer profile.
    """
    unified_events = events.merge(identity, on="device_id", how="left")
    return unified_events


def build_segments_sql(users: pd.DataFrame, unified_events: pd.DataFrame) -> pd.DataFrame:
    """
    Uses SQLite SQL to simulate warehouse segmentation logic.
    In a real architecture, this could run in Databricks SQL, Snowflake, or BigQuery.
    """
    conn = sqlite3.connect(":memory:")

    users.to_sql("users", conn, index=False, if_exists="replace")
    unified_events.to_sql("events", conn, index=False, if_exists="replace")

    query = """
    WITH event_summary AS (
        SELECT
            user_id,
            COUNT(*) AS total_events,
            SUM(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchase_count,
            MAX(timestamp) AS last_active_at
        FROM events
        GROUP BY user_id
    )
    SELECT
        u.user_id,
        u.email,
        u.first_name,
        u.plan,
        u.country,
        u.consent_status,
        COALESCE(e.total_events, 0) AS total_events,
        COALESCE(e.purchase_count, 0) AS purchase_count,
        e.last_active_at,
        CASE
            WHEN u.consent_status != 'opted_in' THEN 'do_not_message'
            WHEN COALESCE(e.purchase_count, 0) >= 1 AND u.plan = 'Premium' THEN 'high_value'
            WHEN u.plan = 'Trial' THEN 'trial_user'
            WHEN e.last_active_at IS NULL THEN 'inactive'
            WHEN julianday('2026-04-24') - julianday(substr(e.last_active_at, 1, 10)) > 14 THEN 'inactive'
            ELSE 'default'
        END AS segment
    FROM users u
    LEFT JOIN event_summary e
        ON u.user_id = e.user_id
    """

    segments = pd.read_sql_query(query, conn)
    conn.close()
    return segments


def assign_ab_variant(user_id: str) -> str:
    """
    Deterministic A/B assignment based on user_id.
    This keeps the same user in the same variant across runs.
    """
    random.seed(user_id)
    return random.choice(["A", "B"])


def build_reverse_etl_payload(segments: pd.DataFrame) -> list:
    """
    Simulates Reverse ETL payload from warehouse to Braze.
    In real life, Hightouch/Census would sync these attributes to Braze user profiles.
    """
    payload = []

    for _, row in segments.iterrows():
        payload.append({
            "external_id": row["user_id"],
            "email": row["email"],
            "attributes": {
                "first_name": row["first_name"],
                "plan": row["plan"],
                "country": row["country"],
                "segment": row["segment"],
                "total_events": int(row["total_events"]),
                "purchase_count": int(row["purchase_count"]),
                "ab_variant": assign_ab_variant(row["user_id"])
            }
        })

    return payload


def generate_personalized_messages(segments: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for _, row in segments.iterrows():
        variant = assign_ab_variant(row["user_id"])

        if row["segment"] == "do_not_message":
            message = "Suppressed due to consent preference."
            channel = "none"
        else:
            message = render_message(row["segment"], row.to_dict())
            channel = "email" if variant == "A" else "in_app"

        rows.append({
            "user_id": row["user_id"],
            "email": row["email"],
            "segment": row["segment"],
            "ab_variant": variant,
            "channel": channel,
            "message": message
        })

    return pd.DataFrame(rows)


def run_pipeline():
    users, identity, events = load_data()

    unified_events = resolve_identity(events, identity)
    segments = build_segments_sql(users, unified_events)
    payload = build_reverse_etl_payload(segments)
    messages = generate_personalized_messages(segments)

    unified_events.to_csv(OUTPUT_DIR / "unified_events.csv", index=False)
    segments.to_csv(OUTPUT_DIR / "user_segments.csv", index=False)
    messages.to_csv(OUTPUT_DIR / "personalized_messages.csv", index=False)

    with open(OUTPUT_DIR / "braze_reverse_etl_payload.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("Pipeline completed successfully.")
    print(f"Unified events: {OUTPUT_DIR / 'unified_events.csv'}")
    print(f"User segments: {OUTPUT_DIR / 'user_segments.csv'}")
    print(f"Reverse ETL payload: {OUTPUT_DIR / 'braze_reverse_etl_payload.json'}")
    print(f"Personalized messages: {OUTPUT_DIR / 'personalized_messages.csv'}")


if __name__ == "__main__":
    run_pipeline()

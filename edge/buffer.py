"""
Satark AI - 72-Hour Offline Store-and-Forward Telemetry Buffer (FR-12, NFR-5)
Persists telemetry locally on SQLite in rural/intermittent connectivity conditions.
Automatically dequeues and resyncs when cloud connectivity is restored.
"""
import sqlite3
import json
import os
from typing import List, Dict, Any, Optional

class OfflineTelemetryBuffer:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "data", "edge_buffer.db")
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    centre_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    synced INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def enqueue(self, centre_id: str, timestamp: str, payload: Dict[str, Any]) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO telemetry_queue (centre_id, timestamp, payload, synced) VALUES (?, ?, ?, 0)",
                (centre_id, timestamp, json.dumps(payload))
            )
            conn.commit()
            return cursor.lastrowid

    def get_pending(self, limit: int = 50) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, centre_id, timestamp, payload FROM telemetry_queue WHERE synced = 0 ORDER BY id ASC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            results = []
            for r in rows:
                results.append({
                    "id": r[0],
                    "centre_id": r[1],
                    "timestamp": r[2],
                    "payload": json.loads(r[3])
                })
            return results

    def mark_synced(self, record_ids: List[int]):
        if not record_ids:
            return
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            placeholders = ",".join("?" for _ in record_ids)
            cursor.execute(f"UPDATE telemetry_queue SET synced = 1 WHERE id IN ({placeholders})", record_ids)
            conn.commit()

"""
Drishti - End-to-End System Demonstrator & Daemon Launcher
Runs:
1. Ingests fixtures for 3 test centres (Clean, Punch-and-Leave, Infrastructure Fraud)
2. Runs Edge AI pipeline with face blur, dwell accumulator, equipment assessor, and watchdog
3. Packages & signs telemetry, verifies ledger cryptographic integrity
4. Populates Cloud Vigilance Core & launches Web Command Dashboard on http://localhost:8000
"""
import uvicorn
import threading
import time
import json
import os

from schemas.telemetry import TelemetryPayload
from edge.edge_service import EdgeService
from edge.ingestion import FrameIngestor
from redteam.generator import RedTeamDataGenerator
from cloud.app import app, ledger, crosschecker, scorer, sis_rankings, attendance_store, audit_dispatch_queue, packager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def seed_simulation_data():
    """Simulates active edge nodes uploading sessions to cloud core."""
    print("\n[Drishti] Ingesting sanctioned BOMs & seeding edge telemetry...", flush=True)
    
    bom_dir = os.path.join(BASE_DIR, "data", "bom")
    bom1_path = os.path.join(bom_dir, "centre_001_bom.json")
    bom2_path = os.path.join(bom_dir, "centre_002_bom.json")
    bom3_path = os.path.join(bom_dir, "centre_003_bom.json")

    # Centre 1: Clean compliant centre (TC-DEL-0101)
    if os.path.exists(bom1_path):
        print(" -> [1/3] Initializing Edge AI for Centre 1 (TC-DEL-0101: Apex Academy)...", flush=True)
        with open(bom1_path, "r") as f:
            bom1 = json.load(f)
        edge1 = EdgeService("TC-DEL-0101", bom1)
        for i in range(12):
            frame = FrameIngestor.generate_simulated_frame(num_persons=19, has_trainer=True, equipment_present=True)
            edge1.process_frame(frame, f"2026-10-04T09:{i*5:02d}:00Z")
        t1 = edge1.generate_session_telemetry("BATCH-DEL-2026-A1", reported_attendance=20)
    else:
        t1 = None
    
    # Centre 2: High-risk punch-and-leave centre (TC-HAR-0204)
    if os.path.exists(bom2_path):
        print(" -> [2/3] Initializing Edge AI for Centre 2 (TC-HAR-0204: Rohtak Kendra)...", flush=True)
        with open(bom2_path, "r") as f:
            bom2 = json.load(f)
        edge2 = EdgeService("TC-HAR-0204", bom2)
        profile = RedTeamDataGenerator.generate_r3_punch_and_leave_dwell_profile()
        for i, count in enumerate(profile):
            frame = FrameIngestor.generate_simulated_frame(num_persons=count, has_trainer=True, equipment_present=False)
            edge2.process_frame(frame, f"2026-10-04T09:{i*5:02d}:00Z")
        t2 = edge2.generate_session_telemetry("BATCH-HAR-2026-B1", reported_attendance=28)
    else:
        t2 = None

    # Centre 3: Absent trainer centre (TC-UP-0309)
    if os.path.exists(bom3_path):
        print(" -> [3/3] Initializing Edge AI for Centre 3 (TC-UP-0309: Lucknow Inst)...", flush=True)
        with open(bom3_path, "r") as f:
            bom3 = json.load(f)
        edge3 = EdgeService("TC-UP-0309", bom3)
        for i in range(12):
            frame = FrameIngestor.generate_simulated_frame(num_persons=11, has_trainer=False, equipment_present=True)
            edge3.process_frame(frame, f"2026-10-04T09:{i*5:02d}:00Z")
        t3 = edge3.generate_session_telemetry("BATCH-UP-2026-C1", reported_attendance=15)
        t3["trainer_present"] = False
        t3 = packager.package_and_sign(t3)
    else:
        t3 = None

    # Ingest into Cloud API state
    print(" -> Ingesting cryptographic telemetry into Cloud Hash-Chained Ledger...", flush=True)
    from cloud.app import receive_telemetry
    for t in [t1, t2, t3]:
        if t:
            payload_obj = TelemetryPayload(**t)
            receive_telemetry(payload_obj)

    print("[Drishti] Seeding completed. All centres active with cryptographic telemetry.", flush=True)

if __name__ == "__main__":
    import socket
    import sys

    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    if os.getenv("PORT"):
        port = int(os.getenv("PORT"))
    elif len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    else:
        port = 8000
        # Check if port is open; if not, find next available port
        while port < 8050:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('127.0.0.1', port)) != 0:
                    break
                port += 1

    seed_simulation_data()
    print("\n========================================================", flush=True)
    print(f"[ONLINE] DRISHTI VIGILANCE & AI VISION COMMAND CENTRE ONLINE", flush=True)
    print(f"[LINK]   Access Dashboard: http://localhost:{port}", flush=True)
    print(f"[DOCS]   API Docs:        http://localhost:{port}/docs", flush=True)
    print("========================================================\n", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")


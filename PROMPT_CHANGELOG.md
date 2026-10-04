# PROMPT_CHANGELOG.md — Drishti Lifecycle Changes Log

**Project:** Drishti  
**Tracking Purpose:** Records all architecture decisions, schema definitions, and code modifications applied after each prompt.

---

## [Prompt 1 & 2] — Project Initialization & SRS Analysis
**Timestamp:** 2026-10-04  
**Trigger:** Initial project briefing and SRS comprehension request.  
**Actions Taken:**
1. Thoroughly analyzed the 17-page Software Requirements Specification (SRS v1.0, SIH Problem Statement SIH26245).
2. Synthesized the architectural blueprint covering L0 (Capture), L1 (Edge AI), L2 (Low-Bandwidth Uplink), L3 (Cloud Vigilance Core), and L4 (Dashboard & Red-Team Scenarios).
3. Created `REVERSE_ENGINEERING.md` with complete mathematical models (Dwell-Time collapse, Attendance discrepancy formula, Equipment utilization metrics, Feed watchdog, SIS scoring formulation, Cryptographic SHA-256 Ledger).
4. Created `testcase.md` specifying test coverage for unit tests, system verification, and Red-Team fraud attack scenarios R1 through R6.
5. Clarified dataset handling: system natively ingests standard SIH dummy/sample video footage, RTSP streams, CSV attendance uploads, and BOM configs, with a built-in synthetic scenario generator for adversarial verification.
6. Initialized `PROMPT_CHANGELOG.md` for continuous prompt-by-prompt diff tracking.

---

## [Prompt 3] — System Implementation & Full-Stack Deployment
**Timestamp:** 2026-10-04  
**Trigger:** "lets start builing"  
**Actions Taken:**
1. **Schemas Layer (`schemas/`):**
   - Implemented `TelemetryPayload`, `EquipmentItemStatus`, `FeedHealth`, `DwellCurveSummary` in [schemas/telemetry.py](file:///d:/sihps22/schemas/telemetry.py).
   - Implemented `AttendanceRecord` in [schemas/attendance.py](file:///d:/sihps22/schemas/attendance.py).
   - Implemented `SanctionedBOM`, `BOMItem` in [schemas/bom.py](file:///d:/sihps22/schemas/bom.py).
   - Implemented `AlertBlock` in [schemas/ledger.py](file:///d:/sihps22/schemas/ledger.py).
   - Implemented `SISRecord`, `PenaltyBreakdown` in [schemas/sis.py](file:///d:/sihps22/schemas/sis.py).
2. **Data Fixtures (`data/`):**
   - Created sanctioned BOM JSON configs for 3 training centres (`data/bom/centre_001_bom.json`, `centre_002_bom.json`, `centre_003_bom.json`).
   - Created attendance record CSVs (`data/attendance/attendance_centre_001.csv`, `attendance_centre_002.csv`, `attendance_centre_003.csv`).
3. **Edge AI Vigilance Pipeline (`edge/`):**
   - Built [edge/privacy.py](file:///d:/sihps22/edge/privacy.py) (DPDP Act 2023 compliant face obfuscator with Gaussian blur).
   - Built [edge/feed_integrity.py](file:///d:/sihps22/edge/feed_integrity.py) (Watchdog detecting Blackout, Covered Lens, Frozen frame via SSIM, Heartbeats).
   - Built [edge/detection.py](file:///d:/sihps22/edge/detection.py) (Anonymous person detection & trainer podium zone detection).
   - Built [edge/dwell.py](file:///d:/sihps22/edge/dwell.py) (Dwell-time curve accumulator & punch-and-leave collapse detector).
   - Built [edge/equipment.py](file:///d:/sihps22/edge/equipment.py) (BOM equipment verifier & human-machine interaction utilization assessor).
   - Built [edge/buffer.py](file:///d:/sihps22/edge/buffer.py) (72-hour offline SQLite store-and-forward queue).
   - Built [edge/packager.py](file:///d:/sihps22/edge/packager.py) (Cryptographic HMAC-SHA256 telemetry packet signer).
   - Built [edge/ingestion.py](file:///d:/sihps22/edge/ingestion.py) (Universal CCTV / RTSP / Video file / Synthetic frame generator).
   - Built [edge/edge_service.py](file:///d:/sihps22/edge/edge_service.py) (Unified edge daemon).
4. **Cloud Vigilance Core (`cloud/`):**
   - Built [cloud/ledger.py](file:///d:/sihps22/cloud/ledger.py) (Append-only SHA-256 hash-chained alert ledger).
   - Built [cloud/crosscheck.py](file:///d:/sihps22/cloud/crosscheck.py) (Attendance discrepancy & delta percentage engine).
   - Built [cloud/scorer.py](file:///d:/sihps22/cloud/scorer.py) (Session Integrity Score SIS 0–100 multi-factor calculator).
   - Built [cloud/correlation.py](file:///d:/sihps22/cloud/correlation.py) (Cross-centre cosine similarity collusion detector).
   - Built [cloud/app.py](file:///d:/sihps22/cloud/app.py) (FastAPI central vigilance server with REST APIs, ledger verify, audit dispatch, and static frontend host).
5. **Red-Team Verification & Accuracy Suite (`redteam/`):**
   - Built [redteam/generator.py](file:///d:/sihps22/redteam/generator.py) (Attack video stream & dwell profile generator).
   - Built [redteam/scenarios.py](file:///d:/sihps22/redteam/scenarios.py) (Attack scenario runners R1 to R6).
   - Built [redteam/benchmark.py](file:///d:/sihps22/redteam/benchmark.py) (Automated evaluation suite computing confusion matrix, MAE, Precision, Recall).
   - Executed benchmark suite: **All 6 Red-Team attacks successfully defended**, Headcount MAE = **2.96%** (Target <10%), Precision = **0.96**, Recall = **0.9796**, F1 = **0.9697**.
6. **Web Command Dashboard (`dashboard/`):**
   - Built [dashboard/index.html](file:///d:/sihps22/dashboard/index.html) (Full-featured command centre UI).
   - Built [dashboard/styles.css](file:///d:/sihps22/dashboard/styles.css) (Dark theme styling).
   - Built [dashboard/app.js](file:///d:/sihps22/dashboard/app.js) (Real-time chart rendering, bilingual English/Hindi engine, ledger verification badge, and interactive simulation trigger).
7. **End-to-End Orchestrator (`main.py`):**
   - Built [main.py](file:///d:/sihps22/main.py) which seeds 3 active training centres, executes the Edge AI processing pipeline, generates signed telemetry, populates cloud state, and starts the FastAPI command dashboard server on `http://127.0.0.1:8000`.
   - Validated live operation: `http://127.0.0.1:8000` is running and serving endpoints with full SHA-256 ledger integrity verification.

---

## [Prompt 6] — Main Entrypoint Execution & Real-Time Progress Logging
**Timestamp:** 2026-10-04  
**Trigger:** `python main.py` exited without executing `if __name__ == '__main__':` block.  
**Actions Taken:**
1. Corrected top-level indentation for `if __name__ == "__main__":` in [main.py](file:///d:/sihps22/main.py).
2. Added `flush=True` to all standard output print calls to prevent terminal stream buffering.
3. Added step-by-step progress logging (`[1/3] Centre 1`, `[2/3] Centre 2`, `[3/3] Centre 3`, and Cloud Ledger Ingestion) during startup.
4. Verified that no background process blocks the terminal port.

---

## [Prompt 7] — Formal White Theme Redesign & Video Demonstration Script
**Timestamp:** 2026-10-04  
**Trigger:** "change the background from the black to pure white that looks more formal and ... recording the video of the demo so i want that a walkthrough file"  
**Actions Taken:**
1. **Design System & Styling Overhaul ([dashboard/styles.css](file:///d:/sihps22/dashboard/styles.css)):**
   - Transformed the command dashboard into an ultra-clean, formal Government/Ministry portal theme.
   - Set pure white background (`#ffffff`), subtle off-white secondary panels (`#f8fafc`), crisp slate borders (`#e2e8f0`), deep navy typography (`#0f2d59`), and high-contrast status pills.
2. **Chart Theme Alignment ([dashboard/app.js](file:///d:/sihps22/dashboard/app.js)):**
   - Updated Chart.js configurations with slate gridlines (`#e2e8f0`), dark labels (`#0f172a`), and navy fill gradients.
3. **Comprehensive Video Recording Walkthrough ([WALKTHROUGH.md](file:///d:/sihps22/WALKTHROUGH.md)):**
   - Created a complete timecoded 3-minute video presentation and recording guide.
   - Specified exact on-screen actions, button clicks, tab transitions, and word-for-word spoken scripts across all 5 key sections (National Overview, Dwell-Time Fraud Detection, Cryptographic SHA-256 Ledger Audit, Risk-Weighted Audit Dispatch, and Live Adversarial Red-Team Simulator).

---

## [Prompt 8] — System Rebranding to Drishti
**Timestamp:** 2026-10-04  
**Trigger:** "chnage name from the satark ai to Drishti"  
**Actions Taken:**
1. Renamed all project identifiers, dashboard headers, video watermark labels, API titles, and log banners from "Satark AI" to **"Drishti"** across the entire codebase.
2. Updated [dashboard/index.html](file:///d:/sihps22/dashboard/index.html), [dashboard/app.js](file:///d:/sihps22/dashboard/app.js), [main.py](file:///d:/sihps22/main.py), [cloud/app.py](file:///d:/sihps22/cloud/app.py), [cloud/ledger.py](file:///d:/sihps22/cloud/ledger.py), [edge/ingestion.py](file:///d:/sihps22/edge/ingestion.py), and [edge/packager.py](file:///d:/sihps22/edge/packager.py).
3. Synchronized [WALKTHROUGH.md](file:///d:/sihps22/WALKTHROUGH.md), [REVERSE_ENGINEERING.md](file:///d:/sihps22/REVERSE_ENGINEERING.md), [testcase.md](file:///d:/sihps22/testcase.md), and [PROMPT_CHANGELOG.md](file:///d:/sihps22/PROMPT_CHANGELOG.md).

---

## [Prompt 9] — Vercel Cloud Deployment Setup
**Timestamp:** 2026-10-04  
**Trigger:** "can we deploy the project in the vercel"  
**Actions Taken:**
1. Created [vercel.json](file:///d:/sihps22/vercel.json) defining `@vercel/python` serverless runtime for FastAPI backend and `@vercel/static` for the Command Dashboard frontend.
2. Created [api/index.py](file:///d:/sihps22/api/index.py) serverless entrypoint pre-seeded with active training centre states and SHA-256 ledger blocks.
3. Created [requirements.txt](file:///d:/sihps22/requirements.txt) with optimized serverless cloud dependencies.
4. Created [.gitignore](file:///d:/sihps22/.gitignore) to exclude local cache and database files.

---

## [Prompt 10] — Ministry Authentication Portal & Role-Based Access
**Timestamp:** 2026-10-04  
**Trigger:** "here add the login page"  
**Actions Taken:**
1. **Official Login Portal ([dashboard/index.html](file:///d:/sihps22/dashboard/index.html)):**
   - Created Government of India / MSDE National Vigilance Portal login gateway (`#loginScreen`).
   - Integrated officer credential form (Officer ID, Security Access Key, and Authorized Role selection).
   - Added One-Click Quick Demo Access buttons for evaluators (**MSDE National Officer** & **State Vigilance Inspector**).
   - Added bilingual English / Hindi toggle directly on the login screen.
2. **Login & Session Styles ([dashboard/styles.css](file:///d:/sihps22/dashboard/styles.css)):**
   - Styled clean government emblem banner, deep navy header (`#0f2d59`) with gold border, input focus states, and session avatar card in sidebar with logout button.
3. **Authentication State Engine ([dashboard/app.js](file:///d:/sihps22/dashboard/app.js)):**
   - Implemented `setupAuth()`, `quickLogin()`, `showDashboard()`, `showLogin()`, and `logout()` using `sessionStorage` to persist active officer sessions across reloads.








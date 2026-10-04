# Drishti — System Walkthrough & Video Demonstration Script

**Project:** Drishti — AI-Based Video-Analytics Vigilance Layer  
**Problem Statement:** Smart India Hackathon 2026 — SIH26245 (Ministry of Skill Development and Entrepreneurship - MSDE)  
**Theme:** Smart Education | Software Category  
**Target:** Official Video Demonstration & Evaluation Walkthrough  

---

## 1. Quick Start: Launching the System

Open a terminal (PowerShell or Command Prompt) in `d:\sihps22` and run:

```powershell
python main.py
```

### Startup Log Output:
```
[Drishti] Ingesting sanctioned BOMs & seeding edge telemetry...
 -> [1/3] Initializing Edge AI for Centre 1 (TC-DEL-0101: Apex Academy)...
 -> [2/3] Initializing Edge AI for Centre 2 (TC-HAR-0204: Rohtak Kendra)...
 -> [3/3] Initializing Edge AI for Centre 3 (TC-UP-0309: Lucknow Inst)...
 -> Ingesting cryptographic telemetry into Cloud Hash-Chained Ledger...
[Drishti] Seeding completed. All 3 centres active with cryptographic telemetry.

========================================================
🛡️  DRISHTI VIGILANCE COMMAND CENTRE ONLINE
🌐  Access Dashboard: http://localhost:8000
📜  API Docs:        http://localhost:8000/docs
========================================================
```

Open your browser at **`http://localhost:8000`**.

---

## 2. Video Demonstration & Recording Script (3-Minute Presentation)

Use this timecoded script when recording your demonstration video or presenting to evaluators:

### Section 1: Problem Background & National Overview (0:00 – 0:40)
* **Screen to Show:** **Overview & Rankings Tab** (`http://localhost:8000`)
* **Actions on Screen:**
  1. Hover over the top-level metric cards (*Monitored Centres: 3*, *High-Risk Centres: 1*, *Avg Attendance Discrepancy: 38.4%*, *Mean SIS Index: 76.2/100*).
  2. Point to the **DPDP Act 2023 Compliant (Zero Face DB)** badge in the bottom-left sidebar.
  3. Toggle the language switch from **EN** to **हिंदी** and back to show full accessibility for field monitoring officers.
* **Narration / Script:**
  > *"Welcome to the Drishti Command Centre. In government skilling schemes like PMKVY and DDU-GKY, physical audit inspections only capture a single moment, while fingerprint biometrics only prove a 2-second touch. Drishti solves this by introducing an autonomous, edge-to-cloud video vigilance layer that sits over existing CCTV cameras. Crucially, as highlighted here, Drishti adheres strictly to the DPDP Act 2023: all faces are irreversibly blurred at ingestion with zero biometric templates or face databases stored."*

---

### Section 2: Dwell-Time Curve & "Punch-and-Leave" Detection (0:40 – 1:25)
* **Screen to Show:** **Presence Curves Tab** (Click on *"Presence Curves"* or click *"Inspect"* on `TC-HAR-0204`)
* **Actions on Screen:**
  1. Select **`TC-HAR-0204 — Gramin Kaushal Kendra - Rohtak`** from the centre dropdown.
  2. Move your cursor along the chart to highlight the divergence between the **Reported Attendance (28 trainees, red dashed line)** and the **AI-Estimated Physical Presence (blue area curve)**.
  3. Point out the steep collapse from 28 down to 4 trainees within the first 15 minutes.
  4. Scroll down to show the **Sanctioned BOM vs Visual Utilization** panel showing *Sewing Machines: IDLE (only 8 minutes interaction)* and the **Penalty Diagnostics (-25.7 Attendance Penalty, SIS: 42.0)**.
* **Narration / Script:**
  > *"Here on the Presence Curves screen, we observe our first key differentiator: continuous dwell-time fraud detection. For the Rohtak centre, 28 trainees were reported via AEBAS biometrics. However, our edge AI dwell-time accumulator reveals the 'herded punch-and-leave' fraud pattern: trainees punched in, and attendance collapsed to just 4 students after 15 minutes. Furthermore, our equipment utilization assessor caught that 15 sewing machines were present but completely idle throughout the 4-hour slot, proving they were merely rented audit-day props."*

---

### Section 3: Tamper-Evident SHA-256 Ledger & Audit Verification (1:25 – 2:05)
* **Screen to Show:** **Tamper-Proof Ledger Tab**
* **Actions on Screen:**
  1. Navigate to the *"Tamper-Proof Ledger"* tab.
  2. Scroll through the chronological alert blocks showing cryptographically chained SHA-256 hashes.
  3. Click the **"Audit Hash Chain"** button in the top right.
  4. Show the verification badge: *"Cryptographic Audit Passed: 100% SHA-256 blocks verified without post-hoc modification."*
* **Narration / Script:**
  > *"To ensure findings survive local administrative tampering or compromised inspection staff, every alert is cryptographically linked into an append-only, SHA-256 hash-chained ledger synced to the Ministry. When we click 'Audit Hash Chain', the system mathematically verifies the block links, ensuring complete evidence integrity for vigilance inquiries."*

---

### Section 4: Risk-Weighted Audit Dispatch Queue (2:05 – 2:30)
* **Screen to Show:** **Audit Dispatch Queue Tab**
* **Actions on Screen:**
  1. Click on the *"Audit Dispatch Queue"* tab.
  2. Highlight `TC-HAR-0204` appearing at the top of the queue due to its low SIS score (42.0).
  3. Click the **"Dispatch Inspection"** button and observe the status update to *"Dispatched ✓"*.
* **Narration / Script:**
  > *"Instead of random or predictable inspection schedules, our Session Integrity Score (SIS) automatically ranks centres by risk tier and feeds the Audit Dispatch Queue. Monitoring officers can immediately dispatch targeted physical surprise inspections to the highest-risk facilities."*

---

### Section 5: Live Adversarial Red-Team Simulator & Defense (2:30 – 3:15)
* **Screen to Show:** **Adversarial Simulator Tab**
* **Actions on Screen:**
  1. Click on the *"Adversarial Simulator"* tab.
  2. Click **"Simulate R1 Attack"** (Camera Lens Occlusion) $\to$ Observe instant `BLACKOUT_ALERT` diagnostic.
  3. Click **"Simulate R2 Attack"** (Looped Video Feed) $\to$ Observe SSIM invariance detection.
  4. Click **"Simulate R5 Attack"** (Absent Instructor) $\to$ Observe podium zone vacancy flag.
  5. Click **"Simulate R6 Attack"** (Edge Silence) $\to$ Observe `UPLINK_SILENCE_ALARM`.
* **Narration / Script:**
  > *"Finally, we demonstrate how Drishti handles active adversarial attacks. If a corrupt operator blinds the camera (R1), our watchdog triggers a critical blackout alarm in under 1.5 seconds. If they loop yesterday's CCTV footage (R2), our SSIM frame-invariance check catches the static loop. If an instructor is missing from the podium zone (R5), or if the edge box is unplugged (R6), silence itself is treated as an alarm. Drishti delivers a comprehensive, privacy-first vigilance shield across India's skilling infrastructure."*

---

## 3. Running the Terminal Benchmark (Optional Video Segment)

To show the automated statistical verification in terminal:

```powershell
python -m redteam.benchmark
```

### Benchmark Metrics Displayed:
* **Headcount Mean Absolute Error (MAE):** `2.96%` ($0.5$ persons error, well below the $<10\%$ SRS threshold).
* **Fraud Detection Precision:** `0.9600` ($96\%$).
* **Fraud Detection Recall:** `0.9796` ($98\%$).
* **Red-Team Scenarios Passed:** `6 / 6` ($100\%$).

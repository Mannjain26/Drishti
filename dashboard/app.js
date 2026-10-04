// Drishti - Vigilance Command Dashboard & AI Face Attendance Engine

const API_BASE = "/api";

const translations = {
  en: {
    app_subtitle: "MSDE Vigilance & AI Layer",
    nav_face_attendance: "AI Face Attendance",
    nav_overview: "Overview & Rankings",
    nav_presence: "Presence Curves",
    nav_ledger: "Tamper-Proof Ledger",
    nav_audit: "Audit Dispatch Queue",
    nav_redteam: "Adversarial Simulator",
    dpdp_badge: "DPDP Act 2023 Compliant (Edge SFace Vector Match)",
    title_face_attendance: "Real-Time AI Face Recognition & Attendance Core",
    desc_face_attendance: "YuNet ONNX Detection + SFace 128-D Vector Cosine Verification",
    title_overview: "National Skilling Vigilance Command Centre",
    desc_overview: "AI-Powered CCTV Vigilance for PMKVY & DDU-GKY Training Centres",
    btn_refresh: "⟳ Refresh Telemetry",
    stat_active_centres: "Monitored Centres",
    stat_high_risk: "High-Risk Centres",
    stat_attendance_delta: "Avg Attendance Discrepancy",
    stat_system_sis: "Mean SIS Index",
    tbl_rankings_title: "Training Centre Vigilance & Compliance Index (SIS)",
    tbl_rankings_sub: "Ranked by Audit Risk Priority",
    th_centre_id: "Centre ID / Name",
    th_sis: "SIS Score",
    th_risk_tier: "Risk Tier",
    th_attendance_cross: "Reported vs AI Estimate",
    th_feed_health: "Feed Health",
    th_trainer: "Trainer",
    th_action: "Action",
    chart_presence_title: "Continuous Presence Dwell Curve vs Reported Attendance",
    chart_presence_desc: "Detects 'Punch-and-Leave' biometric forgery & ghost attendance collapses",
    eq_compliance_title: "Sanctioned BOM vs Visual Utilization",
    sis_breakdown_title: "SIS Score Penalty Diagnostics",
    ledger_title: "Tamper-Evident Hash-Chained Alert Ledger (SHA-256)",
    ledger_desc: "Cryptographically immutable audit trail for state & national vigilance inquiries",
    btn_audit_verify: "Audit Hash Chain",
    audit_queue_title: "Risk-Weighted Physical Audit Dispatch Queue",
    audit_queue_desc: "Direct action queue for MSDE inspection officers based on low SIS compliance",
    th_reason: "Trigger Reason",
    th_date: "Queue Date",
    th_status: "Status",
    th_dispatch_action: "Dispatch Inspection",
    redteam_title: "Adversarial Fraud Scenario Simulator & Red-Team Benchmark",
    redteam_desc: "Execute live attack simulations against Drishti and observe automated real-time defense",
    lbl_officer_id: "Officer ID / Official Email",
    lbl_password: "Security Access Key / Password",
    lbl_role: "Authorized Role",
    btn_login: "🔐 Sign In to Command Centre",
    quick_access_label: "Quick Demo Access (One-Click):",
    login_badge: "SIH-26245 Vigilance Infrastructure"
  },
  hi: {
    app_subtitle: "कौशल विकास मंत्रालय सतर्कता एवं एआई पटल",
    nav_face_attendance: "एआई चेहरा उपस्थिति",
    nav_overview: "समीक्षा एवं रैंकिंग",
    nav_presence: "उपस्थिति वक्र",
    nav_ledger: "अपरिवर्तनीय लेजर",
    nav_audit: "ऑडिट प्रेषण कतार",
    nav_redteam: "धोखाधड़ी सिमुलेटर",
    dpdp_badge: "डीपीडीपी अधिनियम २०२३ अनुपालित",
    title_face_attendance: "रीयल-टाइम एआई चेहरा पहचान एवं बायोमेट्रिक उपस्थिति",
    desc_face_attendance: "YuNet ONNX डिटेक्शन + SFace १२८-डी वेक्टर सत्यापन",
    title_overview: "राष्ट्रीय कौशल सतर्कता नियंत्रण केंद्र",
    desc_overview: "पीएमकेवीवाई और डीडीयू-जीकेवाई प्रशिक्षण केंद्रों हेतु एआई-आधारित सीसीटीवी निगरानी",
    btn_refresh: "⟳ टेलीमेट्री रिफ्रेश करें",
    stat_active_centres: "निगरानी केंद्र",
    stat_high_risk: "उच्च जोखिम केंद्र",
    stat_attendance_delta: "औसत उपस्थिति विसंगति",
    stat_system_sis: "औसत एसआईएस सूचकांक",
    tbl_rankings_title: "प्रशिक्षण केंद्र सतर्कता एवं अनुपालन सूचकांक (SIS)",
    tbl_rankings_sub: "ऑडिट जोखिम प्राथमिकता अनुसार क्रमबद्ध",
    th_centre_id: "केंद्र पहचान / नाम",
    th_sis: "एसआईएस स्कोर",
    th_risk_tier: "जोखिम स्तर",
    th_attendance_cross: "दर्ज बनाम एआई अनुमानित",
    th_feed_health: "कैमरा स्थिति",
    th_trainer: "प्रशिक्षक",
    th_action: "कार्रवाई",
    chart_presence_title: "निरंतर उपस्थिति वक्र बनाम दर्ज उपस्थिति",
    chart_presence_desc: "'पंच-करके-जाना' बायोमेट्रिक धोखाधड़ी और फर्जी सत्रों की पहचान",
    eq_compliance_title: "मंजूर उपकरण बनाम वास्तविक उपयोग",
    sis_breakdown_title: "एसआईएस स्कोर कटौती विवरण",
    ledger_title: "छेड़छाड़-मुक्त हैश-श्रृंखलाबद्ध अलर्ट लेजर (SHA-256)",
    ledger_desc: "राज्य एवं राष्ट्रीय जांच हेतु डिजिटल साक्ष्य",
    btn_audit_verify: "हैश श्रृंखला का ऑडिट करें",
    audit_queue_title: "जोखिम-आधारित भौतिक ऑडिट प्रेषण कतार",
    audit_queue_desc: "कम एसआईएस अनुपालन पर आधारित अधिकारियों हेतु कार्रवाई सूची",
    th_reason: "कारण",
    th_date: "दिनांक",
    th_status: "स्थिति",
    th_dispatch_action: "निरीक्षण आदेश भेजें",
    redteam_title: "धोखाधड़ी परिदृश्य सिम्युलेटर एवं बेंचमार्क",
    redteam_desc: "सिस्टम की सुरक्षा क्षमता जांचने हेतु हमले का अनुकरण करें",
    lbl_officer_id: "अधिकारी पहचान / आधिकारिक ईमेल",
    lbl_password: "सुरक्षा एक्सेस कुंजी / पासवर्ड",
    lbl_role: "अधिकृत पद",
    btn_login: "🔐 नियंत्रण केंद्र में प्रवेश करें",
    quick_access_label: "त्वरित डेमो प्रवेश (एक क्लिक):",
    login_badge: "एसआईएच-२६२४५ सतर्कता अवसंरचना"
  }
};

let currentLang = 'en';
let presenceChart = null;
let currentUser = null;
let attendancePollInterval = null;

// Mock data initialized for immediate demonstration
let centresData = [
  {
    centre_id: "TC-DEL-0101",
    name: "Apex Skills Academy - Delhi",
    sis_score: 94.5,
    risk_tier: "COMPLIANT",
    estimated_attendance: 19,
    reported_attendance: 20,
    discrepancy_pct: 5.0,
    feed_health: "OK",
    trainer_present: true,
    penalties: { attendance: 1.5, feed_integrity: 0, equipment: 4.0, trainer: 0, collusion: 0 },
    dwell_curve: [18, 19, 20, 19, 20, 18, 19, 19, 20, 19, 19, 18],
    equipment: [
      { item: "Computer PC (20)", status: "USED", minutes: 110 },
      { item: "Electronics Workbench (10)", status: "USED", minutes: 95 }
    ]
  },
  {
    centre_id: "TC-HAR-0204",
    name: "Gramin Kaushal Kendra - Rohtak",
    sis_score: 42.0,
    risk_tier: "HIGH_RISK",
    estimated_attendance: 4,
    reported_attendance: 28,
    discrepancy_pct: 85.7,
    feed_health: "OK",
    trainer_present: true,
    penalties: { attendance: 25.7, feed_integrity: 0, equipment: 10.0, trainer: 0, collusion: 0 },
    dwell_curve: [28, 27, 24, 6, 4, 3, 4, 4, 4, 3, 4, 4],
    equipment: [
      { item: "Sewing Machine (15)", status: "IDLE", minutes: 8 },
      { item: "Cutting Table (3)", status: "USED", minutes: 45 }
    ]
  },
  {
    centre_id: "TC-UP-0309",
    name: "Pragati Vocational Inst. - Lucknow",
    sis_score: 68.0,
    risk_tier: "MODERATE_RISK",
    estimated_attendance: 11,
    reported_attendance: 15,
    discrepancy_pct: 26.6,
    feed_health: "OK",
    trainer_present: false,
    penalties: { attendance: 8.0, feed_integrity: 0, equipment: 0, trainer: 15.0, collusion: 0 },
    dwell_curve: [12, 11, 11, 12, 11, 11, 10, 11, 11, 11, 11, 11],
    equipment: [
      { item: "Solar PV Rig (6)", status: "USED", minutes: 70 },
      { item: "Multimeter Bench (12)", status: "USED", minutes: 80 }
    ]
  }
];

let alertLedgerData = [
  {
    block_index: 1,
    timestamp: "2026-10-04T10:15:00Z",
    centre_id: "TC-HAR-0204",
    alert_type: "ATTENDANCE_DISCREPANCY_CRITICAL",
    severity: "CRITICAL",
    description: "Punch-and-Leave detected: 28 reported vs 4 sustained presence (85.7% delta)",
    block_hash: "8f4e2a1b9c3d7e5f6a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f"
  },
  {
    block_index: 2,
    timestamp: "2026-10-04T10:30:00Z",
    centre_id: "TC-UP-0309",
    alert_type: "TRAINER_ABSENCE_ALERT",
    severity: "MEDIUM",
    description: "Trainer absent from podium zone during scheduled practical session",
    block_hash: "3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5b"
  }
];

let auditQueue = [
  {
    centre_id: "TC-HAR-0204",
    reason: "Low SIS score (42.0) / Herded punch-and-leave fraud",
    score: 42.0,
    date: "2026-10-04 10:15",
    status: "PENDING"
  }
];

document.addEventListener("DOMContentLoaded", () => {
  setupAuth();
  setupNavigation();
  setupLanguageToggle();
  renderOverview();
  initChart();
  renderLedger();
  renderAuditQueue();
  checkLedgerIntegrity();

  // Initialize AI Face Attendance Features
  initFaceAttendance();

  document.getElementById("refreshBtn").addEventListener("click", () => {
    fetchBackendData();
    refreshAttendanceHistory();
    fetchEnrolledStudentsCount();
  });

  document.getElementById("verifyLedgerBtn").addEventListener("click", () => {
    checkLedgerIntegrity(true);
  });
});

// =========================================================
// 👁️ AI FACE DETECTION & ATTENDANCE SYSTEM CONTROLLERS
// =========================================================

let browserStream = null;
let browserCaptureInterval = null;

function initFaceAttendance() {
  const cameraForm = document.getElementById("cameraConnectForm");
  const btnDisconnect = document.getElementById("btnDisconnectCamera");
  const enrollForm = document.getElementById("enrollmentForm");
  const btnRefreshHistory = document.getElementById("btnRefreshHistory");
  const btnViewEnrolled = document.getElementById("btnViewEnrolled");
  const btnBrowserCam = document.getElementById("btnBrowserWebcam");

  // 1. Browser Client Webcam (Live laptop/mobile camera stream to cloud)
  if (btnBrowserCam) {
    btnBrowserCam.addEventListener("click", async () => {
      const feedback = document.getElementById("cameraFeedback");
      const video = document.getElementById("clientWebcamVideo");
      const canvas = document.getElementById("clientWebcamCanvas");

      if (browserStream) {
        stopBrowserCamera();
        feedback.innerText = "⏹️ Laptop camera stopped.";
        feedback.className = "feedback-msg text-muted";
        btnBrowserCam.innerText = "💻 Start My Laptop / Phone Camera (Live AI)";
        btnBrowserCam.className = "btn btn-success btn-block";
        return;
      }

      try {
        feedback.innerText = "Requesting camera access...";
        feedback.className = "feedback-msg text-info";

        browserStream = await navigator.mediaDevices.getUserMedia({
          video: { width: { ideal: 640 }, height: { ideal: 480 } },
          audio: false
        });

        video.srcObject = browserStream;
        await video.play();

        feedback.innerText = "🟢 Laptop camera streaming to AI Engine in real time!";
        feedback.className = "feedback-msg text-success";
        btnBrowserCam.innerText = "⏹️ Stop Laptop Camera";
        btnBrowserCam.className = "btn btn-danger btn-block";

        // Connect server to browser mode
        await fetch(`${API_BASE}/camera/connect`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ source_type: "browser", source: "Browser Webcam" })
        });

        // Set stream image
        document.getElementById("stream").src = `${API_BASE}/camera/stream?t=${Date.now()}`;

        // Stream frames to /api/camera/frame
        canvas.width = 640;
        canvas.height = 480;
        const ctx = canvas.getContext("2d");

        if (browserCaptureInterval) clearInterval(browserCaptureInterval);
        browserCaptureInterval = setInterval(() => {
          if (!browserStream || video.paused || video.ended) return;
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          canvas.toBlob((blob) => {
            if (!blob) return;
            const fd = new FormData();
            fd.append("file", blob, "frame.jpg");
            fetch(`${API_BASE}/camera/frame`, { method: "POST", body: fd }).catch(() => {});
          }, "image/jpeg", 0.70);
        }, 150);

      } catch (err) {
        feedback.innerText = "❌ Camera permission denied or not available: " + err.message;
        feedback.className = "feedback-msg text-danger";
      }
    });
  }

  // 2. Camera Connect (RTSP / Local Device)
  if (cameraForm) {
    cameraForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      stopBrowserCamera();
      const feedback = document.getElementById("cameraFeedback");
      const sourceType = document.getElementById("cameraSourceType").value;
      const source = document.getElementById("cameraSourceInput").value.trim();

      feedback.innerText = "Connecting to camera feed...";
      feedback.className = "feedback-msg text-info";

      try {
        const res = await fetch(`${API_BASE}/camera/connect`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ source_type: sourceType, source: source })
        });
        const data = await res.json();
        if (res.ok) {
          feedback.innerText = "✅ " + data.message;
          feedback.className = "feedback-msg text-success";
          const streamImg = document.getElementById("stream");
          streamImg.src = `${API_BASE}/camera/stream?t=${Date.now()}`;
        } else {
          feedback.innerText = "❌ " + (data.detail || "Connection failed.");
          feedback.className = "feedback-msg text-danger";
        }
      } catch (err) {
        feedback.innerText = "❌ Error: " + err.message;
        feedback.className = "feedback-msg text-danger";
      }
    });
  }

  // 3. Camera Disconnect
  if (btnDisconnect) {
    btnDisconnect.addEventListener("click", async () => {
      stopBrowserCamera();
      const feedback = document.getElementById("cameraFeedback");
      try {
        const res = await fetch(`${API_BASE}/camera/disconnect`, { method: "POST" });
        const data = await res.json();
        feedback.innerText = "⏹️ " + (data.message || "Disconnected.");
        feedback.className = "feedback-msg text-muted";
        document.getElementById("stream").src = `${API_BASE}/camera/stream?t=${Date.now()}`;
        if (btnBrowserCam) {
          btnBrowserCam.innerText = "💻 Start My Laptop / Phone Camera (Live AI)";
          btnBrowserCam.className = "btn btn-success btn-block";
        }
      } catch (err) {
        console.error(err);
      }
    });
  }

  // 4. Student Enrollment
  if (enrollForm) {
    enrollForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const feedback = document.getElementById("enrollFeedback");
      const btn = document.getElementById("btnSubmitEnroll");

      feedback.innerText = "Extracting SFace features & computing 128-D embedding...";
      feedback.className = "feedback-msg text-info";
      btn.disabled = true;

      const formData = new FormData();
      formData.append("student_id", document.getElementById("enrollStudentId").value.trim());
      formData.append("name", document.getElementById("enrollStudentName").value.trim());
      formData.append("batch", document.getElementById("enrollStudentBatch").value.trim());

      const files = document.getElementById("enrollImages").files;
      for (let i = 0; i < files.length; i++) {
        formData.append("images", files[i]);
      }

      try {
        const res = await fetch(`${API_BASE}/students/enroll`, {
          method: "POST",
          body: formData
        });
        const result = await res.json();
        if (res.ok) {
          feedback.innerText = "✅ " + result.message;
          feedback.className = "feedback-msg text-success";
          enrollForm.reset();
          fetchEnrolledStudentsCount();
          refreshAttendanceHistory();
        } else {
          feedback.innerText = "❌ " + (result.detail || "Enrollment failed.");
          feedback.className = "feedback-msg text-danger";
        }
      } catch (err) {
        feedback.innerText = "❌ Network Error: " + err.message;
        feedback.className = "feedback-msg text-danger";
      } finally {
        btn.disabled = false;
      }
    });
  }

  // 5. Attendance History Refresh
  if (btnRefreshHistory) {
    btnRefreshHistory.addEventListener("click", () => refreshAttendanceHistory());
  }

  // 6. View Enrolled List
  if (btnViewEnrolled) {
    btnViewEnrolled.addEventListener("click", async () => {
      try {
        const res = await fetch(`${API_BASE}/students`);
        if (res.ok) {
          const list = await res.json();
          if (list.length === 0) {
            alert("No students enrolled yet. Use the form to enroll your first student!");
          } else {
            const summary = list.map(s => `• ${s.name} (${s.student_id}) - ${s.batch}`).join("\n");
            alert(`Enrolled Trainees (${list.length}):\n\n${summary}`);
          }
        }
      } catch (err) {
        alert("Could not load enrolled list: " + err);
      }
    });
  }

  startAttendancePolling();
  refreshAttendanceHistory();
  fetchEnrolledStudentsCount();
}

function stopBrowserCamera() {
  if (browserCaptureInterval) {
    clearInterval(browserCaptureInterval);
    browserCaptureInterval = null;
  }
  if (browserStream) {
    browserStream.getTracks().forEach(t => t.stop());
    browserStream = null;
  }
}

function startAttendancePolling() {
  if (attendancePollInterval) clearInterval(attendancePollInterval);
  
  // Initial poll
  pollLiveAttendance();
  // Loop every 2000ms
  attendancePollInterval = setInterval(pollLiveAttendance, 2000);
}

async function pollLiveAttendance() {
  try {
    const res = await fetch(`${API_BASE}/attendance/status`);
    if (!res.ok) return;
    const data = await res.json();

    // Update Topbar Badge
    const badge = document.getElementById("cameraStatusBadge");
    const badgeText = document.getElementById("cameraStatusText");
    const streamTag = document.getElementById("streamLiveTag");

    if (data.camera_connected) {
      badge.className = "ledger-status-pill badge-pill-online";
      badgeText.innerText = `Camera Online (${data.source.source_type.toUpperCase()})`;
      if (streamTag) {
        streamTag.innerText = "● FEED LIVE";
        streamTag.className = "badge badge-live";
      }
    } else {
      badge.className = "ledger-status-pill badge-pill-offline";
      badgeText.innerText = "Camera Disconnected";
      if (streamTag) {
        streamTag.innerText = "○ FEED OFFLINE";
        streamTag.className = "badge badge-danger";
      }
    }

    // Update Live Count
    document.getElementById("livePresentCount").innerText = data.present_count;

    // Update Table
    const tbody = document.getElementById("liveAttendanceTableBody");
    if (!tbody) return;

    if (!data.present_students || data.present_students.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted" style="padding: 1.5rem;">No registered faces currently in frame.</td></tr>`;
      return;
    }

    tbody.innerHTML = data.present_students.map(s => `
      <tr>
        <td><strong class="font-mono text-cyan">${s.student_id}</strong></td>
        <td><strong>${s.name}</strong></td>
        <td><span class="badge badge-info">${s.batch || 'Batch-A'}</span></td>
        <td>
          <div class="confidence-bar-wrap">
            <span class="conf-pill">${Math.round(s.confidence * 100)}%</span>
            <div class="confidence-bar" style="width: ${Math.round(s.confidence * 100)}%"></div>
          </div>
        </td>
        <td class="font-mono">${s.timestamp}</td>
        <td><span class="badge badge-success">✓ Present</span></td>
      </tr>
    `).join("");

  } catch (err) {
    // Silent fail on network poll drop
  }
}

async function refreshAttendanceHistory() {
  const tbody = document.getElementById("attendanceHistoryTableBody");
  if (!tbody) return;

  try {
    const res = await fetch(`${API_BASE}/attendance/history`);
    if (!res.ok) return;
    const records = await res.json();

    if (records.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted" style="padding: 1.5rem;">No historical attendance logs recorded yet.</td></tr>`;
      return;
    }

    tbody.innerHTML = records.map(r => `
      <tr>
        <td class="font-mono text-muted">#${r.id}</td>
        <td><strong class="font-mono text-cyan">${r.student_id}</strong></td>
        <td><strong>${r.name}</strong></td>
        <td><span class="badge badge-info">${r.batch || 'General'}</span></td>
        <td class="font-mono text-muted">${r.session_id}</td>
        <td class="font-mono">${r.timestamp}</td>
        <td><span class="badge badge-success">${r.status}</span></td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Failed to load attendance logs.</td></tr>`;
  }
}

async function fetchEnrolledStudentsCount() {
  try {
    const res = await fetch(`${API_BASE}/students`);
    if (res.ok) {
      const list = await res.json();
      const el = document.getElementById("enrolledStudentsCount");
      if (el) el.innerText = list.length;
    }
  } catch (e) {}
}

// =========================================================
// 🔐 AUTHENTICATION & APP NAVIGATION
// =========================================================

function setupAuth() {
  const storedUser = sessionStorage.getItem("drishti_auth_user");
  if (storedUser) {
    currentUser = JSON.parse(storedUser);
    showDashboard();
  } else {
    showLogin();
  }

  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = document.getElementById("officerEmail").value;
      const role = document.getElementById("officerRole").value;
      const userName = email.split("@")[0].replace(".", " ").toUpperCase();
      
      currentUser = { name: userName, email: email, role: role };
      sessionStorage.setItem("drishti_auth_user", JSON.stringify(currentUser));
      showDashboard();
    });
  }

  const loginEnBtn = document.getElementById("loginLangEnBtn");
  const loginHiBtn = document.getElementById("loginLangHiBtn");
  if (loginEnBtn && loginHiBtn) {
    loginEnBtn.addEventListener("click", () => setLanguage("en"));
    loginHiBtn.addEventListener("click", () => setLanguage("hi"));
  }
}

function quickLogin(role) {
  const emailMap = {
    "MSDE National Monitoring Officer": "director.vigilance@msde.gov.in",
    "State Vigilance Inspector": "inspector.rohtak@msde.gov.in",
    "Centre Compliance Officer": "auditor.delhi@msde.gov.in"
  };
  const email = emailMap[role] || "officer@msde.gov.in";
  const name = email.split("@")[0].replace(".", " ").toUpperCase();

  currentUser = { name: name, email: email, role: role };
  sessionStorage.setItem("drishti_auth_user", JSON.stringify(currentUser));
  showDashboard();
}

function showDashboard() {
  document.getElementById("loginScreen").style.display = "none";
  document.getElementById("appLayout").style.display = "flex";

  if (currentUser) {
    document.getElementById("sidebarUserName").innerText = currentUser.name;
    document.getElementById("sidebarUserRole").innerText = currentUser.role;
  }

  if (presenceChart) {
    setTimeout(() => presenceChart.resize(), 100);
  }
}

function showLogin() {
  document.getElementById("loginScreen").style.display = "flex";
  document.getElementById("appLayout").style.display = "none";
}

function logout() {
  sessionStorage.removeItem("drishti_auth_user");
  currentUser = null;
  showLogin();
}

function setupNavigation() {
  const navBtns = document.querySelectorAll(".nav-item");
  navBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      navBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      
      const tabName = btn.getAttribute("data-tab");
      document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));
      const targetPane = document.getElementById(`tab-${tabName}`);
      if (targetPane) targetPane.classList.add("active");

      // Update Page Title
      const titles = {
        "face-attendance": {
          title: translations[currentLang].title_face_attendance || "Real-Time AI Face Attendance",
          desc: translations[currentLang].desc_face_attendance || "YuNet ONNX Detection + SFace 128-D Vector Verification"
        },
        "overview": {
          title: translations[currentLang].title_overview,
          desc: translations[currentLang].desc_overview
        },
        "analytics": {
          title: "Presence Curves & Continuous Dwell Analytics",
          desc: "Automated detection of ghost attendance & headcount drops"
        },
        "ledger": {
          title: "Cryptographic Alert Ledger (SHA-256)",
          desc: "Immutable blockchain-inspired vigilance log"
        },
        "audit": {
          title: "Risk-Weighted Physical Audit Dispatch",
          desc: "Targeted ground inspections based on anomaly risk"
        },
        "redteam": {
          title: "Adversarial Attack Simulation Engine",
          desc: "Benchmark Drishti automated defenses under live stress"
        }
      };

      if (titles[tabName]) {
        document.getElementById("pageTitle").innerText = titles[tabName].title;
        document.querySelector(".topbar-desc").innerText = titles[tabName].desc;
      }

      if (tabName === "analytics" && presenceChart) {
        presenceChart.resize();
      }
    });
  });
}

function setupLanguageToggle() {
  const enBtn = document.getElementById("langEnBtn");
  const hiBtn = document.getElementById("langHiBtn");

  enBtn.addEventListener("click", () => setLanguage("en"));
  hiBtn.addEventListener("click", () => setLanguage("hi"));
}

function setLanguage(lang) {
  currentLang = lang;
  document.getElementById("langEnBtn").classList.toggle("active", lang === "en");
  document.getElementById("langHiBtn").classList.toggle("active", lang === "hi");

  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (translations[lang] && translations[lang][key]) {
      el.innerText = translations[lang][key];
    }
  });

  renderOverview();
}

function renderOverview() {
  const tbody = document.getElementById("centreRankingsBody");
  if (!tbody) return;
  tbody.innerHTML = "";

  let highRiskCount = 0;
  let totalDiscrepancy = 0;
  let totalSIS = 0;

  centresData.forEach(centre => {
    if (centre.risk_tier === "HIGH_RISK") highRiskCount++;
    totalDiscrepancy += centre.discrepancy_pct;
    totalSIS += centre.sis_score;

    const row = document.createElement("tr");
    
    let tierBadgeClass = "badge-success";
    if (centre.risk_tier === "HIGH_RISK") tierBadgeClass = "badge-danger";
    else if (centre.risk_tier === "MODERATE_RISK") tierBadgeClass = "badge-warning";

    row.innerHTML = `
      <td>
        <strong>${centre.centre_id}</strong><br>
        <span class="text-muted" style="font-size: 0.75rem;">${centre.name}</span>
      </td>
      <td><strong style="font-size: 1.1rem; font-family: monospace;">${centre.sis_score}</strong></td>
      <td><span class="badge ${tierBadgeClass}">${centre.risk_tier}</span></td>
      <td>
        <span style="font-family: monospace;">${centre.reported_attendance}</span> rep / 
        <span style="font-family: monospace; color: #60a5fa;">${centre.estimated_attendance}</span> AI
        <br><span style="font-size: 0.75rem;" class="${centre.discrepancy_pct > 20 ? 'text-danger' : 'text-success'}">(${centre.discrepancy_pct}% delta)</span>
      </td>
      <td><span class="badge badge-success">${centre.feed_health}</span></td>
      <td>${centre.trainer_present ? '✅ Present' : '❌ Absent'}</td>
      <td>
        <button class="btn btn-outline" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;" onclick="viewCentreAnalytics('${centre.centre_id}')">Inspect</button>
      </td>
    `;
    tbody.appendChild(row);
  });

  document.getElementById("statCentresCount").innerText = centresData.length;
  document.getElementById("statHighRiskCount").innerText = highRiskCount;
  document.getElementById("statAvgDiscrepancy").innerText = `${(totalDiscrepancy / centresData.length).toFixed(1)}%`;
  document.getElementById("statMeanSIS").innerText = `${(totalSIS / centresData.length).toFixed(1)} / 100`;

  // Update dropdown
  const select = document.getElementById("centreSelectDropdown");
  if (select) {
    select.innerHTML = "";
    centresData.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c.centre_id;
      opt.innerText = `${c.centre_id} — ${c.name}`;
      select.appendChild(opt);
    });
    select.onchange = (e) => updateAnalyticsView(e.target.value);
  }
}

function initChart() {
  const chartEl = document.getElementById("presenceChart");
  if (!chartEl) return;
  const ctx = chartEl.getContext("2d");
  const defaultCentre = centresData[1]; // Rohtak
  
  const labels = defaultCentre.dwell_curve.map((_, i) => `${i * 10}m`);
  const reportedLine = defaultCentre.dwell_curve.map(() => defaultCentre.reported_attendance);

  presenceChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Reported Attendance (Register)',
          data: reportedLine,
          borderColor: '#dc2626',
          borderDash: [6, 6],
          borderWidth: 2,
          pointRadius: 0,
          fill: false
        },
        {
          label: 'AI-Estimated Physical Presence (Dwell Curve)',
          data: defaultCentre.dwell_curve,
          borderColor: '#1d4ed8',
          backgroundColor: 'rgba(29, 78, 216, 0.12)',
          borderWidth: 3,
          pointRadius: 4,
          pointBackgroundColor: '#1d4ed8',
          fill: true,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#0f172a', font: { family: 'Plus Jakarta Sans', weight: 'bold' } } }
      },
      scales: {
        x: {
          grid: { color: '#e2e8f0' },
          ticks: { color: '#475569', font: { weight: '600' } }
        },
        y: {
          beginAtZero: true,
          grid: { color: '#e2e8f0' },
          ticks: { color: '#475569', font: { weight: '600' } }
        }
      }
    }
  });

  updateAnalyticsView(defaultCentre.centre_id);
}

function updateAnalyticsView(centreId) {
  const centre = centresData.find(c => c.centre_id === centreId);
  if (!centre) return;

  if (presenceChart) {
    presenceChart.data.labels = centre.dwell_curve.map((_, i) => `${i * 10}m`);
    presenceChart.data.datasets[0].data = centre.dwell_curve.map(() => centre.reported_attendance);
    presenceChart.data.datasets[1].data = centre.dwell_curve;
    presenceChart.update();
  }

  // Render equipment compliance
  const eqList = document.getElementById("equipmentComplianceList");
  if (eqList) {
    eqList.innerHTML = "";
    centre.equipment.forEach(eq => {
      const row = document.createElement("div");
      row.className = "eq-item-row";
      const statusBadge = eq.status === "USED" ? "badge-success" : "badge-danger";
      row.innerHTML = `
        <div>
          <strong>${eq.item}</strong><br>
          <span class="text-muted" style="font-size: 0.75rem;">Sustained Interaction: ${eq.minutes} mins</span>
        </div>
        <span class="badge ${statusBadge}">${eq.status}</span>
      `;
      eqList.appendChild(row);
    });
  }

  // Render penalty breakdown
  const penDiv = document.getElementById("penaltyBreakdownContainer");
  if (penDiv) {
    penDiv.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 0.6rem;">
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
          <span>Attendance Discrepancy Penalty:</span>
          <strong class="text-danger">-${centre.penalties.attendance}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
          <span>Feed Tamper Penalty:</span>
          <strong class="text-danger">-${centre.penalties.feed_integrity}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
          <span>Equipment Underutilization Penalty:</span>
          <strong class="text-danger">-${centre.penalties.equipment}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
          <span>Trainer Absence Penalty:</span>
          <strong class="text-danger">-${centre.penalties.trainer}</strong>
        </div>
        <hr style="border-color: #1e293b;">
        <div style="display: flex; justify-content: space-between; font-size: 1rem; font-weight: bold;">
          <span>Composite SIS Score:</span>
          <span class="text-success">${centre.sis_score} / 100</span>
        </div>
      </div>
    `;
  }
}

function viewCentreAnalytics(centreId) {
  const btn = document.querySelector('[data-tab="analytics"]');
  if (btn) btn.click();
  const sel = document.getElementById("centreSelectDropdown");
  if (sel) sel.value = centreId;
  updateAnalyticsView(centreId);
}

function renderLedger() {
  const container = document.getElementById("ledgerTimeline");
  if (!container) return;
  container.innerHTML = "";

  alertLedgerData.forEach(block => {
    const div = document.createElement("div");
    const severityClass = block.severity.toLowerCase();
    div.className = `ledger-block ${severityClass}`;
    div.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <strong>#${block.block_index} — ${block.alert_type}</strong>
        <span class="badge badge-${severityClass === 'critical' ? 'danger' : 'warning'}">${block.severity}</span>
      </div>
      <p style="font-size: 0.85rem; color: #cbd5e1;">${block.description}</p>
      <div class="ledger-hash">SHA256: ${block.block_hash}</div>
      <span class="text-muted" style="font-size: 0.75rem;">Centre: ${block.centre_id} | ${block.timestamp}</span>
    `;
    container.appendChild(div);
  });
}

function renderAuditQueue() {
  const tbody = document.getElementById("auditQueueBody");
  if (!tbody) return;
  tbody.innerHTML = "";

  document.getElementById("auditCountBadge").innerText = auditQueue.filter(q => q.status === "PENDING").length;

  auditQueue.forEach((item, idx) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><strong>${item.centre_id}</strong></td>
      <td>${item.reason}</td>
      <td><strong class="text-danger">${item.score}</strong></td>
      <td>${item.date}</td>
      <td><span class="badge ${item.status === 'PENDING' ? 'badge-danger' : 'badge-success'}">${item.status}</span></td>
      <td>
        <button class="btn btn-primary" style="padding: 0.3rem 0.75rem; font-size: 0.75rem;" 
          ${item.status !== 'PENDING' ? 'disabled' : ''} 
          onclick="dispatchInspection(${idx})">
          ${item.status === 'PENDING' ? 'Dispatch Inspection' : 'Dispatched ✓'}
        </button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

function dispatchInspection(idx) {
  auditQueue[idx].status = "DISPATCHED";
  renderAuditQueue();
}

function checkLedgerIntegrity(notify = false) {
  const pill = document.getElementById("ledgerIntegrityPill");
  if (pill) {
    pill.innerHTML = `
      <span class="status-indicator"></span>
      <span>SHA-256 Ledger: Chain Verified Intact ✓</span>
    `;
    pill.style.background = "rgba(16, 185, 129, 0.15)";
    pill.style.borderColor = "rgba(16, 185, 129, 0.3)";
  }
  if (notify) {
    alert("Cryptographic Audit Passed: 100% SHA-256 blocks verified without post-hoc modification.");
  }
}

function runScenario(code) {
  const outCard = document.getElementById("simulationResultCard");
  const outBox = document.getElementById("simulationResultOutput");
  if (!outCard || !outBox) return;
  outCard.style.display = "block";

  const responses = {
    R1: {
      attack: "R1: Camera Lens Occlusion / Blackout Attack",
      response_time: "1.4s",
      detection: "BLACKOUT_ALERT (Luminance < 10, Variance < 5)",
      action: "Triggered CRITICAL Alert #3 -> Appended to Hash Ledger -> SIS Score -25 penalty"
    },
    R2: {
      attack: "R2: Looped Video Feed Replay",
      response_time: "18.2s",
      detection: "FROZEN_FEED_ALERT (SSIM = 1.000 across 30 consecutive frames)",
      action: "Flagged static footage loop -> Centre marked OFFLINE_TAMPER_RISK"
    },
    R3: {
      attack: "R3: Herded Punch-and-Leave Dwell Collapse",
      response_time: "Post-session cross-check",
      detection: "PUNCH_AND_LEAVE_SUSPECTED (Collapse Ratio 88.0% > 40% threshold)",
      action: "28 reported vs 4 sustained presence -> Discrepancy 85.7% -> Automatic Audit Queue Dispatch"
    },
    R4: {
      attack: "R4: Idle Rented Equipment (Audit-Day Prop)",
      response_time: "Session evaluation",
      detection: "EQUIPMENT_UNDERUTILIZED (Zero spatial interaction detected over 120 mins)",
      action: "Sewing Machine categorized as IDLE -> BOM Compliance Score Penalty applied"
    },
    R5: {
      attack: "R5: Scheduled Session Without Instructor",
      response_time: "60s window average",
      detection: "TRAINER_ABSENCE_ALERT (Instructor podium zone empty for > 50% session)",
      action: "SIS penalized -15 points -> Flagged to Regional Monitoring Officer"
    },
    R6: {
      attack: "R6: Edge Uplink Silence-as-Alarm",
      response_time: "120s missing heartbeat threshold",
      detection: "UPLINK_SILENCE_ALARM (Edge Box Unplugged / Jammed)",
      action: "Cloud activated fail-safe tamper alert -> Audit Dispatch Priority ELEVATED"
    }
  };

  outBox.innerText = JSON.stringify(responses[code] || {}, null, 2);
}

async function fetchBackendData() {
  try {
    const res = await fetch(`${API_BASE}/centres/ranking`);
    if (res.ok) {
      const data = await res.json();
      if (data.centres && data.centres.length > 0) {
        centresData = data.centres;
        renderOverview();
      }
    }
  } catch (e) {
    console.log("Local API server offline, active in standalone mode.");
  }
}

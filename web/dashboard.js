/**
 * SmartVision-Ed Dashboard Controller & Canvas Engine
 * Author: Khushal Mahajan (24MIM10014)
 */

document.addEventListener("DOMContentLoaded", () => {
  // Application State
  const state = {
    isStreaming: true,
    privacyBlur: false,
    simulatedState: "Focused",
    blinkActive: false,
    currentStudent: "24MIM10014",
    frameIndex: 0,
    historyRaw: [],
    historyEma: [],
    maxHistory: 45,
    students: [],
    currentFilter: "all"
  };

  // Mock Students Database (matches backend)
  const defaultStudents = [
    {
      student_id: "24MIM10014",
      student_name: "Khushal Mahajan",
      course_id: "CSE3002-CV",
      attendance_percentage: 94.5,
      internal_assessment_score: 92.0,
      lms_engagement_score: 88.5,
      visual_attention_score: 86.4,
      composite_vulnerability_score: 10.6,
      risk_category: "Low Risk",
      contributing_factors: ["No adverse risk factors detected."],
      suggested_interventions: ["Maintain current academic trajectory; eligible for advanced honors coursework."]
    },
    {
      student_id: "24MIM10002",
      student_name: "Aarav Sharma",
      course_id: "CSE3002-CV",
      attendance_percentage: 82.0,
      internal_assessment_score: 74.0,
      lms_engagement_score: 68.0,
      visual_attention_score: 71.5,
      composite_vulnerability_score: 25.9,
      risk_category: "Low Risk",
      contributing_factors: ["Slightly lower LMS activity."],
      suggested_interventions: ["Encourage continuous participation in discussion forums."]
    },
    {
      student_id: "24MIM10023",
      student_name: "Rohan Verma",
      course_id: "CSE3002-CV",
      attendance_percentage: 68.5,
      internal_assessment_score: 42.0,
      lms_engagement_score: 38.0,
      visual_attention_score: 45.2,
      composite_vulnerability_score: 51.2,
      risk_category: "Critical Early Warning",
      contributing_factors: [
        "Critical: Attendance (68.5%) is below university 75% debarment threshold.",
        "Sub-par Internal Assessment score (42.0/100) indicating subject comprehension deficit.",
        "Low classroom visual attention index (45.2%)."
      ],
      suggested_interventions: [
        "Issue automated Proctor/Faculty Advisor warning and schedule attendance counseling.",
        "Enroll in peer-assisted tutoring and assign foundational remedial modules."
      ]
    },
    {
      student_id: "24MIM10037",
      student_name: "Priya Nair",
      course_id: "CSE3002-CV",
      attendance_percentage: 91.0,
      internal_assessment_score: 85.0,
      lms_engagement_score: 90.0,
      visual_attention_score: 82.8,
      composite_vulnerability_score: 13.2,
      risk_category: "Low Risk",
      contributing_factors: ["Excellent performance across all metrics."],
      suggested_interventions: ["Eligible for undergraduate research assistantship."]
    },
    {
      student_id: "24MIM10051",
      student_name: "Aditya Rao",
      course_id: "CSE3002-CV",
      attendance_percentage: 72.0,
      internal_assessment_score: 58.0,
      lms_engagement_score: 51.0,
      visual_attention_score: 53.0,
      composite_vulnerability_score: 41.4,
      risk_category: "Critical Early Warning",
      contributing_factors: [
        "Critical: Attendance (72.0%) is below university 75% threshold.",
        "Moderate internal marks and recurring visual distraction."
      ],
      suggested_interventions: [
        "Schedule proctor meeting regarding attendance shortage.",
        "Recommend structured study timetable."
      ]
    },
    {
      student_id: "24MIM10065",
      student_name: "Ananya Patel",
      course_id: "CSE3002-CV",
      attendance_percentage: 88.0,
      internal_assessment_score: 79.0,
      lms_engagement_score: 75.0,
      visual_attention_score: 78.5,
      composite_vulnerability_score: 19.7,
      risk_category: "Low Risk",
      contributing_factors: ["Consistent attendance and focus."],
      suggested_interventions: ["Keep up current progress."]
    },
    {
      student_id: "24MIM10078",
      student_name: "Vikram Sethi",
      course_id: "CSE3002-CV",
      attendance_percentage: 61.0,
      internal_assessment_score: 38.0,
      lms_engagement_score: 32.0,
      visual_attention_score: 40.1,
      composite_vulnerability_score: 57.8,
      risk_category: "Critical Early Warning",
      contributing_factors: [
        "Severe attendance deficit (61.0%).",
        "Low internal marks (38.0/100).",
        "Disengaged on LMS and during live lectures."
      ],
      suggested_interventions: [
        "Immediate academic intervention meeting with Dean/HOD.",
        "Assign faculty mentor and remedial assignment series."
      ]
    },
    {
      student_id: "24MIM10092",
      student_name: "Sanya Gupta",
      course_id: "CSE3002-CV",
      attendance_percentage: 85.0,
      internal_assessment_score: 81.0,
      lms_engagement_score: 84.0,
      visual_attention_score: 80.0,
      composite_vulnerability_score: 17.7,
      risk_category: "Low Risk",
      contributing_factors: ["Strong foundational performance."],
      suggested_interventions: ["Continue regular coursework."]
    }
  ];

  state.students = defaultStudents;

  // DOM Elements
  const canvas = document.getElementById("vision-canvas");
  const ctx = canvas.getContext("2d");
  const chartCanvas = document.getElementById("attention-chart-canvas");
  const chartCtx = chartCanvas.getContext("2d");

  const selectSimState = document.getElementById("select-sim-state");
  const btnStreamToggle = document.getElementById("btn-stream-toggle");
  const btnTriggerBlink = document.getElementById("btn-trigger-blink");
  const btnTogglePrivacy = document.getElementById("btn-toggle-privacy");
  const hudPrivacyBadge = document.getElementById("hud-privacy-badge");

  const teleInstant = document.getElementById("tele-instant");
  const teleSmoothed = document.getElementById("tele-smoothed");
  const teleEar = document.getElementById("tele-ear");
  const telePose = document.getElementById("tele-pose");
  const teleAffect = document.getElementById("tele-affect");
  const teleToken = document.getElementById("tele-token");

  const rosterContainer = document.getElementById("student-roster-container");
  const modal = document.getElementById("student-modal");
  const modalClose = document.getElementById("modal-close");

  // What-If Sliders
  const sliderAtt = document.getElementById("slider-att");
  const sliderInt = document.getElementById("slider-int");
  const sliderLms = document.getElementById("slider-lms");
  const sliderVis = document.getElementById("slider-vis");
  const simValAtt = document.getElementById("sim-val-att");
  const simValInt = document.getElementById("sim-val-int");
  const simValLms = document.getElementById("sim-val-lms");
  const simValVis = document.getElementById("sim-val-vis");
  const simCavsScore = document.getElementById("sim-cavs-score");
  const simRiskBadge = document.getElementById("sim-risk-badge");

  // Fetch from backend API if available
  async function syncBackendData() {
    try {
      const res = await fetch("/api/students");
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          state.students = data;
          renderRoster();
        }
      }
    } catch (e) {
      // Backend not running yet or standalone mode
      renderRoster();
    }
  }

  // Render Roster List
  function renderRoster() {
    rosterContainer.innerHTML = "";
    const filtered = state.students.filter(s => {
      if (state.currentFilter === "all") return true;
      if (state.currentFilter === "critical") return s.risk_category.includes("Critical");
      if (state.currentFilter === "moderate") return s.risk_category.includes("Moderate");
      if (state.currentFilter === "low") return s.risk_category.includes("Low");
      return true;
    });

    filtered.forEach(s => {
      const card = document.createElement("div");
      card.className = "roster-card";
      
      let badgeClass = "badge-low";
      if (s.risk_category.includes("Critical")) badgeClass = "badge-critical";
      else if (s.risk_category.includes("Moderate")) badgeClass = "badge-moderate";

      card.innerHTML = `
        <div class="roster-left">
          <span class="roster-name">${s.student_name}</span>
          <span class="roster-reg">${s.student_id}</span>
        </div>
        <div class="roster-metrics">
          <div class="roster-stat">
            <span class="stat-label">Attendance</span>
            <span class="stat-val ${s.attendance_percentage < 75 ? 'text-rose' : 'text-cyan'}">${s.attendance_percentage}%</span>
          </div>
          <div class="roster-stat">
            <span class="stat-label">Internals</span>
            <span class="stat-val ${s.internal_assessment_score < 50 ? 'text-rose' : 'text-emerald'}">${s.internal_assessment_score}</span>
          </div>
          <div class="roster-stat">
            <span class="stat-label">CAVS</span>
            <span class="stat-val">${s.composite_vulnerability_score.toFixed(1)}</span>
          </div>
          <span class="risk-badge ${badgeClass}">${s.risk_category.replace(" Early Warning", "")}</span>
        </div>
      `;

      card.addEventListener("click", () => openStudentModal(s));
      rosterContainer.appendChild(card);
    });
  }

  // Open Detailed Modal
  function openStudentModal(student) {
    document.getElementById("modal-student-name").textContent = `${student.student_name} (${student.student_id})`;
    document.getElementById("modal-student-course").textContent = `Course: ${student.course_id || 'CSE3002 - Computer Vision'}`;
    
    document.getElementById("modal-att").textContent = `${student.attendance_percentage}%`;
    document.getElementById("modal-int").textContent = `${student.internal_assessment_score}/100`;
    document.getElementById("modal-lms").textContent = `${student.lms_engagement_score}%`;
    document.getElementById("modal-vis").textContent = `${student.visual_attention_score}%`;

    const factorsContainer = document.getElementById("modal-factors");
    factorsContainer.innerHTML = "";
    (student.contributing_factors || ["No risk factors"]).forEach(f => {
      const li = document.createElement("li");
      li.textContent = f;
      factorsContainer.appendChild(li);
    });

    const interContainer = document.getElementById("modal-interventions");
    interContainer.innerHTML = "";
    (student.suggested_interventions || ["None"]).forEach(i => {
      const div = document.createElement("div");
      div.className = "intervention-item";
      div.textContent = `• ${i}`;
      interContainer.appendChild(div);
    });

    modal.style.display = "flex";
  }

  modalClose.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("click", (e) => {
    if (e.target === modal) modal.style.display = "none";
  });

  // Filter Buttons
  document.querySelectorAll(".filter-pill").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".filter-pill").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.currentFilter = btn.getAttribute("data-filter");
      renderRoster();
    });
  });

  // What-If Simulator Update
  function updateSimulator() {
    const att = parseFloat(sliderAtt.value);
    const intMarks = parseFloat(sliderInt.value);
    const lms = parseFloat(sliderLms.value);
    const vis = parseFloat(sliderVis.value);

    simValAtt.textContent = `${att}%`;
    simValInt.textContent = `${intMarks}`;
    simValLms.textContent = `${lms}%`;
    simValVis.textContent = `${vis}%`;

    // CAVS Formula: 100 - [0.30*vis + 0.25*att + 0.25*int + 0.20*lms]
    const compPerf = (0.30 * vis) + (0.25 * att) + (0.25 * intMarks) + (0.20 * lms);
    const cavs = Math.max(0, Math.min(100, 100.0 - compPerf));

    simCavsScore.textContent = `${cavs.toFixed(1)} / 100`;

    if (cavs >= 58.0 || att < 75.0) {
      simRiskBadge.className = "risk-badge badge-critical";
      simRiskBadge.textContent = "CRITICAL EARLY WARNING";
      simCavsScore.className = "sim-result-score text-rose";
    } else if (cavs >= 35.0) {
      simRiskBadge.className = "risk-badge badge-moderate";
      simRiskBadge.textContent = "MODERATE RISK";
      simCavsScore.className = "sim-result-score text-amber";
    } else {
      simRiskBadge.className = "risk-badge badge-low";
      simRiskBadge.textContent = "LOW RISK";
      simCavsScore.className = "sim-result-score text-emerald";
    }
  }

  [sliderAtt, sliderInt, sliderLms, sliderVis].forEach(s => s.addEventListener("input", updateSimulator));

  // Controls Handlers
  selectSimState.addEventListener("change", (e) => {
    state.simulatedState = e.target.value;
  });

  btnStreamToggle.addEventListener("click", () => {
    state.isStreaming = !state.isStreaming;
    btnStreamToggle.textContent = state.isStreaming ? "Pause Stream" : "Resume Stream";
    btnStreamToggle.className = state.isStreaming ? "btn btn-primary" : "btn btn-secondary";
  });

  btnTriggerBlink.addEventListener("click", () => {
    state.blinkActive = true;
    setTimeout(() => { state.blinkActive = false; }, 220);
  });

  btnTogglePrivacy.addEventListener("click", () => {
    state.privacyBlur = !state.privacyBlur;
    hudPrivacyBadge.textContent = `De-identification: ${state.privacyBlur ? 'ON (Gaussian ROI)' : 'OFF'}`;
    hudPrivacyBadge.style.color = state.privacyBlur ? '#34d399' : '#94a3b8';
  });

  // Canvas Drawing Engine
  function drawStreamHUD() {
    state.frameIndex++;

    const w = canvas.width;
    const h = canvas.height;
    const cx = w / 2;
    const cy = h / 2;

    // Background Studio Grid
    ctx.fillStyle = "#0c101a";
    ctx.fillRect(0, 0, w, h);

    // Subtle grid lines
    ctx.strokeStyle = "rgba(255, 255, 255, 0.04)";
    ctx.lineWidth = 1;
    for (let x = 0; x < w; x += 40) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
    }
    for (let y = 0; y < h; y += 40) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }

    // State parameters calculation
    let yawOffset = 0;
    let pitchOffset = 0;
    let earVal = 0.30;
    let marVal = 0.20;
    let instantAttention = 88.0;
    let dominantAffect = "FOCUSED";
    let affectConf = 0.88;

    const t = state.frameIndex * 0.05;
    const microJitterX = Math.sin(t * 1.5) * 3;
    const microJitterY = Math.cos(t * 1.2) * 2;

    switch (state.simulatedState) {
      case "Focused":
        yawOffset = microJitterX;
        pitchOffset = microJitterY;
        earVal = 0.29 + Math.sin(t * 2) * 0.02;
        marVal = 0.18;
        instantAttention = 88.0 + Math.sin(t) * 4.0;
        dominantAffect = "FOCUSED";
        affectConf = 0.89;
        break;

      case "Distracted":
        yawOffset = 52 + Math.sin(t) * 6;
        pitchOffset = 14 + Math.cos(t) * 4;
        earVal = 0.27;
        marVal = 0.22;
        instantAttention = 32.0 + Math.sin(t) * 5.0;
        dominantAffect = "DISTRACTED";
        affectConf = 0.92;
        break;

      case "Drowsy":
        yawOffset = Math.sin(t * 0.8) * 8;
        pitchOffset = 28 + Math.sin(t * 0.5) * 10;
        earVal = 0.13;
        marVal = 0.72; // Yawning
        instantAttention = 18.0 + Math.cos(t) * 6.0;
        dominantAffect = "DROWSY";
        affectConf = 0.95;
        break;

      case "Confused":
        yawOffset = -15 + Math.sin(t) * 4;
        pitchOffset = -10 + Math.cos(t) * 3;
        earVal = 0.26;
        marVal = 0.25;
        instantAttention = 68.0 + Math.sin(t) * 5.0;
        dominantAffect = "CONFUSED";
        affectConf = 0.76;
        break;

      case "Neutral":
        yawOffset = 4 + microJitterX;
        pitchOffset = microJitterY;
        earVal = 0.28;
        marVal = 0.20;
        instantAttention = 74.0 + Math.sin(t) * 3.0;
        dominantAffect = "NEUTRAL";
        affectConf = 0.65;
        break;
    }

    if (state.blinkActive) {
      earVal = 0.08;
    }

    instantAttention = Math.max(5, Math.min(99, instantAttention));

    // Temporal EMA smoothing calculation
    let prevEma = state.historyEma.length > 0 ? state.historyEma[state.historyEma.length - 1] : instantAttention;
    let smoothedAttention = 0.22 * instantAttention + 0.78 * prevEma;

    state.historyRaw.push(instantAttention);
    state.historyEma.push(smoothedAttention);
    if (state.historyRaw.length > state.maxHistory) state.historyRaw.shift();
    if (state.historyEma.length > state.maxHistory) state.historyEma.shift();

    // Color based on attention
    let themeColor = "#10b981"; // Emerald
    if (instantAttention < 45) themeColor = "#f43f5e"; // Rose
    else if (instantAttention < 70) themeColor = "#f59e0b"; // Amber

    // Face coordinates
    const faceX = cx - 110 + yawOffset;
    const faceY = cy - 100 + pitchOffset;
    const faceW = 220;
    const faceH = 250;

    // Privacy Blur or Normal Face
    if (state.privacyBlur) {
      ctx.save();
      ctx.fillStyle = "rgba(30, 41, 59, 0.92)";
      ctx.beginPath();
      ctx.roundRect(faceX, faceY, faceW, faceH, 16);
      ctx.fill();

      // Pixelation pattern
      ctx.fillStyle = "rgba(56, 189, 248, 0.15)";
      for (let px = faceX; px < faceX + faceW; px += 20) {
        for (let py = faceY; py < faceY + faceH; py += 20) {
          if (Math.random() > 0.4) ctx.fillRect(px, py, 18, 18);
        }
      }

      ctx.fillStyle = "#38bdf8";
      ctx.font = "600 13px 'JetBrains Mono'";
      ctx.textAlign = "center";
      ctx.fillText("[PII ANONYMIZED - PRIVACY FILTER ACTIVE]", cx + yawOffset, cy + pitchOffset);
      ctx.restore();
    } else {
      // Facial Silhouette
      ctx.save();
      ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
      ctx.lineWidth = 2;
      ctx.fillStyle = "rgba(25, 34, 52, 0.65)";
      ctx.beginPath();
      ctx.ellipse(cx + yawOffset, cy + 20 + pitchOffset, 85, 115, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Eyes
      const eyeH = state.blinkActive || earVal < 0.18 ? 3 : 14;
      const leftEyeX = cx - 38 + yawOffset;
      const rightEyeX = cx + 38 + yawOffset;
      const eyeY = cy - 15 + pitchOffset;

      ctx.fillStyle = "#38bdf8";
      ctx.beginPath();
      ctx.ellipse(leftEyeX, eyeY, 18, eyeH, 0, 0, Math.PI * 2);
      ctx.ellipse(rightEyeX, eyeY, 18, eyeH, 0, 0, Math.PI * 2);
      ctx.fill();

      // Pupils
      if (eyeH > 4) {
        ctx.fillStyle = "#0f172a";
        ctx.beginPath();
        ctx.arc(leftEyeX + (yawOffset * 0.15), eyeY, 6, 0, Math.PI * 2);
        ctx.arc(rightEyeX + (yawOffset * 0.15), eyeY, 6, 0, Math.PI * 2);
        ctx.fill();
      }

      // 68-Point Mesh Simulation Dots
      ctx.fillStyle = "rgba(56, 189, 248, 0.75)";
      const meshPoints = [
        [leftEyeX - 16, eyeY], [leftEyeX, eyeY - eyeH], [leftEyeX + 16, eyeY], [leftEyeX, eyeY + eyeH],
        [rightEyeX - 16, eyeY], [rightEyeX, eyeY - eyeH], [rightEyeX + 16, eyeY], [rightEyeX, eyeY + eyeH],
        [cx + yawOffset, cy + 15 + pitchOffset], // Nose tip
        [cx + yawOffset, cy + pitchOffset],      // Nose bridge
        [cx - 12 + yawOffset, cy + 25 + pitchOffset],
        [cx + 12 + yawOffset, cy + 25 + pitchOffset],
        [cx - 30 + yawOffset, cy + 55 + pitchOffset], // Mouth left
        [cx + 30 + yawOffset, cy + 55 + pitchOffset], // Mouth right
        [cx + yawOffset, cy + 115 + pitchOffset]      // Chin
      ];
      meshPoints.forEach(([px, py]) => {
        ctx.beginPath();
        ctx.arc(px, py, 2.5, 0, Math.PI * 2);
        ctx.fill();
      });

      // Mouth
      ctx.strokeStyle = themeColor;
      ctx.lineWidth = 2;
      ctx.beginPath();
      if (marVal > 0.6) {
        // Yawn
        ctx.ellipse(cx + yawOffset, cy + 60 + pitchOffset, 22, 26, 0, 0, Math.PI * 2);
        ctx.stroke();
      } else {
        ctx.arc(cx + yawOffset, cy + 50 + pitchOffset, 22, 0.2 * Math.PI, 0.8 * Math.PI);
        ctx.stroke();
      }

      // Head Pose Vector Projection Line (PnP axis)
      ctx.strokeStyle = "#a855f7";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(cx + yawOffset, cy + 15 + pitchOffset);
      ctx.lineTo(cx + yawOffset + (yawOffset * 1.8), cy + 15 + pitchOffset + (pitchOffset * 1.8));
      ctx.stroke();

      ctx.restore();
    }

    // Outer Bounding Box with Corner Brackets
    ctx.strokeStyle = themeColor;
    ctx.lineWidth = 2;
    ctx.strokeRect(faceX, faceY, faceW, faceH);

    // Corner accents
    const bracketLen = 18;
    ctx.lineWidth = 4;
    // Top Left
    ctx.beginPath();
    ctx.moveTo(faceX, faceY + bracketLen); ctx.lineTo(faceX, faceY); ctx.lineTo(faceX + bracketLen, faceY);
    ctx.stroke();
    // Top Right
    ctx.beginPath();
    ctx.moveTo(faceX + faceW - bracketLen, faceY); ctx.lineTo(faceX + faceW, faceY); ctx.lineTo(faceX + faceW, faceY + bracketLen);
    ctx.stroke();
    // Bottom Left
    ctx.beginPath();
    ctx.moveTo(faceX, faceY + faceH - bracketLen); ctx.lineTo(faceX, faceY + faceH); ctx.lineTo(faceX + bracketLen, faceY + faceH);
    ctx.stroke();
    // Bottom Right
    ctx.beginPath();
    ctx.moveTo(faceX + faceW - bracketLen, faceY + faceH); ctx.lineTo(faceX + faceW, faceY + faceH); ctx.lineTo(faceX + faceW, faceY + faceH - bracketLen);
    ctx.stroke();

    // Top Telemetry Banner inside Canvas
    ctx.fillStyle = "rgba(12, 16, 26, 0.85)";
    ctx.fillRect(14, 14, 380, 100);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
    ctx.lineWidth = 1;
    ctx.strokeRect(14, 14, 380, 100);

    ctx.font = "600 12px 'JetBrains Mono'";
    ctx.fillStyle = "#e2e8f0";
    ctx.textAlign = "left";
    ctx.fillText(`TOKEN: ANON-8B4E19C0 | FPS: 30.0`, 26, 34);

    ctx.fillStyle = themeColor;
    ctx.fillText(`STATE: ${dominantAffect} (${(affectConf).toFixed(2)})`, 26, 54);

    ctx.fillStyle = "#94a3b8";
    ctx.fillText(`EAR: ${earVal.toFixed(2)} | YAW: ${(yawOffset).toFixed(1)}° | PITCH: ${(pitchOffset).toFixed(1)}°`, 26, 72);

    // Attention Bar
    ctx.fillStyle = "#fff";
    ctx.fillText(`ATTENTION: ${instantAttention.toFixed(1)}%`, 26, 94);

    const barW = 160;
    const barFill = (instantAttention / 100) * barW;
    ctx.fillStyle = "rgba(255, 255, 255, 0.1)";
    ctx.fillRect(180, 83, barW, 12);
    ctx.fillStyle = themeColor;
    ctx.fillRect(180, 83, barFill, 12);

    // Update DOM Telemetry Matrix
    teleInstant.textContent = `${instantAttention.toFixed(1)}%`;
    teleSmoothed.textContent = `${smoothedAttention.toFixed(1)}%`;
    teleEar.textContent = earVal.toFixed(2);
    telePose.textContent = `${yawOffset >= 0 ? '+' : ''}${yawOffset.toFixed(1)}° / ${pitchOffset >= 0 ? '+' : ''}${pitchOffset.toFixed(1)}°`;
    teleAffect.textContent = `${dominantAffect} (${affectConf.toFixed(2)})`;
    teleAffect.className = `tele-val ${instantAttention >= 70 ? 'text-emerald' : (instantAttention >= 45 ? 'text-amber' : 'text-rose')}`;

    // Draw Temporal Dynamics Chart
    drawAttentionChart();
  }

  // Draw Temporal Chart Canvas
  function drawAttentionChart() {
    const cw = chartCanvas.width;
    const ch = chartCanvas.height;

    chartCtx.clearRect(0, 0, cw, ch);

    // Grid lines
    chartCtx.strokeStyle = "rgba(255, 255, 255, 0.05)";
    chartCtx.lineWidth = 1;
    [0.25, 0.5, 0.75].forEach(ratio => {
      const y = ch * ratio;
      chartCtx.beginPath();
      chartCtx.moveTo(0, y);
      chartCtx.lineTo(cw, y);
      chartCtx.stroke();
    });

    if (state.historyRaw.length < 2) return;

    const step = cw / (state.maxHistory - 1);

    // 1. Draw Raw Attention Line (Cyan)
    chartCtx.strokeStyle = "rgba(56, 189, 248, 0.6)";
    chartCtx.lineWidth = 1.5;
    chartCtx.beginPath();
    state.historyRaw.forEach((val, i) => {
      const x = i * step;
      const y = ch - (val / 100.0) * (ch - 10) - 5;
      if (i === 0) chartCtx.moveTo(x, y);
      else chartCtx.lineTo(x, y);
    });
    chartCtx.stroke();

    // 2. Draw Smoothed EMA Line (Emerald) with Gradient Area
    chartCtx.strokeStyle = "#10b981";
    chartCtx.lineWidth = 2.5;
    chartCtx.beginPath();
    state.historyEma.forEach((val, i) => {
      const x = i * step;
      const y = ch - (val / 100.0) * (ch - 10) - 5;
      if (i === 0) chartCtx.moveTo(x, y);
      else chartCtx.lineTo(x, y);
    });
    chartCtx.stroke();
  }

  // Animation Loop
  function tick() {
    if (state.isStreaming) {
      drawStreamHUD();
    }
    requestAnimationFrame(tick);
  }

  // Initial Boot
  syncBackendData();
  updateSimulator();
  requestAnimationFrame(tick);
});

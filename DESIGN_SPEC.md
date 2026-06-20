# Clinical Protocol Auditor — UI/UX Design Specification
**Version 1.0** | **Role: Senior Product Designer** | **Date: 2026-06-20**

---

## Executive Summary

This design specification defines a **web-based clinical compliance dashboard** for identifying protocol risks and adherence errors. The application prioritizes **trust**, **clarity**, and **actionability** through a split-view paradigm, medical-grade aesthetics, and proactive compliance workflows.

**Core Principle:** *Empower clinicians to make informed compliance decisions by combining AI insights with human oversight.*

---

## 1. Information Architecture & Layout

### 1.1 Split-View Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                         TOP NAVIGATION BAR                       │
│  [← Back] | Auditor Dashboard | [Protocol Name] | [User Menu]   │
└─────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────┬──────────────────────────────┐
│                                  │                              │
│     LEFT PANEL: PDF VIEWER       │   RIGHT PANEL: AUDIT LOG    │
│     (58% width)                  │   (42% width)                │
│                                  │                              │
│  ┌────────────────────────────┐  │ ┌──────────────────────────┐ │
│  │ PDF Viewer                 │  │ │ Compliance Overview      │ │
│  │ • Scrollable               │  │ │ ┌──────────────────────┐ │ │
│  │ • Text Selection           │  │ │ │ Status: 🟡 AT RISK   │ │ │
│  │ • Sensitive Highlight      │  │ │ │ Confidence: 87%      │ │ │
│  │ • Annotation Pins          │  │ │ │ Issues Found: 7      │ │ │
│  │                            │  │ │ └──────────────────────┘ │ │
│  │ [Page 1/8]                │  │ │                          │ │
│  │                            │  │ ├──────────────────────────┤ │
│  │ <<Highlighted Clause>>     │  │ │ AUDIT LOG (Searchable)   │ │
│  │ "Study inclusion criteria  │  │ │                          │ │
│  │  must include patients..." │  │ │ 1. ⚠️  HIGH PRIORITY     │ │
│  │                            │  │ │    Inclusion Criteria    │ │
│  │ [Section 2.1 Flagged]      │  │ │    Gap identified        │ │
│  │                            │  │ │    Line: 47              │ │
│  │                            │  │ │    [View] [Fix] [Ignore] │ │
│  │                            │  │ │                          │ │
│  │                            │  │ │ 2. ⚠️  MEDIUM PRIORITY   │ │
│  │                            │  │ │    Dosage Documentation  │ │
│  │                            │  │ │    Incomplete ref        │ │
│  │                            │  │ │    [View] [Fix] [Ignore] │ │
│  │                            │  │ │                          │ │
│  │                            │  │ │ 3. ℹ️  LOW PRIORITY      │ │
│  │                            │  │ │    Format Issue          │ │
│  │                            │  │ │    [View] [Ignore]       │ │
│  │                            │  │ │                          │ │
│  └────────────────────────────┘  │ └──────────────────────────┘ │
│                                  │                              │
└──────────────────────────────────┴──────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│  [Export Report] [Share] [Resolve All] | Last Sync: 2min ago    │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Layout Specifications

| Component | Width | Height | Notes |
|-----------|-------|--------|-------|
| Left Panel (PDF Viewer) | 58% | Full | Responsive grid layout |
| Right Panel (Audit Log) | 42% | Full | Fixed scrollable container |
| Top Bar | 100% | 60px | Sticky navigation |
| Bottom Bar | 100% | 50px | Action bar, always visible |

---

## 2. Visual Design System

### 2.1 Medical-Grade Color Palette

**Primary Palette** — Trust & Clarity
- **Accent Blue**: `#0066CC` (trust, professionalism) — Primary actions, hover states
- **Deep Navy**: `#1A2332` (authority, stability) — Text, headers, dark mode
- **Clean White**: `#FFFFFF` (clarity, hygiene) — Backgrounds, card surfaces
- **Neutral Gray**: `#F5F5F5` (calm, non-intrusive) — Secondary backgrounds, dividers

**Status Traffic-Light System**
- **🟢 Green (Compliant)**: `#00AA44` — Risk score 0–20%
- **🟡 Yellow (At Risk)**: `#FFAA00` — Risk score 21–60%
- **🔴 Red (Critical)**: `#DD3333` — Risk score 61–100%

**Contextual Status Indicators**
- **High Priority (⚠️)**: `#DD3333` (Red)
- **Medium Priority (⚠️)**: `#FFAA00` (Yellow)
- **Low Priority (ℹ️)**: `#0066CC` (Blue)
- **Resolved (✓)**: `#00AA44` (Green)
- **Flagged for Review (♦)**: `#9966CC` (Purple)

### 2.2 Typography

| Element | Font | Weight | Size | Line Height |
|---------|------|--------|------|-------------|
| Page Title | Inter | 700 | 28px | 1.3 |
| Section Header | Inter | 600 | 18px | 1.4 |
| Body Text | Inter | 400 | 14px | 1.6 |
| Small Label | Inter | 500 | 12px | 1.5 |
| Monospace (Code) | JetBrains Mono | 400 | 13px | 1.5 |

**Rationale:** Inter is optimized for screen readability; clean sans-serif avoids medical serif stereotypes. Monospace for clause references ensures precision.

### 2.3 Spacing & Grid

- **Base Unit**: 8px
- **Spacing Scale**: 8px, 12px, 16px, 24px, 32px, 48px
- **Card Padding**: 16px
- **Section Margin**: 24px
- **Border Radius**: 6px (subtle softness, not overly rounded)

### 2.4 Visual Hierarchy: Subtle Medical Aesthetic

```css
/* Cards: Minimal shadow, clean borders */
.audit-card {
  background: #FFFFFF;
  border: 1px solid #E0E0E0;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);  /* Soft, non-aggressive */
  padding: 16px;
}

/* Status Badges: Solid background, no gradients */
.status-badge {
  padding: 6px 12px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 12px;
  letter-spacing: 0.5px;  /* Slight spacing for clarity */
}

/* Hover: Subtle elevation */
.audit-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.2s ease-out;
}
```

---

## 3. Cognitive Load Reduction Strategy

### 3.1 Traffic-Light Status System

**Primary Compliance Score (Central Hub)**
```
┌─────────────────────────────┐
│    COMPLIANCE SCORE         │
│                             │
│         🟡 AT RISK          │
│         67% Risk            │
│                             │
│  ┌─────────────────────────┐│
│  │ 7 Issues · 2 Critical   ││
│  │ 3 Unresolved · 2 Waived ││
│  └─────────────────────────┘│
│                             │
│  [Expand Summary]           │
└─────────────────────────────┘
```

**Color-Coded Logic:**
- **🟢 Green (0–20% Risk)**: Proceed to publication review.
- **🟡 Yellow (21–60% Risk)**: Further review recommended; blockers exist but manageable.
- **🔴 Red (61–100% Risk)**: Cannot proceed; critical compliance gaps identified.

---

### 3.2 Audit Confidence Micro-Interactions

**Problem:** Users must distinguish between high-confidence AI flags and edge cases where manual review is essential.

**Solution: Confidence Indicator with Layered Transparency**

```
┌────────────────────────────────────┐
│ ⚠️  HIGH PRIORITY                  │
│ Inclusion Criteria Gap             │
│                                    │
│ Confidence: ████████░░ 87%        │ ← Filled bar + percentage
│ AI Rationale: "This clause..."     │
│ Suggested Fix: [Apply]             │
│ Manual Review Threshold: No         │ ← Green: Auto-trust OK
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ ⚠️  MEDIUM PRIORITY                │
│ Dosage Documentation Reference     │
│                                    │
│ Confidence: ███████░░░ 62%        │ ← Partial bar
│ AI Rationale: "Reference unclear"  │
│ Suggested Fix: [Review First]      │
│ Manual Review Threshold: YES ⚠️    │ ← Yellow: Expert needed
│ [I Reviewed & Approve]             │ ← User attestation checkbox
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ ⚠️  LOW PRIORITY                   │
│ Format Inconsistency               │
│                                    │
│ Confidence: ████░░░░░░ 38%        │ ← Low confidence
│ AI Rationale: "Minor variation"    │
│ Suggested Fix: [Ignore Pattern]    │ ← Allow user override
│ Manual Review Threshold: NO         │ ← Discretionary
└────────────────────────────────────┘
```

**Micro-Interactions:**
1. **Hover on Confidence Bar**: Show tooltip with AI model info + confidence factors (e.g., "Based on 3 clauses matching 92% similarity")
2. **Click "Manual Review Threshold"**: Expand explanation of why AI flagged it + historical similar cases
3. **Keystroke Shortcut** (`U` for "User Attest"): Speed up approval workflow for experienced users

---

### 3.3 Visual Hierarchy: What Matters First

**Audit Log Sorting (Default to High-Value Issues)**

1. **Critical Issues** (Risk score 80–100) — Red, Pin to top
2. **Blocking Issues** (Risk score 60–79) — Yellow, Expandable
3. **Advisory Issues** (Risk score 21–59) — Blue, Collapsible
4. **Resolved Issues** (Status: ✓) — Gray, Hidden by default

**Smart Filtering:**
- "Show: All | Unresolved | Critical Only | Requires Review"
- Default: "Unresolved" (hide already-resolved items)

---

## 4. Hackathon "Wow-Factor" Features

### Feature 1: **AI-Suggested Fix with One-Click Apply** ⚡

**User Pain Point:** Manual corrections take 5–10 minutes per issue.

**Solution: Smart Fix Suggestion Engine**

```
┌──────────────────────────────────────┐
│ ⚠️  CRITICAL: Dosage Mismatch        │
│                                      │
│ Issue:                               │
│ "Max dose: 5mg, but protocol        │
│  permits 10mg daily."                │
│                                      │
│ ✅ AI-Suggested Fix:                 │
│ ┌──────────────────────────────────┐ │
│ │ "Revise max dose to 5mg/day      │ │
│ │  (align with Section 3.2.1)"     │ │
│ │                                  │ │
│ │ [Apply Fix] [Edit First] [Info]  │ │
│ └──────────────────────────────────┘ │
│                                      │
│ 📊 Impact: Fixes 1 issue, affects   │
│    3 downstream clauses             │
│    [Show Impact Map]                │
└──────────────────────────────────────┘
```

**Implementation:**
- Use LLM chain to generate revision suggestions (prompt: "Given this compliance gap, suggest a specific, minimal text change")
- Store fix templates (domain-specific patterns for common errors)
- On "Apply Fix": Generate side-by-side diff view; require user confirmation before committing
- Track fix history for audit trail

**Wow Factor:** User sees compliance improve in real-time (update traffic-light score instantly)

---

### Feature 2: **Risk Trend Timeline** 📈

**User Pain Point:** "Have we been fixing things, or just papering over cracks?"

**Solution: Interactive Risk History Dashboard**

```
┌────────────────────────────────────────────┐
│ RISK TREND (Last 30 Days)                  │
├────────────────────────────────────────────┤
│                                            │
│  Risk%  100│                               │
│         80│     ╱╲___                      │
│         60│  ╱╲╱     ╲___                  │
│         40│╱              ╲___╱╲_           │
│         20│                    ╲╱╲_        │
│          0│                       ╲___     │
│            └──────────────────────────────│
│            Jun 1   Jun 10  Jun 15  Jun 20  │
│                                            │
│  Key Events:                               │
│  📌 Jun 5: Uploaded protocol (Risk: 78%)   │
│  ✅ Jun 8: Fixed 3 critical issues        │
│  📌 Jun 15: Added new inclusion criteria  │
│  ✅ Jun 19: Resolved 2 flagged items      │
│                                            │
│  Current: 🟡 32% Risk (Improving!)         │
└────────────────────────────────────────────┘
```

**Implementation:**
- Store audit snapshot on each upload + after each fix
- Render Chart.js or D3.js sparkline with events
- Hover on data point: show "Risk breakdown at this point"
- Click event: jump to PDF section / audit log entry

**Wow Factor:** Tangible proof of compliance improvement; builds user confidence in the tool

---

### Feature 3: **Smart Waiver + Risk Acceptance Workflow** ⚖️

**User Pain Point:** Not all flags are true blockers; sometimes clinical judgment overrides algorithm.

**Solution: Transparent Risk Acceptance UI**

```
┌────────────────────────────────────────┐
│ 🔴 CRITICAL: Dosage Range Undefined   │
├────────────────────────────────────────┤
│ AI Flag: "Protocol lacks max dose     │
│ specification for Medication X."      │
│                                       │
│ AI Confidence: 94% (Verified match)   │
│                                       │
│ Your Options:                         │
│                                       │
│ [1] 🔧 Apply AI Fix                   │
│     "Add 'Max dose: 5mg/day'"         │
│                                       │
│ [2] ⚖️ Accept Risk (Waive)            │
│     "Clinical team approved dosing   │
│      range verbally; document here"  │
│     ┌──────────────────────────────┐ │
│     │ Waiver Reason:               │ │
│     │ [Dropdown: Select]           │ │
│     │  - Verbal approval by PI     │ │
│     │  - Protocol amendment filed  │ │
│     │  - Risk <5%; defer to review │ │
│     │ [Attestation by: Dr. Smith]  │ │
│     │ [Approval Date: 2026-06-20]  │ │
│     │ [Audit Trail Link]           │ │
│     └──────────────────────────────┘ │
│                                       │
│ [3] ❌ Reject & Exit                  │
│     Go back; flag as blocker          │
│                                       │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ Impact:                               │
│ • If Accept: Risk score drops 8%     │
│ • If Apply Fix: Risk score drops 12% │
│ • Waiver adds audit trail entry      │
└────────────────────────────────────────┘
```

**Implementation:**
- Store waivers in audit log with user, timestamp, reason, approver
- Generate compliance certificate that lists waivers transparently
- Regulatory dashboard shows "8 issues fixed, 2 accepted waivers, 0 unresolved"

**Wow Factor:** Transforms adversarial "compliance checker" into collaborative "compliance partner"

---

## 5. User Workflow: Identify → Review → Resolve

### 5.1 Workflow State Machine

```
                      ┌─────────────────┐
                      │  START          │
                      │  (Upload PDF)   │
                      └────────┬────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ ANALYZE              │
                    │ • Extract text       │
                    │ • Run AI audit       │
                    │ • Compute risk score │
                    │ • Redact PII         │
                    └────────┬─────────────┘
                             │
                             ▼
                  ┌─────────────────────────┐
                  │ DISPLAY RESULTS         │
                  │ (Dashboard: Split-view) │
                  │ Status: 🟡 AT RISK      │
                  └────────┬────────────────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
        ┌────────┐   ┌────────┐   ┌─────────┐
        │IDENTIFY│   │ REVIEW │   │ANNOTATE │
        │(Scan   │   │(Expert │   │(Notes,  │
        │issues) │   │ review)│   │references)
        └────┬───┘   └───┬────┘   └────┬────┘
             │           │             │
             └───────┬───┴─────────────┘
                     ▼
              ┌─────────────┐
              │ RESOLVE     │
              │ • Apply fix │
              │ • Waive     │
              │ • Ignore    │
              └──────┬──────┘
                     ▼
              ┌──────────────┐
              │ APPROVED?    │
              └──────┬───────┘
               YES  │  NO
                    ▼
              ┌──────────────┐
              │ EXPORT REPORT│
              │ • Audit log  │
              │ • Waivers    │
              │ • Sign-offs  │
              └──────┬───────┘
                     ▼
              ┌──────────────┐
              │ END (Archive)│
              └──────────────┘
```

### 5.2 Detailed Workflow Steps

| Step | User Action | App Behavior | Success Criteria |
|------|-------------|--------------|-----------------|
| **1. IDENTIFY** | Upload PDF; system auto-runs audit | Split-view loads; audit log displays top issues; risk score computed | Issues visible in <5 sec; no errors |
| **2. REVIEW** | Click issue → highlight appears in PDF; read context | PDF scrolls to section; confidence bar shows; AI rationale displays | User understands why flagged (confidence >70%) |
| **3. RESOLVE (Fix)** | Click "Apply Fix" → review diff → confirm | Issue status changes to "Resolved"; risk score updates; move to next | User sees 1-click impact (risk ↓ by X%) |
| **3b. RESOLVE (Waive)** | Click "Accept Risk" → choose reason → attest | Waiver logged; issue marked "Waived"; audit trail link added | Waivers searchable; auditor can review rationale |
| **3c. RESOLVE (Ignore)** | Click "Ignore" → select reason (low confidence, false positive, etc.) | Issue hidden; can be re-surfaced via filter "Show ignored" | Pattern learning (if many ignored at <40% confidence, flag model drift) |
| **4. EXPORT** | Click "Generate Report" → download PDF or share link | Report compiled (audit log + waivers + sign-offs); QR code for verification | Report HIPAA-compliant; timestamped; signed |
| **5. SIGN-OFF** | Click "I Approve" → add digital signature | Protocol marked "Approved"; archival begins; audit trail frozen | Legally defensible (timestamp + signer + role) |

---

## 6. Accessibility (WCAG 2.1 AA Compliance)

### 6.1 Color & Contrast

| Element | Foreground | Background | Contrast Ratio | WCAG Level |
|---------|-----------|-----------|----------------|-----------|
| Body Text | #1A2332 | #FFFFFF | 12.6:1 | AAA |
| Status Badge (Green) | #FFFFFF | #00AA44 | 4.5:1 | AA |
| Status Badge (Yellow) | #000000 | #FFAA00 | 5.1:1 | AA |
| Status Badge (Red) | #FFFFFF | #DD3333 | 4.9:1 | AA |
| Link Text | #0066CC | #FFFFFF | 7.2:1 | AAA |

**Rule:** Never use color alone to convey meaning. Always pair with icons + text labels.

### 6.2 Keyboard Navigation

```
Tab Order:
1. Top nav [← Back]
2. Top nav [User Menu]
3. PDF Viewer (↑↓← → to scroll; Ctrl+F to search)
4. Audit Log Item 1 [View] [Fix] [Ignore]
5. Audit Log Item 2 [View] [Fix] [Ignore]
...
6. Bottom bar [Export] [Share] [Resolve All]

Keyboard Shortcuts:
- Alt + H: Jump to Highlight (next flagged section in PDF)
- Alt + R: Resolve Current Item
- Alt + W: Waive Current Item
- Alt + E: Export Report
- Escape: Close modal / Exit edit mode
```

### 6.3 Screen Reader Support

```html
<!-- Example: Audit Item with ARIA labels -->
<div role="article" aria-label="Critical issue: Inclusion Criteria Gap">
  <h3>⚠️ <span aria-hidden="true">HIGH PRIORITY</span></h3>
  <p>Inclusion Criteria Gap</p>
  <p>Confidence: <span aria-label="87 percent">87%</span></p>
  <p>AI Rationale: This clause...</p>
  <button aria-label="View flagged section in PDF">View</button>
  <button aria-label="Apply suggested fix">Fix</button>
  <button aria-label="Ignore this issue">Ignore</button>
</div>
```

### 6.4 Focus Management

- Focus outline: `2px solid #0066CC` (high contrast, visible on all backgrounds)
- Focus trap (modals): Keep focus within modal; on close, return to trigger button
- Skip to main: Add hidden "Skip to Audit Log" link at top (for keyboard users)

---

## 7. Implementation Roadmap

### Phase 1: MVP (Weeks 1–2)
- [ ] Split-view layout (PDF left, audit log right)
- [ ] Traffic-light status system
- [ ] Basic audit log with priority sorting
- [ ] PII redaction + visual highlight

**Deliverable:** Functional dashboard; manual audit workflows

---

### Phase 2: Smart Features (Weeks 3–4)
- [ ] AI-Suggested Fix engine (LLM chain integration)
- [ ] Confidence micro-interactions + manual review threshold
- [ ] Risk trend timeline (historical tracking)

**Deliverable:** Proactive compliance features; user confidence in AI

---

### Phase 3: Clinical Workflows (Weeks 5–6)
- [ ] Waiver + risk acceptance UI
- [ ] Digital signature + audit trail
- [ ] Export report (PDF + shareable link)

**Deliverable:** Compliance-ready; auditor-friendly

---

### Phase 4: Polish & Accessibility (Weeks 7–8)
- [ ] WCAG 2.1 AA audit
- [ ] Keyboard navigation testing
- [ ] Mobile responsiveness (tablet + mobile breakpoints)
- [ ] Dark mode (optional; accessibility + night-shift use)

**Deliverable:** Production-ready; hospital-grade UX

---

## 8. Component Library (Streamlit + Custom CSS)

### 8.1 Key Components to Build

```python
# components/status_badge.py
def status_badge(priority: str, confidence: float):
    """Render status badge with confidence bar."""
    colors = {"high": "#DD3333", "medium": "#FFAA00", "low": "#0066CC"}
    icon = {"high": "⚠️", "medium": "⚠️", "low": "ℹ️"}
    return f"""
    <div class="status-badge" style="background: {colors[priority]}">
      {icon[priority]} {priority.upper()}
      <div class="confidence-bar" style="width: {confidence}%"></div>
      {confidence:.0f}% Confidence
    </div>
    """

# components/audit_item.py
def audit_item(issue_id, title, confidence, suggested_fix, ai_rationale):
    """Render single audit log entry with actions."""
    st.container(border=True)
    st.markdown(status_badge(priority, confidence))
    st.write(title)
    with st.expander("AI Rationale"):
        st.write(ai_rationale)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("View", key=f"view_{issue_id}"):
            highlight_pdf_section(issue_id)
    with col2:
        if st.button("Apply Fix", key=f"fix_{issue_id}"):
            show_diff_view(suggested_fix)
    with col3:
        if st.button("Waive", key=f"waive_{issue_id}"):
            show_waiver_form()

# components/confidence_indicator.py
def confidence_indicator(confidence: float, manual_review_required: bool):
    """Render confidence bar with threshold explanation."""
    bar_width = int(confidence)
    threshold_label = "YES ⚠️" if manual_review_required else "NO ✓"
    return f"""
    <div class="confidence-container">
      <div class="confidence-bar" style="width: {bar_width}%"></div>
      <span>{confidence:.0f}%</span>
      <span class="manual-threshold">{threshold_label}</span>
    </div>
    """
```

### 8.2 Custom CSS

```css
/* styles/medical-grade.css */

:root {
  --color-primary: #0066CC;
  --color-success: #00AA44;
  --color-warning: #FFAA00;
  --color-error: #DD3333;
  --color-neutral: #F5F5F5;
  --color-text-dark: #1A2332;
  --color-text-light: #666666;
  --shadow-soft: 0 2px 8px rgba(0, 0, 0, 0.04);
  --shadow-elevated: 0 4px 12px rgba(0, 0, 0, 0.08);
  --spacing-base: 8px;
}

/* Split-view layout */
.dashboard-container {
  display: grid;
  grid-template-columns: 58fr 42fr;
  gap: 1px;
  height: 100vh;
  background: #E0E0E0; /* Divider color */
}

.panel-left, .panel-right {
  background: white;
  overflow-y: auto;
  padding: 24px;
}

/* Audit item card */
.audit-card {
  background: white;
  border: 1px solid #E0E0E0;
  border-radius: 6px;
  box-shadow: var(--shadow-soft);
  padding: 16px;
  margin-bottom: 12px;
  transition: all 0.2s ease-out;
}

.audit-card:hover {
  box-shadow: var(--shadow-elevated);
  border-color: var(--color-primary);
}

.audit-card.high-priority {
  border-left: 4px solid var(--color-error);
}

.audit-card.medium-priority {
  border-left: 4px solid var(--color-warning);
}

.audit-card.low-priority {
  border-left: 4px solid var(--color-primary);
}

/* Confidence bar */
.confidence-bar {
  display: inline-block;
  height: 6px;
  background: linear-gradient(90deg, var(--color-error), var(--color-warning), var(--color-success));
  border-radius: 3px;
  margin: 0 8px;
  transition: width 0.3s ease-out;
}

/* Status badge */
.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 12px;
  letter-spacing: 0.5px;
  color: white;
}

.status-badge.high {
  background: var(--color-error);
}

.status-badge.medium {
  background: var(--color-warning);
  color: black;
}

.status-badge.low {
  background: var(--color-primary);
}

/* Buttons */
button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease-out;
}

button.primary {
  background: var(--color-primary);
  color: white;
}

button.primary:hover {
  background: #0052A3;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

button.secondary {
  background: var(--color-neutral);
  color: var(--color-text-dark);
  border: 1px solid #D0D0D0;
}

button.secondary:hover {
  background: #E0E0E0;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Focus state (accessibility) */
*:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Dark mode (optional) */
@media (prefers-color-scheme: dark) {
  :root {
    --color-text-dark: #F0F0F0;
    --color-neutral: #2A2A2A;
  }
  .panel-left, .panel-right {
    background: #1A1A1A;
    color: var(--color-text-dark);
  }
}
```

---

## 9. Success Metrics & KPIs

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Audit Completion Time** | <5 min for 5–10 issues | Speed = adoption |
| **AI Fix Acceptance Rate** | >75% | Indicates UX + trust |
| **Manual Review Accuracy** | >95% (vs. baseline) | Confidence threshold working |
| **Waiver Transparency** | 100% logged + searchable | Compliance audit trail |
| **Accessibility Score** | WCAG 2.1 AA | Legal requirement |
| **User Satisfaction (NPS)** | >50 | Usability target |
| **Feature Adoption** | >60% use Risk Timeline | Engagement metric |

---

## 10. Design Principles Summary

1. **Trust Over Flair**: Every pixel serves clarity; no unnecessary decoration.
2. **Clinical Expertise**: Respect the user's domain knowledge; AI is assistant, not authority.
3. **Human Oversight**: Always provide an "out" (ignore, waive, override).
4. **Accessibility First**: WCAG 2.1 AA is non-negotiable; design with keyboard + screen reader users.
5. **Transparency**: Explain every flag; audit trail is immutable.
6. **Speed**: Dashboard loads in <2 sec; no spinners for non-blocking operations.

---

## Appendix: Wireframe References

See `WIREFRAMES.md` (next file) for detailed Figma links and clickable prototypes.

---

**Design Spec v1.0 Complete** ✓  
**Next Steps:** Handoff to Engineering; refine components; user testing with domain experts.


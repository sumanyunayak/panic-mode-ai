# PANIC MODE — AI Crisis Assistant

> **Submission for Vibe2Ship Hackathon 2026** (Organized by Coding Ninjas in collaboration with Google for Developers)  
> **Problem Statement Track:** *The Last-Minute Life Saver*  
> 🌍 **Live Application Link:** [Panic Mode Web App](https://panic-mode-ai-683548424552.asia-south1.run.app/)

---

## 📌 Project Overview
**Panic Mode** is a context-aware, non-linear AI emergency productivity assistant designed to rescue students, developers, and professionals from looming deadline paralysis. 

Unlike traditional static to-do applications that increase anxiety via endless tasks, Panic Mode acts as an **Emergency Room for Productivity**. It evaluates the user's emotional baseline, diagnoses crisis constraints via the **Google Gemini API**, protects focus using micro-task allocations ("Task Explosion"), and tracks focus dynamically using custom state-preserving checkpoints over an optimized Google Cloud infrastructure.

---

## ⚡ Key Architecture & Features

### 1. Contextual AI Diagnostic & Triage
*   **Dynamic Emotional Calibration:** Tailors response tones according to emotional choices (*Exhausted, Panicking, Stressed, or Ready to Fight*).
*   **Predictive Diagnostics:** Instantly parses text parameters via Gemini to output a *Crisis Diagnosis, Severity Level, Target Success Probability*, and *Critical Risk Threats* to avoid.

### 2. High-Yield Task Planning & "Task Explosion"
*   **Rescue Roadmaps:** Breaks macro objectives down into sequential, hyper-focused sub-milestones.
*   **AI Task Explosion:** Provides on-demand structural subdivisions of intimidating items into digestible, actionable micro-tasks to halt cognitive overload.

### 3. Progressive Midpoint AI Check-ins
*   **Dynamic 50% Triggers:** Rather than relying on generic, annoying timers, an adaptive check-in is automatically fired at exactly **50% of each task's dedicated duration**.
*   **Real-Time Adaptive Replanning:** Based on user progress or feedback (Completed, Stuck, Needs Help), the backend dynamically recalculates time allocations and shifts subsequent milestones on the fly.

### 4. Robust Production Persistence
*   **Timer & State Isolation:** Session tracking state and active countdown sequences survive incidental page updates, route navigation variations, or unexpected connection losses.

---

## 🛠️ Technology Stack

*   **Frontend:** HTML5, CSS3, Vanilla JavaScript (DOM-driven focus mechanics, UI animations).
*   **Backend:** Python, Django, Django REST Framework (DRF endpoints, session pipelines).
*   **Artificial Intelligence:** Google Gemini API, Advanced Persona Prompt Engineering.
*   **Cloud & CI/CD:** Google Cloud Run, Google Cloud Build, Google Artifact Registry.
*   **Developer Tooling:** Google AI Studio, Google Cloud Shell, Git/GitHub.

---

## 🚀 Deep Dive: Google Ecosystem Utilization

Panic Mode relies natively on the Google Developers stack to deliver its real-time functionality safely at scale:

1.  **Google AI Studio:** Used extensively during the prototyping phase to orchestrate system instructions, iterate over JSON payload consistency, optimize zero-shot prompt robustness, and validate exception schemas.
2.  **Google Gemini API:** Serves as the analytical engine powering the application's central intelligence, executing conversational triage logic, tracking task completions, and rewriting live strategies.
3.  **Google Cloud Run:** Hosts the unified Django and Vanilla JS codebase inside a serverless container environment, scaling down dynamically to zero when idle and rapidly auto-scaling during spike-traffic scenarios.
4.  **Google Cloud Build & Artifact Registry:** Powers the Continuous Deployment flow, automatically compiling clean container builds from code changes and packaging deployment images directly via standard cloud pipelines.
5.  **Google Cloud Shell:** Allowed continuous browser-based infrastructure provisioning, IAM permission configuration, and active deployment debugging.

---

## 🔄 Core Project Workflow & User Journey
 ```text
 [User Setup] -> Input Text Emergency & Select Emotional Vibe State
                       │
                       ▼
 [Triage Block] -> Gemini API analyzes context, structures severity matrices & tasks
                       │
                       ▼
 [Focus Active] -> UI locks onto individual item + Launch Countdown Timer
                       │
                       ▼
 [50% Mark UI]  -> Trigger automatic checkpoint inquiry (Done / Stuck / Need Help)
                       │
       ┌───────────────┴───────────────┐
       ▼ (If Stuck / Delayed)          ▼ (If Done)
 [Adaptive Recalibration]        [Advance Sequence]
 Gemini API adjusts timelines    Lock next milestone
       │                               │
       └───────────────┬───────────────┘
                       ▼
 [Debriefing]   -> Final rescue analytics presentation & target recovery protocol
```

## 🛠️ Local Installation & Setup Instructions

### Prerequisites
*   Python 3.10+ Installed
*   A verified Google Gemini API Key (obtained from [Google AI Studio](https://aistudio.google.com/))

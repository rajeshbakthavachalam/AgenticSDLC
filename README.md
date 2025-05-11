# AgenticSDLC: WiFi7 Project SDLC Automation

## 🚀 Overview
AgenticSDLC is an AI-powered, end-to-end solution designed to automate the entire Software Development Lifecycle (SDLC) for modern, complex projects. This example demonstrates how AgenticSDLC can be used to manage the SDLC for a **WiFi7 management platform**—from requirements gathering to deployment, with human-in-the-loop review and artifact generation at every step.

## 🌐 Why WiFi7?
WiFi7 is the next generation of wireless networking, enabling ultra-fast, low-latency, and highly reliable connectivity for smart homes, IoT, and enterprise environments. Building robust WiFi7 management software requires:
- Advanced configuration and monitoring
- Real-time performance analytics
- Security and compliance
- User-friendly interfaces for both admins and end-users

AgenticSDLC automates and orchestrates all these SDLC phases, ensuring rapid, secure, and high-quality delivery.

---

## 🛠️ Key Features
- **End-to-End SDLC Automation:** From requirements to deployment, all phases are orchestrated and documented.
- **AI-Driven Artifacts:** Automatically generates user stories, design docs, code, security reviews, test cases, and more.
- **Human-in-the-Loop:** Approve or provide feedback at every stage for maximum control and quality.
- **Graph-Based Workflow:** Modular, state-driven process powered by LangGraph.
- **LLM Integrations:** Supports OpenAI, Gemini, and Groq for code and artifact generation.
- **Redis-Powered State:** Robust state management for multi-session, multi-user workflows.
- **Modern UI & API:** Use Streamlit for interactive UI or FastAPI for programmatic access.
- **Downloadable Artifacts:** Markdown docs for every SDLC phase.

---

## 🖼️ Example: WiFi7 Project SDLC Flow

### 1. **Requirements Gathering**
- "The system should support WiFi7 connectivity."
- "Users should be able to configure WiFi7 settings."
- "The system should monitor WiFi7 performance."
- "Users should receive alerts for WiFi7 issues."

### 2. **User Stories**
- *Support WiFi7 Connectivity*: As a user, I want the system to support WiFi7 so I can benefit from the latest wireless technology.
- *Configure WiFi7 Settings*: As a user, I want to configure WiFi7 settings to optimize my network.
- *Monitor WiFi7 Performance*: As a user, I want to monitor WiFi7 performance for optimal connectivity.
- *Receive WiFi7 Alerts*: As a user, I want to receive alerts for WiFi7 issues so I can take corrective action.

### 3. **Design Documents**
- **Functional**: Describes user flows, configuration screens, alerting mechanisms, and performance dashboards.
- **Technical**: Details microservices, device communication protocols, security layers, and data storage.

### 4. **Code Generation & Security Review**
- AI generates modular Python code for WiFi7 device management, configuration APIs, and monitoring services.
- Automated security review highlights vulnerabilities and recommends fixes.

### 5. **Test Cases & QA**
- Comprehensive test cases for connectivity, configuration, performance, and alerting.
- Simulated QA feedback and bug reports.

### 6. **Deployment & Artifacts**
- Simulated deployment feedback.
- Download all generated artifacts (requirements, user stories, design docs, code, test cases, QA reports).

---

## 📦 Project Structure
```plaintext
AgenticSDLC/
├── artifacts/              # Generated Markdown artifact files
├── src/
│   └── dev_pilot/
│       ├── cache/          # Redis cache and state persistence
│       ├── api/            # Fast API integration logic
│       ├── graph/          # Graph builder and related logic
│       ├── LLMS/           # LLM integrations (Gemini, Groq, OpenAI, etc.)
│       ├── nodes/          # Individual nodes handling each SDLC phase
│       ├── state/          # SDLC state definitions and data models
│       ├── ui/             # UI components (Streamlit front-end)
│       ├── utils/          # Utility functions
├── app_streamlit.py        # Streamlit UI entry point
├── app_api.py              # FastAPI entry point
├── requirements.txt        # Python dependencies
├── workflow_graph.png      # Visual workflow diagram
└── README.md
```

---

## ⚡ Getting Started

### 1. **Clone & Install**
```bash
git clone https://github.com/rajeshbakthavachalam/AgenticSDLC.git
cd AgenticSDLC
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. **Start Redis (Docker)**
```bash
docker run -p 6379:6379 redis
```

### 3. **Set Up Environment Variables**
Create a `.env` file with your LLM API keys:
```
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 4. **Run the App**
- **Streamlit UI:**
  ```bash
  streamlit run app_streamlit.py
  ```
- **FastAPI:**
  ```bash
  python app_api.py
  ```

---

## 🧭 API Example (WiFi7 Project)

### Start SDLC Process
```http
POST /api/v1/sdlc/start
Content-Type: application/json
{
    "project_name": "WiFi7 project"
}
```

### Generate User Stories
```http
POST /api/v1/sdlc/user_stories
Content-Type: application/json
{
    "project_name": "WiFi7 project",
    "requirements": [
        "The system should support WiFi7 connectivity",
        "Users should be able to configure WiFi7 settings",
        "The system should monitor WiFi7 performance",
        "Users should receive alerts for WiFi7 issues"
    ],
    "task_id": "sdlc-session-xxxxxxx"
}
```

### Progress Workflow
```http
POST /api/v1/sdlc/progress_flow
Content-Type: application/json
{
    "project_name": "WiFi7 project",
    "task_id": "sdlc-session-xxxxxxx",
    "next_node": "review_user_stories",
    "status": "approved",
    "feedback": "None"
}
```

---

## 📊 Workflow Graph
![Workflow Graph](workflow_graph.png)

---

## 👤 Maintainer
This project is maintained by [rajeshbakthavachalam](https://github.com/rajeshbakthavachalam/AgenticSDLC)

---

## 📝 License
[GPL-3.0 License](LICENSE)


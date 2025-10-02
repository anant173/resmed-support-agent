# 🛠️ Development Challenge: ResMed CPAP Troubleshooting Agent

## Project Goal

The objective of this challenge is to build a **production-ready, conversational AI agent** that can diagnose common issues and provide compliance checks for a simulated fleet of cloud-connected ResMed CPAP devices. The solution must be highly modular, scalable, and fully observable.

---

## Part 1: Agent Persona and Core Intelligence

The agent must be designed to handle multi-step reasoning, where it decides between responding directly or using an external tool.

### 1.1 Persona Definition

* **Task:** Define a clear **System Prompt** that assigns the agent the persona of a **"Certified Sleep Therapist and ResMed Device Support Agent."**

* **Constraint:** The prompt must include a non-negotiable **RULE** requiring the agent to prioritize data access by using its tools *before* giving any general advice.

### 1.2 Agent Orchestration (LangGraph)

* **Task:** Implement the core reasoning engine using the **LangGraph** library, specifically leveraging the **ReAct (Reasoning and Acting)** framework.

* **Requirement:** The agent must be initialized with a **`MemorySaver`** component to retain conversation history across turns using a unique `thread_id`.

---

## Part 2: Tool Development and Data Modeling

The agent's intelligence is worthless without access to external data. You must define the necessary tools and the simulated data models they rely on.

### 2.1 Data Modeling (`device_data_model.py` equivalent)

* **Task:** Define Pydantic models to simulate the backend data structure, including `DeviceMetrics` (e.g., usage hours, leak rate) and a `DeviceData` collection.

* **Requirement:** Implement core business logic methods within the data model to calculate metrics, such as a function to determine **compliance status** based on usage rules.

### 2.2 Tool Development (`device_tools.py` equivalent)

* **Task:** Create the following three asynchronous, callable tools. Each tool must be decorated with both the LangChain **`@tool`** (for agent functionality) and the Traceloop **`@tool`** (for observability).

| Tool Function | Core Responsibility |
| :--- | :--- |
| **`list_available_devices()`** | Return the model names of all connected devices. |
| **`check_device_compliance(model_name)`** | Retrieve and return therapy metrics, including a compliance verdict and recommendation. |
| **`find_troubleshooting_manual(device_model, issue_keywords)`** | Simulate querying an internal manual database to provide a specific troubleshooting step based on user keywords. |

---

## Part 3: Serving, Packaging, and User Interface

The final solution must be packaged as a scalable service accessible via a simple frontend.

### 3.1 Backend Service (FastAPI)

* **Task:** Create a **FastAPI** application (`main.py`) that exposes the agent via a robust, asynchronous POST endpoint (`/run_agent`).

* **Constraint:** The endpoint must accept a structured **Pydantic model** for user input (`thread_id`, `user_input`) and correctly invoke the asynchronous `run_agent` function using `await`.

### 3.2 Frontend (Streamlit)

* **Task:** Develop a simple, interactive **Streamlit** chat interface (`streamlit_app.py`) that acts as the client.

* **Requirement:** The frontend must manage the session state (`thread_id` and message history) and use `asyncio.run()` to communicate with the agent logic.

### 3.3 Containerization

* **Task:** Create a suitable `Dockerfile` (e.g., `Dockerfile.streamlit`) to package the entire application, ensuring it runs on the required Python version (3.13) and uses the efficient `uv` dependency manager.

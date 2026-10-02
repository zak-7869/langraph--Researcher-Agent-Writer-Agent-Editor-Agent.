# Multi-Agent Content Generation Pipeline (LangGraph & Groq)
```
+-----------------------+
                        |      START NODE       |
                        +-----------+-----------+
                                    |
                                    v
                        +-----------------------+
                        |    RESEARCHER AGENT   |  <--- Gathers web data/sources
                        +-----------+-----------+       Populates `research_data`
                                    |
                                    v
                        +-----------------------+
                        |      WRITER AGENT     |  <--- Generates draft from research
                        +-----------+-----------+       Refines using editor feedback
                                    |
                                    v
                        +-----------------------+
                        |      EDITOR AGENT     |  <--- Reviews draft for quality
                        +-----------+-----------+       Sets `editor_feedback`
                                    |
                           /-----------------\
                          /   Approved or     \
                         /  Max Revisions?     \
                        /-----------------------\
                           /                 \
                 NEEDS    /                   \  APPROVED
               REVISION  /                     \
                        v                       v
            +-----------------------+   +-----------------------+
            |  Route back to Writer |   |       END NODE        |
            +-----------------------+   +-----------------------+

```
An advanced multi-agent workflows system built using **LangGraph** and powered by **Groq models** to deliver lightning-fast latency. This pipeline orchestrates three distinct AI agents—a **Researcher**, a **Writer**, and an **Editor**—to collaboratively gather data, draft high-quality content, and refine the final output.

## 🚀 Key Features
* **Extreme Low Latency:** Utilizes Groq's high-speed inference engine for near-instant agent coordination and execution.
* **Stateful Orchestration:** Built on LangGraph to cleanly manage cyclical graphs, memory, and smooth state transitions between agents.
* **Specialized Agent Roles:** Segregates tasks into dedicated agents (Research, Writing, Editing) to maximize output quality and factuality.

## 🤖 The Agent Workflow
The system processes user requests sequentially through a structured state graph:
1. **Researcher Agent:** Takes the initial prompt, queries relevant background information, compiles key data points, and passes a structured report to the next phase.
2. **Writer Agent:** Consumes the research report to draft a comprehensive, engaging article or document.
3. **Editor Agent:** Reviews the draft for grammar, tone consistency, formatting correctness, and structural flow to produce the final polished output.

## 🛠️ Tech Stack
* **Framework:** LangGraph (by LangChain)
* **LLM Engine:** Groq Cloud API
* **Language:** Python 3.10+

## 📁 Repository Structure
* `app.py`: The main entry point containing the core application logic, LangGraph workflow definition, and agent initializations.
* `requirements.txt`: Python package dependencies necessary to run the project.

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com
cd langraph--Researcher-Agent-Writer-Agent-Editor-Agent.
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here


```

### 5. Run the Application
```bash
python app.py
```
##
[
## System Architecture & GitOps Pipeline

```text
+-----------+       +-------------------+       +-------------------+       +-----------------------+
| Developer | ----> | Application Repo  | ----> |    Jenkins CI     | ----> |    Docker Registry    |
+-----------+       |     (GitHub)      |       | (Build & Container)       |  (Docker Hub / ECR)   |
                    +-------------------+       +---------+---------+       +-----------+-----------+
                                                          |                             |
                                                          | Update Tag                  |
                                                          v                             |
                                                +-------------------+                   |
                                                |  GitOps Config    |                   | Pull
                                                | Manifest Repository                   | Image
                                                +---------+---------+                   |
                                                          |                             |
                                                          v                             v
                                                +---------------------------------------------------+
                                                |                  ArgoCD (in K8s)                  |
                                                +-------------------------+-------------------------+
                                                                          |
                                                                          v Sync Deployment
                                                +---------------------------------------------------+
                                                |                 Kubernetes Cluster                |
                                                |      [ Pods | Services | Ingress | Stateful ]      |
                                                +---------------------------------------------------+
]
##
## 📝 License
This project is open-source and available under the MIT License.

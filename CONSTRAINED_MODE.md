# RepurAgent — Constrained Local Mode Guide (Windows 4 GB RAM)

This guide documents the native Windows **Constrained Local Mode** designed for machines with limited hardware resources (~4 GB RAM, integrated graphics, CPU-only).

---

## 1. Executive Summary & Why Changes Were Made

The standard RepurAgent deployment requires **Docker Desktop with WSL2** and runs **Java 11 (CPSign ADMET models)** inside the container. 
On a Windows machine with only **4 GB of physical RAM**:
- WSL2 and Docker Desktop consume 2.0–3.0 GB of RAM on boot, which starvates the Windows OS and crashes the machine.
- Spawning a full 64-bit Java Virtual Machine (JVM) with default heap settings consumes up to 1.0 GB of RAM.
- Local ChromaDB vector stores load an ONNX-based embedding model (`all-MiniLM-L6-v2`) in local memory (~200 MB).

### Key Architectural Principle: Keep Real Science, Cut Unnecessary Overhead
In **Constrained Local Mode (`LOCAL_CONSTRAINED_MODE=true`)**:
1. **Docker is eliminated completely**: RepurAgent runs natively on Windows using Python 3.13, reducing background memory overhead from ~3.5 GB down to ~350–550 MB.
2. **Scientific workflow is 100% preserved**: The planning agent, human approval gate, supervisor, research agent, knowledge graph builder, literature retriever (LitSense), SOP RAG retriever, data agent, ranking/scoring, and report generator all run natively.
3. **No fabricated evidence**: Missing local services (like Java CPSign) do **not** return fake/mock numbers. If Java is unavailable, the system explicitly reports that ADMET liabilities cannot be computed locally and instructs the agent to cite that limitation. Meanwhile, physicochemical estimation (Lipophilicity via RDKit) and repurposing indications (via the remote RepurposeDrugs server) remain fully active.
4. **Episodic memory uses remote embeddings**: Instead of holding an ONNX model in RAM, ChromaDB uses remote OpenAI embeddings (`text-embedding-3-small`).
5. **Memory leaks prevented**: Active Python garbage collection, bounded session caching (`PYTHON_SESSION_CACHE_SIZE=4`), and relaxed polling frequencies safeguard physical RAM.

---

## 2. Process Breakdown: Local vs. Remote

| Component | Execution Mode | Details |
|---|---|---|
| **Web UI & Server** | **LOCAL** | FastAPI + Gradio 5 serving at `http://localhost:7860` |
| **Agent Orchestration** | **LOCAL** | LangGraph compiled graph & state machine |
| **State Persistence** | **LOCAL** | SQLite (`persistence/memory/shortterm_memory/langgraph_checkpoints.db`) |
| **Data Sandbox** | **LOCAL** | AST-walking sandboxed Python executor (Pandas, RDKit, NumPy) |
| **SOP Document RAG** | **LOCAL + REMOTE** | Prebuilt BM25 index on disk + OpenAI embeddings |
| **LLM Inference** | **REMOTE** | OpenAI API (GPT models for planning, supervisor, report) |
| **Biomedical Literature** | **REMOTE** | NCBI LitSense API (PubMed passages) |
| **Knowledge Graph Data** | **REMOTE** | OpenTargets GraphQL, ChEMBL REST, UniProt REST, KEGG, GWAS Catalog |
| **Drug Repurposing ML** | **REMOTE** | RepurposeDrugs API (Aittokallio Group) |
| **Physicochemical Properties** | **LOCAL** | RDKit Crippen MolLogP calculation |
| **ADMET Conformal Models** | **LOCAL (Optional)** | CPSign Java models (requires JRE with `-Xmx256m`); if JRE absent, reported as unavailable |

---

## 3. Prerequisites & Required API Keys

1. **Operating System**: Windows 10 or 11 (64-bit).
2. **Python**: Python 3.13 (or 3.11/3.12).
3. **OpenAI API Key**: Mandatory for agent reasoning and SOP retrieval.
   - Get your key from [platform.openai.com](https://platform.openai.com/).

*(Docker and Java are NOT required).*

---

## 4. Windows Installation & Setup (PowerShell / Command Prompt)

Open **PowerShell** or **Command Prompt** and navigate to the project directory:

```powershell
cd c:\Users\User\Downloads\RxRevive\RxRevive
```

### Step 1: Create Virtual Environment
```powershell
python -m venv .venv
```

### Step 2: Activate the Virtual Environment
- **PowerShell**:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  *(If PowerShell scripts are restricted, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once).*
- **Command Prompt (CMD)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```

### Step 3: Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure `.env`
Copy `.env.example` to `.env` (or edit existing `.env`):
```powershell
Copy-Item .env.example .env
```
Open `.env` and configure your credentials:

**Option A: Google Gemini API (Recommended for Free Tier)**
```env
LOCAL_CONSTRAINED_MODE=true
GEMINI_API_KEY=AIzaSyYourActualKeyFromGoogleAIStudio
```
*(When `GEMINI_API_KEY` is provided, RepurAgent automatically routes all 9 agent roles to Google's OpenAI-compatible endpoint using `gemini-2.5-flash`).*

**Option B: OpenAI API**
```env
LOCAL_CONSTRAINED_MODE=true
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

---

## 5. Starting and Stopping the Application

### How to Start RepurAgent
```powershell
python main.py
```
Wait until the terminal displays:
```
INFO:     Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)
INFO: repuragent - Repuragent ready on 0.0.0.0:7860
```
Open your web browser and navigate to:
**[http://localhost:7860](http://localhost:7860)**

### How to Stop RepurAgent
Press `CTRL+C` in the PowerShell/CMD window where `main.py` is running.

---

## 6. Observed RAM Footprint

| State | Physical RAM Usage |
|---|---|
| **Base Windows OS** | ~2.0 GB |
| **RepurAgent Server Idle** | ~280 MB – 380 MB |
| **Browser (Edge/Chrome on UI)** | ~400 MB – 600 MB |
| **Active Lightweight Workflow** | ~450 MB – 650 MB |
| **Total System RAM during run** | **~3.0 GB – 3.3 GB** (Fits inside 3.6 GB physical memory) |

---

## 7. Feature Availability Matrix

| Feature | Constrained Native Mode | Full Original (Docker) Mode |
|---|:---:|:---:|
| Planning Agent & Plan Ledger (`plan.md`) | Available | Available |
| Human-in-the-loop Approval Gate | Available | Available |
| Supervisor Agent Workflow Execution | Available | Available |
| Disease ID Resolution (OpenTargets) | Available | Available |
| Knowledge Graph Construction (PyBEL/NetworkX) | Available | Available |
| PubMed Literature Retrieval (LitSense) | Available | Available |
| SOP Regulatory Retrieval (BM25 + Chroma) | Available | Available |
| Python Sandbox & Candidate Ranking | Available | Available |
| Lipophilicity Estimator (RDKit) | Available | Available |
| Indication Predictions (RepurposeDrugs API) | Available | Available |
| Evidence-Based Report Generation | Available | Available |
| SQLite State & File Persistence | Available | Available |
| Conformal ADMET Models (CPSign Java) | Unavailable (unless JRE installed) | Available (runs in Docker JVM) |
| On-device PDF OCR (`pytesseract`/`unstructured`) | Skipped (prebuilt index used) | Available |

---

## 8. How to Switch Back to Full / Original Mode

To switch back to the original configuration:
1. In `.env`, set:
   ```env
   LOCAL_CONSTRAINED_MODE=false
   ```
2. If Docker Desktop is available on a larger machine (e.g. 16 GB RAM), run:
   ```bash
   docker compose up --build
   ```
This immediately restores full Docker deployment and unconstrained session caching.


# Pharma Complaint Management System

An AI-powered pharmaceutical complaint intake and triage application designed for quality teams, complaint handlers, and regulatory operations. The system lets users upload a complaint PDF, extract structured complaint information with AI, review the populated form, and save the complaint into a database for downstream workflow processing.

## 1. What this application does

The system follows a practical end-to-end workflow:

1. A user uploads a complaint PDF from the frontend.
2. The backend extracts the raw text from the PDF.
3. An AI model extracts structured complaint fields from that text.
4. A second AI step analyzes the structured data and returns a risk assessment.
5. The complaint is saved into PostgreSQL.
6. The frontend displays the extracted values in a polished complaint form and AI insights panel.

The application is intentionally organized so the front end focuses on review and triage, while the back end handles file parsing, AI processing, and persistence.

## 2. Tech stack

### Frontend
- React 18 with TypeScript
- Vite for build and development
- Material UI for enterprise-style dashboard components
- Axios for API requests
- Custom React state management for form population, highlighting, and AI insights

### Backend
- FastAPI for the API layer
- SQLAlchemy ORM for database interaction
- PostgreSQL for complaint persistence
- Pydantic schemas for request and response validation
- PyMuPDF (fitz) for PDF text extraction

### AI layer
- Groq as the LLM provider
- Custom prompt engineering for extraction and risk assessment
- Structured JSON output for deterministic downstream use

> The current implementation uses direct Groq calls for extraction and analysis. The project also contains a graph package for future workflow orchestration, but the live upload flow is currently implemented through the API and service layers.

## 3. End-to-end flow: from PDF upload to AI summary

### Step 1: Upload PDF from the frontend

The user opens the complaint intake experience in the frontend and uploads a PDF through the AI assistant panel.

What the frontend does:
- Shows a drag-and-drop upload area and a file picker.
- Accepts PDF files only.
- Sends the file to the backend upload endpoint.
- Displays a summary card after extraction completes.
- Populates the complaint form automatically with AI-extracted values.

### Step 2: Backend receives the file

The FastAPI route receives the uploaded file and saves it into the uploads folder.

What happens in the backend:
- The route validates that a filename exists.
- The uploaded file is written to the local uploads directory.
- The route then extracts text from the PDF.


### Step 3: PDF text extraction

The backend uses PyMuPDF to open the PDF and extract all readable text page by page.

Why this step matters:
# AI-Powered Pharmaceutical Complaint Management System

An AI-assisted pharmaceutical complaint intake application built for quality teams that need to process complaint documents consistently, quickly, and with traceable outputs. The system combines PDF ingestion, structured extraction, risk evaluation, and human verification in a single workflow, helping teams reduce manual data entry while retaining reviewer control over final records.

## Features

- PDF upload for complaint intake
- AI field extraction from unstructured complaint documents
- Complaint auto population in a structured form
- Editable complaint form for reviewer corrections
- AI-generated complaint summary
- AI risk assessment with severity indicators
- Confidence score for extraction transparency
- CAPA-oriented recommendations
- PostgreSQL-backed complaint storage
- Responsive Material UI dashboard
- Human-in-the-loop verification before finalization

## Screenshots

![Dashboard](assets/dashboard.png)
![Upload Panel](assets/upload.png)
![AI Chat](assets/ai-chat.png)
![Database View](assets/database.png)

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Material UI, Axios, Vite |
| Backend | FastAPI, Python, SQLAlchemy, Pydantic |
| Database | PostgreSQL |
| AI | Groq LLM, prompt engineering, structured JSON extraction, AI risk scoring, AI summarization |
| Development Tools | Uvicorn, npm, virtual environments, REST APIs |

## System Architecture

```mermaid
flowchart TD
    U[User Uploads PDF] --> FE[Frontend - React]
    FE --> API[FastAPI Upload API]
    API --> TXT[PDF Text Extraction - PyMuPDF]
    TXT --> AI[Groq AI Extraction]
    AI --> JSON[Structured Complaint JSON]
    JSON --> RISK[AI Risk Assessment]
    RISK --> DB[(PostgreSQL)]
    DB --> RESP[Return AI Insights + Complaint Data]
    RESP --> FE
```

## Folder Structure

```text
pharma-complaint-management-system/
├── backend/
│   ├── app/
│   │   ├── ai/                 # Prompt templates, parsing, extraction logic
│   │   ├── api/routes/         # Upload and complaint endpoints
│   │   ├── core/               # App settings and configuration
│   │   ├── crud/               # Database operations
│   │   ├── database/           # Session and DB initialization
│   │   ├── models/             # SQLAlchemy models
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── services/           # Complaint orchestration services
│   │   └── utils/              # PDF reader and shared utilities
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/                # Axios clients and API wrappers
│   │   ├── components/         # Upload panel, forms, AI insights UI
│   │   └── types/              # Frontend domain types
│   └── package.json
└── uploads/                    # Uploaded input files
```

## Installation

### 1. Clone Repository

```bash
git clone <your-repository-url>
cd pharma-complaint-management-system
```

### 2. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside `backend/` using the sample below.

### 4. Frontend Setup

```bash
cd ../frontend
npm install
```

### 5. Run Backend

```bash
cd ../backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Run Frontend

```bash
cd ../frontend
npm run dev
```

Frontend is served by Vite at `http://localhost:5173` by default.

## Environment Variables

Sample `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/pharma_complaints
GROQ_API_KEY=your_groq_api_key
DEBUG=true
APP_NAME=AI-Powered Pharmaceutical Complaint Management System
```

## Workflow

1. Upload PDF complaint document from the frontend.
2. Extract text from the PDF using PyMuPDF.
3. Run AI extraction to convert free text into structured complaint fields.
4. Execute risk analysis and derive risk-related insights.
5. Save the structured complaint record into PostgreSQL.
6. Return structured response, AI summary, and recommendations via API.
7. Populate frontend forms and insights panels for human review.

## AI Workflow

### Prompt Engineering

The extraction prompt is designed around pharmaceutical complaint semantics to capture required fields while minimizing ambiguity in AI responses.

### JSON Extraction

The model is constrained to produce structured JSON output aligned to expected complaint attributes.

### Structured Validation

Parsed outputs are validated against backend schemas to prevent malformed payloads from entering downstream logic.

### Risk Assessment

Business and AI-assisted rules evaluate severity indicators and contextual signals to assign a practical risk level.

### Summary Generation

The pipeline generates a concise complaint summary intended to support quick triage by quality reviewers.

### Confidence Score

A confidence indicator is returned alongside extracted fields so users can prioritize manual verification where needed.

### Recommended Actions

The system provides CAPA-oriented next-step suggestions to assist investigation and follow-up workflows.

## Database Design

The core data model centers on a Complaint entity that stores both operational fields and AI outputs.

Key columns include:

- Complaint reference metadata (IDs, timestamps, and source file context)
- Product and batch details relevant to quality investigations
- Reporter and event details, including occurrence timelines
- Complaint classification and textual issue description
- AI-generated summary and structured extraction artifacts
- Risk assessment outputs such as risk level and confidence score
- Recommendation fields to support CAPA planning
- Record lifecycle fields for creation and update tracking

This design keeps raw intake context, validated structured data, and AI insights in one record lifecycle for simpler auditability.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/upload` | Upload complaint PDF, run extraction pipeline, and return structured AI output |
| POST | `/complaints` | Create a new complaint record |
| GET | `/complaints` | Retrieve complaint records |
| PATCH | `/complaints/{id}` | Update selected complaint fields |
| DELETE | `/complaints/{id}` | Delete a complaint record |

## Frontend

### Complaint Form

Displays extracted fields in a reviewer-friendly layout and supports manual correction before save.

### Upload Panel

Provides the document upload entry point and triggers backend extraction.

### AI Insights

Surfaces summary, risk indicators, confidence score, and recommendations from the AI pipeline.

### Chat Assistant

Supports contextual interaction patterns for discussing extracted complaint details and review decisions.

### Editable Fields

All critical complaint fields remain user-editable to preserve quality team oversight.

### Automatic Highlighting

High-risk signals and low-confidence extraction points are emphasized to guide reviewer attention.

## Future Improvements

- LangGraph-based agent workflow orchestration
- Conversation memory for reviewer context continuity
- RAG for historical complaint grounding
- End-to-end audit logs for decision traceability
- Role-based access control
- Authentication and session management
- Email notifications for escalation events
- Vector database integration for semantic retrieval
- Formal human approval workflow before complaint closure

## Challenges

- Handling inconsistent PDF layouts and OCR noise across vendors
- Keeping prompt behavior stable across varied complaint writing styles
- Normalizing date formats from ambiguous source text
- Enforcing strict structured JSON validation under non-deterministic model outputs
- Maintaining deterministic extraction quality while evolving prompts and schemas

## Lessons Learned

- AI extraction quality improves significantly when prompt design is tied to explicit schema requirements.
- Human-in-the-loop review is essential for regulated domains, even with strong model confidence.
- Validation boundaries between extraction, scoring, and persistence reduce error propagation.
- Early focus on observability and traceability simplifies debugging and stakeholder trust.


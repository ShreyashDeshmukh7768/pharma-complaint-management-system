# Frontend README

## Overview
This frontend is a simple, single-page React + TypeScript application for an AI-powered customer complaint management system.

It was built to provide a clean complaint intake experience with:
- a complaint form on the left side
- an AI-assisted upload panel on the right side
- placeholder AI insights that will later be connected to the FastAPI backend

## Current Status
The frontend is currently working and builds successfully.

### Verified status
- Build command: `npm run build`
- Result: successful production build

## What the frontend shows right now
The current UI includes:
- a header titled "Complaint Intake Console"
- a complaint form with sections for:
  - customer details
  - product details
  - complaint details
  - initial assessment
- an upload panel for PDF intake
- placeholder AI extraction results such as:
  - complaint summary
  - complaint category
  - risk assessment
  - root cause
  - CAPA recommendation

## Tech Stack Used
- React
- TypeScript
- Material UI (MUI)
- Vite
- Axios (prepared for backend integration)

## Project Structure
- `src/App.tsx` - main page layout
- `src/main.tsx` - React entry point
- `src/components/`
  - `Header.tsx`
  - `ComplaintForm.tsx`
  - `UploadPanel.tsx`
  - `AIInsights.tsx`
- `src/api/`
  - `axios.ts`
  - `complaintApi.ts`
- `src/types/complaint.ts` - complaint and AI insight interfaces
- `src/style.css` - basic global styling

## Current Functionality
### Completed
- Single-page responsive UI
- MUI-based form layout
- Controlled form fields
- Upload panel UI
- Type-safe data structures
- Production build working

### Not yet connected
- No real FastAPI integration yet
- Upload does not send data to the backend yet
- AI results are placeholders only

## How to Run Locally
From the `frontend` folder, run:

```bash
npm install
npm run dev
```

Then open the local Vite URL shown in the terminal, usually:

```text
http://localhost:5173
```

## Notes
This frontend is intentionally simple and minimal, in line with the assignment requirements. It is structured so that backend integration can be added later in a straightforward way.

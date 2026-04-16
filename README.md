# LoanSense AI

AI-powered loan eligibility and risk assessment system for **Cognizant Hackathon 2026** (Banking and Lending Track).

## Project Structure

```text
loansense-ai/
├── frontend/         # React.js app (Vite + Tailwind)
├── backend/          # Python FastAPI server
├── README.md
├── .gitignore
└── .env.example
```

## Tech Stack

### Frontend
- React 18+
- Vite
- Tailwind CSS v3
- Axios
- React Router DOM v6
- Chart.js + Recharts

### Backend
- Python 3.10+
- FastAPI
- Uvicorn
- Motor (MongoDB async driver)
- Pydantic v2
- python-multipart
- pdfplumber
- Anthropic Python SDK (Claude API)
- python-dotenv

## Prerequisites
- Node.js 18+
- Python 3.10+
- npm (comes with Node.js)

## Environment Variables

Create your local `.env` file by copying `.env.example` and filling in real values.

```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
MONGODB_URL=your_mongodb_connection_string_here
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`

## Run Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

Health check endpoint: `GET /`

## What Is Already Set Up
- React app scaffolded with Vite
- Tailwind CSS configured and ready
- Example routing (`/` and `/insights`) in frontend
- FastAPI modular backend with CORS and upload route
- PDF text extraction service using pdfplumber
- Claude analysis service using Anthropic SDK

## Next Build Steps
1. Add loan application form + document upload flow
2. Implement eligibility scoring logic in backend services
3. Integrate Anthropic API for explanation and recommendation generation
4. Add MongoDB models for applicants, decisions, and risk metrics
5. Add authentication, validations, and tests

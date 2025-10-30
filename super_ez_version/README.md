# Meeting Intelligence API - Interview Question

A backend engineering interview question focused on building a meeting intelligence API with pre-meeting context generation and post-meeting insight extraction.

## 📂 Two Versions Available

This repository contains **two versions** of the interview question:

1. **Guided Version** (this folder) - Step-by-step with detailed TODOs
   - Best for: New grads, coding skills focus
   - Files: `api.py`, `problem.md`, etc.

2. **Open-Ended Version** (`interview_question_open_ended/`) - Minimal guidance
   - Best for: Experienced candidates, design thinking focus
   - **Read `INTERVIEWER_GUIDE.md` in that folder before using!**

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
python api.py

# Server will start on http://localhost:5000
```

## Files Overview

- **`problem.md`** - Full interview question description (start here!)
- **`api.py`** - Flask API with TODO sections to implement
- **`data.py`** - Mock database with users, contacts, and historical meetings
- **`llm_client.py`** - MockLLMClient that simulates LLM API responses
- **`requirements.txt`** - Python dependencies

## For Interviewers

### This Version: Guided (Prescriptive)

This version is designed for new grad candidates or when you want to focus on coding ability with consistent evaluation. The question:

- **Duration**: ~60 minutes
- **Difficulty**: Medium
- **Focus Areas**: API design, LLM integration, workflow orchestration, system thinking
- **Structure**: Step-by-step TODOs with examples and hints

### Want More Challenge? Use the Open-Ended Version

See `interview_question_open_ended/` folder for a version with:
- ❌ No step-by-step instructions
- ❌ No TODO comments with hints
- ❌ No prescribed API schemas
- ✅ Tests design thinking and decision-making
- ✅ Better for experienced candidates (2+ years)
- ✅ Includes comprehensive `INTERVIEWER_GUIDE.md`

### What Candidates Implement

1. **Create Meeting Endpoint** (15-20 min) - Basic CRUD operations
2. **Pre-Meeting Context** (20-25 min) - LLM prompt engineering and integration
3. **Post-Meeting Analysis** (25-30 min) - Multiple insight extractors with error handling
4. **Discussion** (10-15 min) - Architecture and scaling questions

### Key Features

- **Realistic LLM failures**: The MockLLMClient fails 20% of the time to test error handling
- **Multi-step workflows**: Pre-meeting prep and post-meeting analysis with multiple LLM calls
- **Partial failure scenarios**: In the analyze endpoint, candidates must handle some extractors succeeding while others fail

### Evaluation Criteria

- **Error handling** (critical): Retry logic, try-except blocks, graceful degradation
- Clean, readable code without duplication
- RESTful API design with appropriate status codes
- Thoughtful LLM prompts
- Good system design thinking and production readiness

## For Candidates

Read **`problem.md`** for complete instructions. You can use any AI coding assistants (ChatGPT, Claude, Copilot, etc.) during the interview.

**⚠️ Important**: The `MockLLMClient` fails randomly ~20% of the time. You must implement proper error handling and retry logic!

### Testing Your Endpoints

```bash
# Health check
curl http://localhost:5000/health

# Create meeting
curl -X POST http://localhost:5000/meetings \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Q4 Planning",
    "contact_id": "contact_1",
    "user_id": "user_1",
    "scheduled_time": "2025-11-15T10:00:00",
    "status": "scheduled"
  }'

# Prepare for meeting
curl -X POST http://localhost:5000/meetings/<meeting_id>/prepare \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_1"}'

# Analyze meeting
curl -X POST http://localhost:5000/meetings/<meeting_id>/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "Sarah: Let me walk through the proposal... Jennifer: This looks great!",
    "user_id": "user_1"
  }'
```

## Mock Data

The `data.py` file contains:
- 2 users (Sarah Chen, Michael Rodriguez)
- 3 contacts (Jennifer Liu, David Thompson, Amanda Foster)
- 6 historical meetings with rich context

All data is provided as Python dictionaries for simplicity.

## Architecture Notes

This is a simplified version for interview purposes. In production, you would:
- Use a real database (PostgreSQL, MongoDB)
- Implement proper authentication/authorization
- Add caching for LLM responses
- Use background jobs for expensive operations
- Add comprehensive error handling and logging
- Implement rate limiting
- Add monitoring and observability

Good luck!

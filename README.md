# Meeting Intelligence Platform - Backend Interview

Welcome! You'll be building a REST API for a meeting intelligence platform that helps sales teams prepare for meetings and extract insights from transcripts.

## 🚀 Setup

```bash
git clone https://github.com/ReevoAI/newgrad_interview_q1.git
cd newgrad_interview_q1
pip install -r requirements.txt
python api.py
```

Server starts at `http://localhost:5000`

## 📋 What to Read

1. **`problem.md`** - Start here! Business requirements and context
2. **`llm_client.py`** - Mock LLM client (⚠️ it fails randomly - read this!)
3. **`data.py`** - Mock database with sample data
4. **`api.py`** - Your starting point

## 🎯 Your Task

Design and implement a REST API that:
- Manages meetings
- Provides pre-meeting context (past discussions, talking points, action items)
- Analyzes meeting transcripts to extract insights

You decide the endpoints, request/response formats, and error handling strategy.

## ⏱️ Time

~60 minutes of implementation + discussion

## 💡 Notes

- Feel free to use AI coding assistants (ChatGPT, Claude, Copilot, etc.)
- Ask questions if anything is unclear
- The LLM is unreliable - handle failures gracefully
- Focus on clean, production-quality code

Good luck! 🚀

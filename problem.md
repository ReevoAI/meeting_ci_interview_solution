# Meeting Intelligence Platform - Backend Engineer Interview

## Context

You're building the backend for a meeting intelligence platform used by sales teams and customer success managers. The platform helps users:

1. **Prepare for upcoming meetings** by surfacing relevant context from their past interactions
2. **Extract insights from meeting transcripts** after meetings conclude

Think of products like Gong, Chorus, or Fireflies.ai - tools that help teams stay on top of their customer relationships through AI-powered analysis.

## Business Requirements

### Feature 1: Meeting Management
Users need to track their meetings. They should be able to create meetings and associate them with contacts they're meeting with.

### Feature 2: Pre-Meeting Intelligence
Before a meeting starts, users want to see:
- Who they're meeting with
- What they discussed previously
- Suggested talking points
- Any outstanding action items from past meetings

This context helps them prepare and be more effective in the conversation.

### Feature 3: Post-Meeting Analysis
After a meeting, users upload or paste the transcript. The system should extract useful insights like:
- Action items and who's responsible
- Key topics that were discussed
- Overall sentiment and relationship health
- Recommended follow-up actions

These insights get stored and can be referenced before future meetings.

## What You're Building

Design and implement a **REST API** that supports these features. You'll need to decide:
- What endpoints to create
- What the request/response formats should be
- How to structure the data
- How to generate the AI-powered insights

## What's Provided

You have:
- **`data.py`**: Mock data with users, contacts, and historical meetings
- **`llm_client.py`**: A mock LLM client for generating insights (read the file to understand how to use it)
- **`api.py`**: Starter Flask application (mostly empty - you'll build the endpoints)

## Hints & Guidance

### Data Structure
- Look at `HISTORICAL_MEETINGS` in `data.py` to see what information past meetings contain - this can serve as inspiration for your meeting structure
- Your API should work with **IDs** (like `user_id`, `contact_id`) rather than passing full user/contact objects
- The helper functions in `data.py` (`get_user()`, `get_contact()`, `add_meeting()`, etc.) are available for you to use

### Meeting Lifecycle
- Think about what information you need when **creating** a meeting (before it happens)
- vs. what gets **added later** after the meeting completes (transcript, insights, etc.)
- Consider: Does a meeting need a transcript at creation time? Or is that added later?

### Insights Structure
When analyzing transcripts, you'll want to extract multiple types of insights. For example:
- **Action items** might include: task description, owner, deadline, priority
- **Sentiment** might include: a score, summary text, relationship health indicator
- **Topics** might be a list of key themes discussed
- **Follow-ups** might be recommended next steps

The exact schema and fields are up to you - design what makes sense for the business requirements.

## Technical Constraints

- Use Flask (already set up in `api.py`)
- Use the provided `MockLLMClient` for all AI/LLM operations
- The mock database in `data.py` is sufficient - no need for a real database
- Focus on clean, production-quality code

## Assumptions

- **Each meeting involves exactly one user and one contact** (no multi-participant meetings)
- You can use the mock data as-is - no need to create additional users or contacts
- Meeting transcripts are provided as plain text (no audio processing needed)
- Dates are in ISO 8601 format (e.g., "2025-11-20T14:00:00")

## Expected Error Handling

Your API should return appropriate HTTP status codes:

### Success Codes
- **200 OK** - Successful GET request or operation completed

### Client Error Codes
- **400 Bad Request** - Invalid request format, missing required fields, or validation errors
- **404 Not Found** - Resource doesn't exist (meeting not found, user not found, etc.)

### Server Error Codes
- **500 Internal Server Error** - Unexpected errors (JSON parsing failures, etc.)
- **503 Service Unavailable** - External service failures (LLM API down, all retries exhausted)

## Important Notes

⚠️ **The LLM client is unreliable** - it fails randomly. Your code needs to handle this gracefully. Read the `llm_client.py` file to understand how it behaves.

⚠️ **Ask questions** - The requirements are intentionally open-ended. If you're unsure about something, ask the interviewer. Part of this exercise is understanding product requirements.

## Success Criteria

Your solution will be evaluated on:
- **API design**: Are your endpoints well-designed and RESTful?
- **Code quality**: Is your code clean, readable, and well-structured?
- **Error handling**: Does your code handle failures gracefully?
- **Completeness**: Does it solve the stated business problems?
- **Decision-making**: Can you justify your design choices?

## Time Expectation

You have approximately **60 minutes** for implementation, followed by a discussion about your approach and how you'd evolve this for production.

## Getting Started

1. Read through the provided files to understand what's available
2. Ask any clarifying questions
3. Design your API (you might want to sketch this out first)
4. Implement your endpoints
5. Test your implementation

You can use AI coding assistants (ChatGPT, Claude, Copilot, etc.) to help you code. We want to see how you work in a real development environment.

Good luck!

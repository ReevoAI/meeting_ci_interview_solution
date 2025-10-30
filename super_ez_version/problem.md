# Meeting Intelligence API - Backend Engineering Interview

## Background

You're building a backend API for a meeting intelligence platform. The platform helps users:
- **Prepare for meetings** by surfacing relevant context from past interactions
- **Extract insights** from meeting transcripts to identify action items, key decisions, and follow-ups

This is a core feature for a high-growth B2B SaaS product where sales teams, customer success managers, and executives use AI to stay on top of their relationships.

## What's Provided

You have starter code with:
- **`data.py`**: Mock database with users, contacts, and historical meetings
- **`llm_client.py`**: A `MockLLMClient` that simulates LLM API calls (you'll use this to generate insights)
- **`api.py`**: Flask starter code with TODO sections
- **`requirements.txt`**: Dependencies to install

## ⚠️ Important: Error Handling Required

**The `MockLLMClient` fails randomly ~20% of the time** to simulate real-world API reliability issues. This is intentional!

You **must implement**:
- ✅ **Try-except blocks** around all LLM calls to catch `LLMAPIError`
- ✅ **Retry logic** (we recommend 3 attempts with small delays)
- ✅ **Graceful degradation** for partial failures (in Part 3)
- ✅ **Appropriate error responses** to API clients

This tests your ability to build production-ready code that handles external service failures gracefully. In a real meeting intelligence platform, LLM APIs can be slow, rate-limited, or temporarily unavailable.

## Your Task

Implement three API endpoints and supporting logic. Work through them in order - they build on each other.

---

## Part 1: Create Meeting Endpoint (15-20 minutes)

**Endpoint**: `POST /meetings`

**Purpose**: Add a new meeting to the database

**Request Body**:
```json
{
  "title": "Q4 Planning with Acme Corp",
  "contact_id": "contact_2",
  "user_id": "user_1",
  "scheduled_time": "2025-11-15T10:00:00",
  "status": "scheduled"
}
```

**Response**:
```json
{
  "meeting_id": "meeting_123",
  "message": "Meeting created successfully"
}
```

**Requirements**:
- Generate a unique meeting_id
- Validate that user_id and contact_id exist
- Add meeting to the MEETINGS dictionary in data.py
- Return appropriate error codes for invalid data

---

## Part 2: Pre-Meeting Context Endpoint (20-25 minutes)

**Endpoint**: `POST /meetings/{meeting_id}/prepare`

**Purpose**: Generate context before a meeting to help the user prepare

**Request Body**:
```json
{
  "user_id": "user_1"
}
```

**Response**:
```json
{
  "meeting_id": "meeting_123",
  "context": {
    "contact_summary": "...",
    "recent_interactions": "...",
    "suggested_topics": ["...", "..."],
    "pending_action_items": ["...", "..."]
  }
}
```

**What to do**:
1. Get the meeting details and contact information
2. Retrieve historical meetings with this contact
3. Use the `MockLLMClient` to generate pre-meeting context
4. Structure the LLM prompt to include:
   - Contact information (name, role, company)
   - Summaries from past meetings
   - The upcoming meeting title
5. **Implement retry logic** (the LLM fails ~20% of the time!)
   - Try up to 3 times
   - Add small delays between retries (`time.sleep(0.1)`)
   - Return 503 if all retries fail
6. Parse the LLM response and return structured data

**Hints**:
- The MockLLMClient expects prompts and returns JSON-formatted responses
- Think about what information would be useful for someone preparing for a meeting
- Catch `LLMAPIError` exceptions from the client

---

## Part 3: Post-Meeting Analysis Endpoint (25-30 minutes)

**Endpoint**: `POST /meetings/{meeting_id}/analyze`

**Purpose**: Extract insights from a meeting transcript

**Request Body**:
```json
{
  "transcript": "Long transcript text here...",
  "user_id": "user_1"
}
```

**Response (success)**:
```json
{
  "meeting_id": "meeting_123",
  "insights": {
    "action_items": [...],
    "key_topics": [...],
    "sentiment": {...},
    "follow_ups": [...]
  }
}
```

**Response (partial failure)**:
```json
{
  "meeting_id": "meeting_123",
  "insights": {
    "action_items": [...],
    "key_topics": [...],
    "sentiment": null,
    "follow_ups": [...]
  },
  "errors": {
    "sentiment": "LLM call failed after 3 retries"
  },
  "partial_success": true
}
```

**What to do**:
1. Implement 4 separate insight extraction functions:
   - `extract_action_items(transcript)` - Find tasks and owners
   - `extract_key_topics(transcript)` - Identify main discussion topics
   - `analyze_sentiment(transcript)` - Determine meeting tone and relationship health
   - `generate_follow_ups(transcript)` - Suggest next steps

2. Each function should:
   - Call the `MockLLMClient` with a specific prompt
   - **Implement retry logic** (3 attempts recommended)
   - Parse the JSON response
   - Return structured data
   - Raise an exception if all retries fail

3. The main endpoint should:
   - Call all 4 insight extraction functions
   - **Wrap each call in try-except** to handle failures
   - Aggregate the results (both successes and failures)
   - If one extractor fails, still return results from others
   - Store the insights with the meeting
   - Return combined insights with error details for any failures

**Hints**:
- **Partial failure handling is critical**: With 4 LLM calls each failing 20% of the time, there's a ~60% chance at least one will fail initially
- Even with 3 retries per call, some calls may still fail - handle this gracefully
- Think about the user experience: Is partial data better than no data?
- Consider whether to run extractions sequentially or in parallel (discuss trade-offs in the discussion section)

---

## Discussion Questions (10-15 minutes)

Be prepared to discuss:

### Architecture & Design
1. **Async Processing**: The LLM calls can be slow (simulated as instant here, but imagine 2-5 seconds each). How would you handle this in production?
   - What are the pros/cons of synchronous vs asynchronous processing?
   - How would you implement background jobs?

2. **API Design**: Should insight extraction be one endpoint or multiple separate endpoints?
   - `/analyze` (all insights) vs `/action-items`, `/topics`, `/sentiment`, etc.
   - What are the trade-offs?

3. **Caching & Storage**:
   - How would you cache LLM responses?
   - Where would you store generated insights long-term?
   - How would you handle regenerating insights if the prompt changes?

### Error Handling & Reliability
4. **Retry Strategy**:
   - Why did you choose your specific retry approach (number of attempts, delay timing)?
   - What are the trade-offs between aggressive retries vs failing fast?
   - Should retry delays be constant or exponential backoff?
   - When should you give up and return an error?

5. **Failure Scenarios**:
   - What if the LLM API is completely down? How do you communicate this to users?
   - In the `/analyze` endpoint with multiple extractors, what HTTP status code should you return for partial success? (200, 207, 500, something else?)
   - Should you store partial insights or only store complete results?
   - How would you monitor and alert on LLM failure rates?

6. **Rate Limiting**: If you're calling external LLM APIs that have rate limits, how would you handle that?
   - Circuit breaker pattern?
   - Queue-based approach?
   - User-facing rate limits?

### Scaling & Performance
7. **Cost Optimization**: LLM API calls cost money per token. How would you minimize costs while maintaining quality?

8. **Scaling**: If this needs to handle 10,000 meetings per day, what would you change?

---

## Evaluation Criteria

We're looking for:
- ✅ **Correct implementation**: Endpoints work as specified
- ✅ **Error handling** (critical!):
  - Proper try-except blocks around LLM calls
  - Retry logic implemented correctly
  - Graceful handling of partial failures in `/analyze`
  - Appropriate error responses and status codes
- ✅ **Code quality**: Clean, readable, well-structured code without duplication
- ✅ **API design**: RESTful patterns, appropriate status codes, good request/response formats
- ✅ **LLM integration**: Thoughtful prompts, proper parsing of responses
- ✅ **System thinking**: Good answers to discussion questions about production readiness

## Time Allocation

- Part 1 (Create Meeting): 15-20 min
- Part 2 (Pre-Meeting Prep): 20-25 min
- Part 3 (Post-Meeting Analysis): 25-30 min
- Discussion: 10-15 min

**Total: ~60 minutes**

---

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run the API: `python api.py`
3. Test with curl or Postman
4. Implement TODOs in order

Good luck! Remember: You can use any LLM tools (ChatGPT, Claude, Copilot, etc.) to help you code. We want to see how you work in a real development environment.

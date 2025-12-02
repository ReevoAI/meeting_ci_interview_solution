# Meeting Intelligence Platform - Service Layer Interview

## Context

You're building the service layer for a meeting intelligence platform used by sales teams and customer success managers. The platform helps users:

1. **Manage their meetings** with internal and external contacts
2. **Find available time slots** across multiple users
3. **Prepare for meetings** by surfacing relevant context from past interactions
4. **Handle failures gracefully** when external services are unreliable

Think of products like Gong, Chorus, or Fireflies.ai - but you'll be focusing on the core business logic rather than API endpoints.

---

## Interview Structure

This interview is divided into **5 progressive phases**. Each phase builds on the previous one:

1. **Phase 1:** Data Models (10 min) - Define Pydantic models
2. **Phase 2:** CRUD Operations (15 min) - Implement basic database operations
3. **Phase 3:** Availability Algorithm (20 min) - Find common free time slots
4. **Phase 4:** Pre-Meeting Prep (10 min) - Generate meeting prep using LLM
5. **Phase 5:** Error Handling (5 min) - Implement retry logic for failures

**Total time: ~70 minutes**

---

## What's Provided

You have:
- **`data.py`**: Mock database with users, contacts, and meetings
- **`llm_client.py`**: Mock LLM client that randomly fails (read this!)
- **`models.py`**: Partially complete Pydantic models (you'll finish these)
- **`meeting_service.py`**: Service skeleton with detailed docstrings (you'll implement)
- **Test files**: `test_phase1.py` through `test_phase5.py` + `test_all.py`
- **`run_tests.py`**: Test runner to check your work

---

## How to Test Your Code

Instead of using curl or Postman, you'll run tests:

```bash
# Test each phase individually
uv run python run_tests.py phase1
uv run python run_tests.py phase2
uv run python run_tests.py phase3

# Or test everything
uv run python run_tests.py all
```

Tests will tell you if your implementation is correct. ✅ = passing, ❌ = failing.

---

## Phase 1: Data Models (~10 min)

### Goal
Complete the Pydantic models in `models.py`.

### Tasks
1. Add missing fields to `User`, `Meeting` models
2. Review all models and ensure they match requirements

### What to Consider
- Which fields should be optional?
- What types should each field be?
- Do the models make sense for the business domain?

### Test
```bash
uv run python run_tests.py phase1
```

---

## Phase 2: CRUD Operations (~15 min)

### Goal
Implement basic Create, Read, Update, Delete operations in `meeting_service.py`.

### Functions to Implement
- `get_all_meetings(user_id, filters)` - Get all meetings for a user
- `get_meeting(meeting_id)` - Get specific meeting
- `create_meeting(meeting_request)` - Create new meeting
- `update_meeting(meeting_id, updates)` - Update meeting fields
- `delete_meeting(meeting_id)` - Delete a meeting

### Process
1. **Design discussion** - Explain your approach to the interviewer
2. **Edge cases** - What could go wrong? How will you handle it?
3. **Implementation** - Write the code (you can use AI assistance after design approval)

### Key Edge Cases
- Invalid user/contact IDs
- Updating non-existent meetings
- Creating internal meetings (no contact)
- Empty filters

### Test
```bash
uv run python run_tests.py phase2
```

---

## Phase 3: Availability Algorithm (~20 min)

### Goal
Implement `find_available_slots()` to find times when all users are free.

### Function Signature
```python
def find_available_slots(
    user_ids: List[str],
    date: str,  # YYYY-MM-DD
    duration_minutes: int,
    work_hours: tuple = (9, 17)
) -> List[TimeSlot]:
```

### Algorithm Design
1. Get all meetings for all users on that date
2. Convert meetings to busy time intervals
3. Merge overlapping busy intervals
4. Find gaps >= duration_minutes
5. Filter gaps to work_hours only
6. Return as TimeSlot objects

### Process
1. **Whiteboard/pseudocode** - Explain your algorithm
2. **Discuss edge cases** - Empty user list? No meetings? Fully booked?
3. **Implement** - Write the code
4. **Test and debug** - Run tests and fix issues

### Key Challenges
- Time parsing and comparison
- Interval merging algorithm
- Handling overlaps and gaps
- Boundary conditions

### Test
```bash
uv run python run_tests.py phase3
```

---

## Phase 4: Pre-Meeting Prep (~10 min)

### Goal
Implement `generate_pre_meeting_prep()` to create meeting preparation using LLM.

### Function Purpose
Generate helpful context before a meeting with an external contact by:
1. Fetching historical meetings with that contact
2. Building a prompt for the LLM
3. Getting prep materials from LLM
4. Returning structured prep

### What to Generate
- Contact summary
- Recent interaction highlights
- Suggested talking points (3-5 items)
- Pending action items from past meetings

### Prompt Design
You'll need to craft a prompt that asks the LLM for structured output. Example structure:

```
You are preparing someone for a meeting.

Contact: {name} - {role} at {company}

Past meetings:
- {date}: {summary}
- {date}: {summary}

Provide:
1. Contact summary (2-3 sentences)
2. Recent interaction highlights
3. 3-5 suggested talking points
4. Pending action items

Return as JSON: {"contact_summary": "...", ...}
```

### Edge Cases
- First meeting with contact (no history)
- Internal meeting (no contact_id) - should raise ValueError
- LLM returns malformed JSON

### Test
```bash
uv run python run_tests.py phase4
```

---

## Phase 5: Error Handling (~5 min)

### Goal
Implement `generate_pre_meeting_prep_with_retry()` with retry logic.

### Why This Matters
⚠️ **The LLM client randomly fails!** It has a ~30% failure rate. Your code must handle this gracefully.

### Retry Strategy
- Try up to `max_retries` times (default 3)
- Use exponential backoff: 0.1s, 0.2s, 0.4s, etc.
- If all retries fail, raise `LLMAPIError`
- If meeting doesn't exist, raise `ValueError` (don't retry)

### Implementation Hints
```python
for attempt in range(max_retries):
    try:
        return generate_pre_meeting_prep(meeting_id)
    except LLMAPIError as e:
        if attempt == max_retries - 1:
            raise
        wait_time = 0.1 * (2 ** attempt)  # Exponential backoff
        time.sleep(wait_time)
```

### Discussion Points
- Why exponential backoff vs fixed delay?
- Should we have a max backoff time?
- Alternative: return partial results on failure?
- Circuit breaker pattern?

### Test
```bash
uv run python run_tests.py phase5
```

---

## General Guidelines

### Use AI Assistance
You're encouraged to use AI tools (ChatGPT, Claude, Copilot) for implementation. We want to see how you work in a real environment.

**However:** Design and algorithm discussions should be yours. Don't just ask AI "implement this function" without understanding the approach first.

### Ask Questions
Requirements are intentionally somewhat open-ended. If something is unclear, ask! Real engineering involves clarifying requirements.

### Code Quality Matters
- Write clean, readable code
- Add comments where helpful
- Use meaningful variable names
- Handle errors appropriately

### Focus on Business Logic
This interview emphasizes:
- Algorithm design
- Data modeling
- Error handling
- Critical thinking

Not testing:
- Flask/API knowledge
- HTTP status codes
- Tool setup

---

## Data Structure Reference

### Available in data.py

**Users:**
```python
USERS = {
    "user_1": {
        "id": "user_1",
        "name": "Sarah Chen",
        "email": "sarah.chen@company.com",
        "role": "Account Executive"
    },
    # ...
}
```

**Contacts:**
```python
CONTACTS = {
    "contact_1": {
        "id": "contact_1",
        "name": "Jennifer Liu",
        "email": "jennifer.liu@acmecorp.com",
        "company": "Acme Corp",
        "role": "VP of Engineering"
    },
    # ...
}
```

**Meetings:**
```python
MEETINGS = {
    "hist_meeting_1": {
        "id": "hist_meeting_1",
        "user_id": "user_1",
        "contact_id": "contact_1",
        "title": "Product Demo",
        "date": "2025-07-10T14:00:00",
        "summary": "...",
        "action_items": [...],
        "sentiment": "positive"
    },
    # ...
}
```

### Helper Functions Available

```python
data.get_user(user_id)
data.get_contact(contact_id)
data.get_meeting(meeting_id)
data.get_historical_meetings_for_contact(contact_id, limit)
data.add_meeting(meeting_data)
data.update_meeting(meeting_id, updates)
data.user_exists(user_id)
data.contact_exists(contact_id)
data.meeting_exists(meeting_id)
```

---

## Success Criteria

You'll be evaluated on:

1. **Algorithm Design** - Can you design efficient, correct algorithms?
2. **Code Quality** - Is your code clean and well-structured?
3. **Error Handling** - Do you handle edge cases and failures gracefully?
4. **Communication** - Can you explain your approach and trade-offs?
5. **Testing Mindset** - Do you think about what could go wrong?
6. **Completeness** - Did you implement all required functions?

---

## Getting Started

1. **Read the files** - Understand what's provided
2. **Ask questions** - Clarify anything unclear
3. **Start with Phase 1** - Complete models
4. **Progress through phases** - Test each phase before moving on
5. **Discuss your approach** - Explain your thinking as you go

Good luck! 🚀

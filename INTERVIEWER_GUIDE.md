# Interviewer Guide - Meeting Intelligence API (Open-Ended Version)

## Overview

This is the **open-ended version** of the meeting intelligence interview question. Unlike the guided version with explicit TODOs, this version tests:

- ✅ **Product thinking**: Can they translate vague requirements into a technical design?
- ✅ **Design decisions**: What choices do they make and why?
- ✅ **Question asking**: Do they clarify ambiguities or make assumptions?
- ✅ **AI tool usage**: How effectively do they use coding assistants with less guidance?
- ✅ **Production readiness**: Do they think about error handling without being told?

**Expected duration**: 60 minutes implementation + 15 minutes discussion

---

## What Makes This Version Different

| Guided Version | Open-Ended Version |
|----------------|-------------------|
| Step-by-step TODOs | High-level requirements only |
| Exact API schemas provided | Must design their own API |
| Explicit retry logic examples | Must figure out error handling |
| Prescribed 4 insight types | Must decide what insights to extract |
| Clear evaluation criteria | Ambiguous success metrics |

---

## Phase 1: Initial Questions (5-10 minutes)

### Questions Strong Candidates Ask

**About API Design:**
- "What endpoints do you want me to build? Should I create separate endpoints for each insight type or combine them?"
- "What should the request/response format look like? Do you have examples?"
- "Should meetings be created before they happen, after, or both?"
- "How should I handle meeting IDs - generate them or let the client provide them?"

**About Insights:**
- "What specific insights should I extract from transcripts?"
- "For action items, what fields should I capture? Just task description or also owner, deadline, priority?"
- "Should sentiment be a number, category, or both?"

**About Error Handling:**
- "The LLM client fails sometimes - how should I handle that? Retry? Return partial results?"
- "What HTTP status codes should I use for different error scenarios?"

**About Data:**
- "Can I assume the data in data.py is all I need? Should I modify it?"
- "Where should I store insights after generating them?"

### Red Flags: Questions They DON'T Ask
- ❌ No questions at all (diving straight into code without clarification)
- ❌ Only asking about syntax or tools ("How do I use Flask?")
- ❌ Not reading the provided files first
- ❌ Asking you to design the API for them

### How to Respond

**For good questions**: Answer them! But don't give away the solution.

Examples:
- Q: "What insights should I extract?"
  A: "What do you think would be valuable for a salesperson preparing for a meeting? Use your judgment."

- Q: "Should I retry failed LLM calls?"
  A: "What would you do in a production system? Think about the user experience."

- Q: "Separate or combined endpoints?"
  A: "Both have trade-offs. What do you think and why?"

**If they ask no questions**: Let them proceed for 5-10 minutes, then ask:
- "Before you code, can you walk me through your API design?"
- "What assumptions are you making about the requirements?"

---

## Phase 2: Design & Implementation (40-50 minutes)

### Expected API Design

Strong candidates will design something like:

```
POST   /meetings                    - Create a meeting
GET    /meetings/{id}               - Get meeting details
POST   /meetings/{id}/prepare       - Generate pre-meeting context
POST   /meetings/{id}/analyze       - Analyze transcript

Alternative (also good):
POST   /meetings/{id}/insights      - Generate all insights
GET    /meetings/{id}/insights      - Retrieve insights
POST   /meetings/{id}/action-items  - Extract action items only
POST   /meetings/{id}/sentiment     - Analyze sentiment only
```

### Key Design Decisions to Watch For

#### 1. **Error Handling Approach**
- ✅ **Great**: Implements retry logic with exponential backoff
- ✅ **Good**: Simple retry (3 attempts) with try-except
- ⚠️ **Okay**: Try-except but no retry
- ❌ **Poor**: No error handling at all

#### 2. **Partial Failure Handling**
- ✅ **Great**: Returns successful insights with error details for failed ones
  ```json
  {
    "insights": { "action_items": [...], "sentiment": null },
    "errors": { "sentiment": "Failed after retries" }
  }
  ```
- ⚠️ **Okay**: Fails entire request if one insight fails
- ❌ **Poor**: Doesn't handle multiple LLM calls failing independently

#### 3. **Insight Extraction Structure**
- ✅ **Great**: Creates separate functions for each insight type (clean, reusable)
- ✅ **Good**: All logic in one endpoint (works but less clean)
- ❌ **Poor**: Doesn't modularize the code at all

#### 4. **Prompt Engineering**
- ✅ **Great**: Includes context and clear instructions in prompts
  ```python
  prompt = f"""
  Extract action items from this meeting transcript.
  For each action item, identify:
  - Task description
  - Person responsible
  - Deadline (if mentioned)

  Transcript: {transcript}

  Return JSON format.
  """
  ```
- ⚠️ **Okay**: Minimal prompts that still work
- ❌ **Poor**: Very vague prompts or expects magic

#### 5. **Using AI Tools Effectively**
- ✅ **Great**: Uses AI to generate boilerplate, then customizes for their needs
- ✅ **Good**: Asks AI specific questions about Flask, error handling patterns
- ⚠️ **Okay**: Copies AI-generated code without understanding it
- ❌ **Poor**: Doesn't use AI tools or uses them poorly

### Code Quality Signals

**Green Flags:**
- ✅ Modular functions (not everything in one endpoint)
- ✅ Descriptive variable names
- ✅ Input validation
- ✅ Appropriate HTTP status codes (404, 400, 503, etc.)
- ✅ JSON parsing with error handling
- ✅ Comments explaining design decisions

**Red Flags:**
- ❌ Giant monolithic functions
- ❌ Copy-pasted code with no modification
- ❌ Hardcoded values everywhere
- ❌ No input validation
- ❌ Always returns 200 OK even for errors
- ❌ Doesn't test their code

---

## Phase 3: Testing & Debugging (5-10 minutes)

### What to Look For

**Great candidates:**
- Test endpoints with curl or Postman as they build
- Run the server and verify it works
- Test error cases (invalid IDs, missing fields)
- Run it multiple times to see LLM failures

**Weaker candidates:**
- Write all code without testing anything
- Can't figure out why their code doesn't work
- Don't know how to debug Flask apps

### If They Get Stuck

**Don't immediately give answers.** Instead:

1. Ask clarifying questions:
   - "What are you trying to do here?"
   - "What error are you seeing?"
   - "Have you run this code yet?"

2. Guide them to the solution:
   - "Read the error message carefully - what is it telling you?"
   - "Look at how the llm_client is used in the example at the bottom of the file"
   - "What does the documentation for Flask's jsonify say?"

3. Only if they're truly stuck after 5+ minutes on the same issue, give hints:
   - "You need to catch the LLMAPIError exception"
   - "Flask requires you to return Response objects or tuples for status codes"

---

## Phase 4: Discussion Questions (10-15 minutes)

After implementation, ask:

### System Design Questions

1. **"Walk me through your API design. Why did you make the choices you did?"**
   - Looking for: Thoughtful reasoning, understanding of trade-offs

2. **"How would you handle the LLM being slow (2-5 seconds per call) in production?"**
   - Looking for: Async processing, background jobs, websockets, polling
   - Great answer: "I'd make this async - return 202 Accepted immediately, process in background, provide a webhook or polling endpoint"

3. **"If one insight extractor fails, what should happen?"**
   - Looking for: Partial success handling, user experience thinking
   - Great answer: "Return what succeeded with error details. Partial data is better than no data."

4. **"How would you scale this to 10,000 meetings per day?"**
   - Looking for: Job queues, caching, rate limiting, database optimization
   - Great answer: "Use Redis queue for async processing, cache LLM responses, implement circuit breaker for API calls"

### Production Readiness

5. **"What's missing from your implementation for production?"**
   - Looking for: Auth, logging, monitoring, tests, database, validation
   - Great answer includes: "Authentication, proper database, structured logging, metrics/monitoring, rate limiting, comprehensive error handling"

6. **"How would you monitor LLM reliability?"**
   - Looking for: Metrics, alerting, SLAs
   - Great answer: "Track success rate, latency, failures by error type. Alert if success rate drops below 95%."

### Cost & Optimization

7. **"LLM calls cost money per token. How would you optimize costs?"**
   - Looking for: Caching, prompt optimization, model selection
   - Great answer: "Cache responses by transcript hash, minimize prompt length, use smaller models for simple tasks"

---

## Evaluation Rubric

### Strong Hire (90-100%)
- ✅ Asks thoughtful clarifying questions upfront
- ✅ Designs clean, RESTful API
- ✅ Implements proper error handling with retries
- ✅ Handles partial failures gracefully
- ✅ Tests their code and catches bugs
- ✅ Uses AI tools effectively
- ✅ Writes clean, modular code
- ✅ Gives excellent answers to discussion questions
- ✅ Shows production thinking

### Hire (75-89%)
- ✅ Asks some questions
- ✅ Reasonable API design
- ✅ Basic error handling (try-except)
- ⚠️ May not handle partial failures perfectly
- ✅ Code works and is readable
- ✅ Uses AI tools adequately
- ✅ Decent answers to discussion questions

### Maybe (60-74%)
- ⚠️ Few or no questions asked
- ⚠️ API design is functional but not great
- ⚠️ Minimal error handling
- ⚠️ Code is messy or poorly organized
- ⚠️ Struggles with debugging
- ⚠️ Uses AI tools but doesn't understand output
- ⚠️ Weak on system design questions

### No Hire (<60%)
- ❌ Doesn't ask questions or clarify requirements
- ❌ Poor API design or doesn't complete it
- ❌ No error handling for LLM failures
- ❌ Code doesn't work or is very buggy
- ❌ Can't use AI tools effectively
- ❌ Can't answer basic system design questions
- ❌ No production thinking

---

## Sample Solution Outline

A complete solution should include:

### Endpoints
1. `POST /meetings` - Create meeting
2. `POST /meetings/{id}/prepare` - Pre-meeting context
3. `POST /meetings/{id}/analyze` - Extract insights

### Helper Functions
```python
def call_llm_with_retry(prompt, max_retries=3):
    """Wrapper for LLM calls with retry logic"""
    for attempt in range(max_retries):
        try:
            return llm_client.generate(prompt)
        except LLMAPIError:
            if attempt == max_retries - 1:
                raise
            time.sleep(0.1 * (2 ** attempt))  # Exponential backoff

def extract_action_items(transcript):
    prompt = f"Extract action items from: {transcript}"
    response = call_llm_with_retry(prompt)
    return json.loads(response)

def extract_key_topics(transcript):
    prompt = f"Extract key topics from: {transcript}"
    response = call_llm_with_retry(prompt)
    return json.loads(response)

# ... more extractors
```

### Error Handling Pattern
```python
@app.route('/meetings/<meeting_id>/analyze', methods=['POST'])
def analyze_meeting(meeting_id):
    transcript = request.json.get('transcript')

    insights = {}
    errors = {}

    # Try each extractor independently
    for name, extractor in [
        ('action_items', extract_action_items),
        ('topics', extract_key_topics),
        # ...
    ]:
        try:
            insights[name] = extractor(transcript)
        except Exception as e:
            errors[name] = str(e)
            insights[name] = None

    response = {'meeting_id': meeting_id, 'insights': insights}
    if errors:
        response['errors'] = errors

    return jsonify(response), 200  # or 207 Multi-Status
```

---

## Time Management Tips

- **0-10 min**: Questions, design discussion
- **10-40 min**: Core implementation
- **40-50 min**: Testing, debugging
- **50-60 min**: Cleanup, edge cases
- **60-75 min**: Discussion

**If running behind:**
- At 30 min: "Let's timebox this. Focus on getting one endpoint fully working."
- At 45 min: "We have 15 minutes left. What's most important to complete?"
- At 55 min: "Let's wrap up and discuss what you've built."

**If they finish early:**
- Ask them to add more features
- Have them refactor for better error handling
- Discuss their code and potential improvements
- Jump to discussion questions

---

## Common Pitfalls & How to Handle

### Pitfall 1: Over-engineering
Candidate starts building a complex system with databases, auth, etc.

**Intervention**: "That's great thinking, but let's focus on the core functionality first. Use the mock data provided."

### Pitfall 2: Under-engineering
No error handling, returns 200 for everything, doesn't validate input.

**Probe**: "What happens if the LLM fails? What if the user sends invalid data?"

### Pitfall 3: Analysis Paralysis
Spends 20 minutes discussing design without writing code.

**Intervention**: "This sounds good. Let's start implementing and iterate as we go."

### Pitfall 4: Copy-Paste Without Understanding
Clearly copying AI-generated code without reading it.

**Probe**: "Can you explain what this code does?" "Why did you choose this approach?"

---

## Comparing to Guided Version

Use **this version** when:
- ✅ Candidate has 2+ years experience
- ✅ You want to test product/design thinking
- ✅ You want to see how they handle ambiguity
- ✅ Role requires working with vague requirements

Use **guided version** when:
- ✅ New grad / early career candidates
- ✅ You want to focus purely on coding ability
- ✅ You want consistent evaluation across candidates
- ✅ Limited time for interview

---

## Final Notes

**Remember:**
- This is meant to be challenging and somewhat ambiguous
- Good candidates will ask questions - that's expected and desired
- Focus on their thought process, not just the final code
- The discussion is as important as the implementation
- Look for production thinking and awareness of edge cases

**The goal is to see:**
- How they handle open-ended problems
- How they make decisions under uncertainty
- How they use modern tools (AI assistants)
- Whether they think beyond the happy path

Good luck with the interview!

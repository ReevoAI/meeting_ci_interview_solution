# Interviewer Guide - Meeting Intelligence API Interview

**Duration:** ~75 minutes total
**Level:** Junior/New Grad (smart but less experienced)
**Format:** Live coding with AI assistance encouraged
**Type:** Open-ended API design and implementation

---

## 🔑 Key Interview Principles (READ THIS FIRST!)

### This is a CONVERSATIONAL interview
- **Ask lots of questions during coding:** system design, product sense, trade-offs
- **Encourage questions from candidate:** about API design, business requirements, user needs
- **Give hints liberally:** Share code snippets in chat when they're stuck
- **Engage actively:** Don't just silently watch them code - discuss their choices

### Incremental Development is REQUIRED
- ❌ **Don't let them one-shot the entire solution with AI** - defeats the purpose
- ✅ **Build one endpoint at a time** - implement, test, move to next
- ✅ **Test as they go** - run server and curl after each endpoint
- ✅ **Iterate based on feedback** - see how they adapt and improve

### LLM Failure Rate Strategy
**IMPORTANT: You control when failures happen!**

**Phase 1 - First 25-30 minutes:**
- Keep `failure_rate=0` in `llm_client.py` (line 44)
- Let them build basic functionality without LLM errors
- Focus on API design and getting endpoints working

**Phase 2 - After basic implementation works:**
- Change to `failure_rate=0.2` (20% failure rate)
- Tell them: *"Oh, I should mention - in production this LLM actually fails about 20% of the time. Let me update the config. You'll need to handle these failures."*
- Watch how they debug and add error handling
- This tests: resilience, debugging skills, error handling patterns

---

## 📋 Pre-Interview Checklist

Before the interview:
- [ ] Review this entire guide
- [ ] Clone/pull the latest version of the repo
- [ ] Test that `python api.py` starts successfully
- [ ] Verify `llm_client.py` and `data.py` are working
- [ ] Have the sample solution (`api.py`) ready for reference
- [ ] Prepare screen sharing setup

---

## 🎯 Interview Overview

### What This Tests

✅ **Product Thinking** - Can they translate business requirements into technical design?
✅ **API Design** - Do they understand REST principles and endpoint structure?
✅ **Error Handling** - Do they think about failure cases without being told?
✅ **AI Tool Usage** - How effectively do they use ChatGPT/Claude/Copilot?
✅ **Problem Solving** - Can they work through ambiguity and make decisions?
✅ **Code Quality** - Is the code readable, organized, and maintainable?

### What This Doesn't Test

❌ Advanced system design (scaling, databases, architecture)
❌ Frontend development
❌ Deep algorithm knowledge
❌ Production ops (deployment, monitoring, etc.)

### Expected Outcome

A **strong junior candidate** will produce:
- 3-4 working API endpoints (create, get, prepare, analyze)
- Basic retry logic for LLM failures (simple loop)
- Proper HTTP status codes (400, 404, 503)
- Reasonably clean code (~200-300 lines)
- Partial success handling (if one insight fails, others succeed)

The code will have rough edges - that's expected! Look for understanding over perfection.

---

## 📝 Interview Script

## Part 1: Introduction (5 minutes)

### What to Say:

> "Hi [Candidate Name]! Welcome to the interview. Today you'll be building a REST API for a meeting intelligence platform - think of products like Gong or Fireflies that help sales teams prepare for meetings and extract insights from transcripts.
>
> This is an open-ended problem where you'll design and implement the API. You'll decide what endpoints to create, how to structure the data, and how to handle errors.
>
> **Important guidelines:**
> - **Use AI coding assistants** (ChatGPT, Claude, Copilot) - we want to see how you work in a real development environment
> - **Build incrementally** - implement one endpoint at a time, test it, then move to the next. Don't try to generate everything at once
> - **Ask questions** - about requirements, design choices, trade-offs. This is a conversation, not a silent coding test
> - I'll be asking you questions too and might share code snippets if you get stuck - that's totally fine!
>
> We have about 75 minutes total:
> - ~10 minutes for questions and planning
> - ~55 minutes for implementation
> - ~10 minutes for discussion
>
> Before we start coding, please read through `problem.md` to understand the requirements. Take about 5 minutes, then we'll discuss any questions you have."

### While They Read:

- ⏱️ **Give them 5 minutes of silence to read**
- Watch if they also open `llm_client.py` and `data.py` (good sign!)
- Note if they start asking questions immediately without reading (red flag)

---

## Part 2: Questions & Planning (5-10 minutes)

### Strong Candidates Will Ask:

**About API Design:**
- "What endpoints should I create? Should I combine features or separate them?"
- "What should the request/response format look like?"
- "Should meetings be created before they happen, or only after?"
- "How should I structure the meeting object?"

**About Requirements:**
- "What specific insights should I extract from transcripts?"
- "For action items, what fields matter? Task, owner, deadline, priority?"
- "Should sentiment be a number, text, or both?"

**About Error Handling:**
- "The LLM fails sometimes - should I retry? How many times?"
- "What happens if one insight fails but others succeed?"
- "What HTTP status codes should I use?"

**About Scope:**
- "How far should I get in 75 minutes? What's most important?"
- "Should I implement all the insight types or focus on a few?"

### How to Respond:

**Good Questions → Answer with Guidance (not solutions):**

Q: "What insights should I extract?"
A: "What would be valuable for a salesperson preparing for their next meeting? Use your judgment - pick 3-4 insight types."

Q: "Should I retry failed LLM calls?"
A: "What would you do in production? Think about user experience."

Q: "Separate endpoints or combined?"
A: "Both approaches have trade-offs. What makes sense to you and why?"

Q: "How should I structure the insights?"
A: "Look at the historical meetings in `data.py` for inspiration. Structure it however makes sense."

**If They Ask No Questions:**

After 2-3 minutes of silence: "Before you start coding, can you walk me through your plan? What endpoints will you build?"

This forces them to think through the design before diving in.

### Red Flags:

❌ No questions at all - just starts coding blindly
❌ Asks you to design the API for them
❌ Only asks syntax questions ("How do I use Flask?")
❌ Wants extremely detailed specs before starting

### Green Flags:

✅ Asks clarifying questions about business requirements
✅ Thinks about edge cases and error scenarios
✅ Sketches out API design before coding
✅ Balances between asking questions and making decisions

---

## Part 3: Implementation (40-55 minutes)

### Timeline Checkpoints:

**10 minutes in:**
- ✅ Should have: Basic Flask app structure, maybe one endpoint started
- 🚨 Red flag: Still reading docs or not typing code yet

**25 minutes in:**
- ✅ Should have: Create meeting endpoint working, starting on prepare or analyze
- 🚨 Red flag: Still stuck on basic Flask syntax

**40 minutes in:**
- ✅ Should have: 2-3 endpoints working, implementing LLM integration
- 🚨 Red flag: No working endpoints yet

**55 minutes in:**
- ✅ Should have: Core functionality complete, testing/debugging
- 🚨 Red flag: Code doesn't run or has major bugs

### What to Watch For:

#### 1. **API Design Quality**

**Great Design:**
```
POST   /meetings                    # Create meeting
GET    /meetings/{id}               # Get meeting details
POST   /meetings/{id}/prepare       # Pre-meeting prep
POST   /meetings/{id}/analyze       # Analyze transcript
```

**Acceptable Design:**
```
POST   /meetings                    # Create meeting
POST   /meetings/{id}/insights      # Analyze (combined)
GET    /meetings/{id}               # Get everything
```

**Poor Design:**
```
POST   /create_new_meeting          # Non-RESTful naming
POST   /analyze                     # Missing resource hierarchy
GET    /get_meeting_by_id/{id}      # Redundant naming
```

#### 2. **Error Handling Approach**

**Great:**
```python
def retry_llm_call(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return llm_client.generate(prompt)
        except LLMAPIError:
            if attempt == max_retries - 1:
                raise
            time.sleep(0.2)
```

**Good:**
```python
try:
    response = llm_client.generate(prompt)
except LLMAPIError:
    try:
        response = llm_client.generate(prompt)  # Retry once
    except:
        return error
```

**Poor:**
```python
response = llm_client.generate(prompt)  # No error handling!
```

#### 3. **Partial Failure Handling**

**Great:**
```python
insights = {}
errors = {}

try:
    insights['action_items'] = extract_action_items(transcript)
except Exception as e:
    errors['action_items'] = str(e)
    insights['action_items'] = None

try:
    insights['sentiment'] = extract_sentiment(transcript)
except Exception as e:
    errors['sentiment'] = str(e)
    insights['sentiment'] = None

return jsonify({"insights": insights, "errors": errors})
```

**Acceptable:**
```python
try:
    insights = extract_all_insights(transcript)
    return jsonify(insights)
except Exception as e:
    return jsonify({"error": str(e)}), 500
```

**Poor:**
```python
insights = extract_all_insights(transcript)  # No try-except!
return jsonify(insights)
```

#### 4. **Code Organization**

**Green Flags:**
- ✅ Helper functions for retry logic
- ✅ Separate functions for each insight type
- ✅ Clear variable names
- ✅ Proper HTTP status codes (200, 201, 400, 404, 503)
- ✅ Input validation
- ✅ Comments explaining key decisions

**Red Flags:**
- ❌ Everything in one giant function
- ❌ Copy-pasted code with no modification
- ❌ No error handling
- ❌ Always returns 200 OK
- ❌ Doesn't test their code as they go

#### 5. **AI Tool Usage**

**Great Usage:**
- Uses AI to generate boilerplate Flask code
- Asks AI specific questions ("How do I retry with exponential backoff in Python?")
- Reviews and customizes AI-generated code
- Understands what the AI wrote

**Poor Usage:**
- Blindly copies entire functions without reading
- Can't explain what the AI-generated code does
- Doesn't use AI at all (missing the point of the exercise)

### When to Intervene:

**Let them struggle for 5-10 minutes** before helping. Learning happens through struggle.

**Intervene if:**
- ❌ Stuck on the same syntax error for 10+ minutes
- ❌ Going down completely wrong path (like building a database from scratch)
- ❌ Clearly confused about what the problem is asking

**How to Intervene:**

1️⃣ **Ask clarifying questions first:**
   - "What are you trying to do here?"
   - "What's the error telling you?"
   - "Walk me through your thinking"

2️⃣ **Guide, don't solve:**
   - "Look at how the llm_client is used at the bottom of `llm_client.py`"
   - "What does the Flask documentation say about returning status codes?"
   - "Have you tested this endpoint yet?"

3️⃣ **Only give direct hints if truly stuck (10+ minutes):**
   - "You need to catch the `LLMAPIError` exception"
   - "Flask requires returning a tuple for status codes: `return jsonify(...), 201`"

### Common Issues & How to Handle:

**Issue: "I don't know Flask"**
→ "That's fine! Use ChatGPT or the Flask docs. Just ask it 'how do I create a POST endpoint in Flask?'"

**Issue: Spends 20 minutes designing, no code written**
→ "Let's start implementing. You can iterate on the design as you go."

**Issue: Code doesn't work, can't debug**
→ "Run the server and test with curl. What error do you get?"

**Issue: Over-engineering (adding auth, database, etc.)**
→ "Good thinking for production, but let's focus on the core features first. Use the mock data provided."

---

## Part 4: Testing & Debugging (5-10 minutes)

### What Strong Candidates Do:

✅ Test endpoints with `curl` or Postman as they build
✅ Run the server frequently to catch errors early
✅ Test error cases (invalid IDs, missing fields)
✅ Run multiple times to observe LLM failures
✅ Fix bugs quickly

### What Weak Candidates Do:

❌ Write all code without testing anything
❌ Don't know how to test an API
❌ Can't figure out why their code doesn't work
❌ Blame the framework or tools

### Testing Commands (Share if they ask):

```bash
# Create a meeting
curl -X POST http://localhost:5000/meetings \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_1",
    "contact_id": "contact_1",
    "title": "Product Demo",
    "scheduled_date": "2025-11-20T14:00:00"
  }'

# Get meeting
curl http://localhost:5000/meetings/{meeting_id}

# Prepare for meeting
curl -X POST http://localhost:5000/meetings/{meeting_id}/prepare

# Analyze transcript
curl -X POST http://localhost:5000/meetings/{meeting_id}/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "Sarah: Thanks for joining Jennifer. Jennifer: Happy to be here. We discussed the new features and pricing. Sarah: I will send the proposal by Friday."
  }'
```

---

## Part 5: Discussion Questions (10-15 minutes)

After implementation, ask these questions to evaluate thinking depth:

### 1. System Design & Architecture

**Q: "Walk me through your API design. Why did you structure it this way?"**

Looking for:
- ✅ Thoughtful reasoning about endpoint organization
- ✅ Understanding of REST principles
- ✅ Consideration of the user journey (before meeting → after meeting)

Great answer: "I separated `/prepare` and `/analyze` because they happen at different stages of the meeting lifecycle. Before the meeting, you need context. After, you need insights. Keeping them separate makes the API clearer and lets us optimize each independently."

Weak answer: "I just made some endpoints that seemed right."

---

**Q: "The LLM takes 2-5 seconds per call. How would you handle this in production?"**

Looking for:
- ✅ Understanding that synchronous calls block the user
- ✅ Knowledge of async patterns (background jobs, webhooks, polling)
- ✅ Thinking about user experience

Great answer: "I'd make this async. Return 202 Accepted immediately, process in the background with Celery or similar, then either webhook the client or provide a polling endpoint. Users shouldn't wait 10+ seconds for a response."

Good answer: "Maybe use async/await in Python to make it non-blocking?"

Weak answer: "Just make the LLM faster" or "I don't know."

---

**Q: "If one insight extractor fails, what should happen to the others?"**

Looking for:
- ✅ Understanding of partial failure patterns
- ✅ User-centric thinking
- ✅ Graceful degradation

Great answer: "Return what succeeded with error details. Partial data is better than no data. Users can still get action items even if sentiment analysis failed. Include an 'errors' field so they know what went wrong."

Weak answer: "Fail the whole request" or "Just retry until it works."

---

### 2. Production Readiness

**Q: "What's missing from your implementation for production?"**

Looking for:
- ✅ Awareness of real-world requirements
- ✅ Understanding of production concerns
- ✅ Growth mindset

Great answer covers several areas:
- "Authentication - users should only access their own data"
- "Proper database instead of in-memory dict"
- "Structured logging for debugging"
- "Monitoring - track LLM success rates, endpoint latency"
- "Input validation library like Pydantic"
- "Rate limiting to prevent abuse"
- "Unit and integration tests"

Good answer covers 2-3 areas.

Weak answer: "Nothing, it's production ready" or "I don't know."

---

**Q: "How would you monitor LLM reliability?"**

Looking for:
- ✅ Understanding of observability
- ✅ Practical metrics
- ✅ Actionable alerting

Great answer: "Track success rate, latency, and error types. Alert if success rate drops below 95% or latency exceeds SLA. Log failed prompts for debugging. Monitor cost per request to catch anomalies."

Good answer: "Log when it fails and track success rate."

Weak answer: "Just check if it's down."

---

### 3. Cost & Optimization

**Q: "LLM calls cost money per token. How would you optimize costs?"**

Looking for:
- ✅ Understanding of LLM pricing models
- ✅ Practical optimization strategies
- ✅ Trade-off thinking

Great answer: "Cache responses by transcript hash - same transcript = same insights. Optimize prompts to use fewer tokens. Use smaller/cheaper models for simple tasks like topic extraction. Batch requests when possible."

Good answer: "Cache the results" or "Use shorter prompts."

Weak answer: "I don't know" or "Don't worry about cost."

---

**Q: "How would you scale this to handle 10,000 meetings per day?"**

Looking for:
- ✅ Understanding of scalability patterns
- ✅ Knowledge of relevant technologies
- ✅ Practical solutions

Great answer: "Use Redis queue for async processing. Multiple workers process jobs concurrently. Database with proper indexes. Cache LLM responses. Rate limiting and circuit breakers for the LLM API. Horizontal scaling with load balancer."

Good answer: "Use a job queue and multiple servers."

Weak answer: "Just use a bigger server" or "I don't know."

---

## 📊 Evaluation Rubric

### Strong Hire (85-100%)

**Technical Execution:**
- ✅ 3-4 working endpoints with proper REST design
- ✅ Implements retry logic for LLM failures
- ✅ Handles partial failures gracefully
- ✅ Proper HTTP status codes (400, 404, 503)
- ✅ Clean, readable code with good organization
- ✅ Tests their code as they build

**Problem Solving:**
- ✅ Asks thoughtful clarifying questions
- ✅ Makes good design decisions with reasoning
- ✅ Uses AI tools effectively
- ✅ Debugs issues quickly

**Discussion:**
- ✅ Strong answers to system design questions
- ✅ Shows production thinking
- ✅ Understands trade-offs and can articulate them

**Overall:** Would be productive with minimal supervision. Shows strong fundamentals and growth potential.

---

### Hire (70-84%)

**Technical Execution:**
- ✅ 2-3 working endpoints
- ✅ Basic error handling (try-except)
- ⚠️ May not handle partial failures perfectly
- ✅ Most HTTP status codes correct
- ✅ Code works but could be cleaner
- ✅ Does some testing

**Problem Solving:**
- ✅ Asks some questions
- ✅ Reasonable design decisions
- ✅ Uses AI tools adequately
- ⚠️ May struggle with debugging but figures it out

**Discussion:**
- ✅ Decent answers to system design questions
- ⚠️ Limited production experience showing
- ✅ Understands basic trade-offs

**Overall:** Would be productive with some guidance. Has solid fundamentals and can grow.

---

### Maybe / Borderline (55-69%)

**Technical Execution:**
- ⚠️ 1-2 working endpoints, others incomplete
- ⚠️ Minimal error handling
- ⚠️ Missing some HTTP status codes
- ⚠️ Code is messy or poorly organized
- ⚠️ Limited testing, bugs remain

**Problem Solving:**
- ⚠️ Few questions asked
- ⚠️ Design decisions seem arbitrary
- ⚠️ Uses AI but doesn't understand output
- ⚠️ Struggles with debugging

**Discussion:**
- ⚠️ Weak answers to system design questions
- ⚠️ Little production awareness
- ⚠️ Doesn't understand trade-offs well

**Overall:** Would need significant mentoring. May not be ready yet.

**Recommendation:** Pass unless team has strong mentorship capacity.

---

### No Hire (<55%)

**Technical Execution:**
- ❌ Few or no working endpoints
- ❌ No error handling
- ❌ Incorrect or missing status codes
- ❌ Code doesn't run or has major bugs
- ❌ Doesn't test anything

**Problem Solving:**
- ❌ Doesn't ask clarifying questions
- ❌ Poor or no design decisions
- ❌ Can't use AI tools effectively
- ❌ Can't debug basic issues

**Discussion:**
- ❌ Can't answer basic system design questions
- ❌ No understanding of production concerns
- ❌ No awareness of trade-offs

**Overall:** Not ready for the role. Needs more foundational learning.

---

## 🎯 Sample Solution Analysis

The provided `api.py` represents a **strong junior candidate's solution** (~75 minutes):

### What's Good:

✅ **~250 lines** - Right size for time limit
✅ **4 working endpoints** - create, get, prepare, analyze
✅ **Simple retry logic** - Basic loop with fixed delay
✅ **Partial failure handling** - Each insight extracted independently
✅ **Proper status codes** - 200, 201, 400, 404, 503
✅ **Input validation** - Checks required fields and existence
✅ **Clean structure** - Helper function for retries, clear endpoint organization

### What's "Junior":

⚠️ **Fixed retry delay** - Not exponential backoff (but good enough!)
⚠️ **Inline logic** - Could be more modular (but readable!)
⚠️ **Basic prompts** - Could be more sophisticated (but work!)
⚠️ **No logging** - Production would need it (but not expected!)
⚠️ **Simple validation** - Just checks required fields (but sufficient!)

### Teaching Points:

Use this solution to calibrate your expectations:
- This is what "strong junior" looks like
- It works, but has room for growth
- It shows understanding without over-engineering
- This candidate would be a **Hire** - solid fundamentals, good potential

---

## 📞 Candidate Communication

### Opening the Interview:

Be warm and welcoming:
- "We're excited to see how you approach problems"
- "Use whatever tools you normally use - AI assistants are encouraged"
- "Ask questions when you need to - we want to see your thought process"

### During the Interview:

Be supportive but not leading:
- "That's an interesting approach, tell me more"
- "What made you decide to do it that way?"
- "Walk me through your thinking here"

### Closing the Interview:

Be positive regardless of outcome:
- "Thanks for working through this with me today"
- "We'll be in touch within [timeframe]"
- "Do you have any questions for me?"

---

## ⏱️ Time Management

### If They're Running Behind:

**At 30 min with no working endpoints:**
"Let's timebox this. Focus on getting one complete flow working - create a meeting and analyze a transcript. We can discuss the other features."

**At 45 min with only 1 endpoint:**
"We have about 10 minutes left for coding. What's the most important thing to complete?"

**At 55 min:**
"Let's wrap up coding in the next 5 minutes, then we'll discuss what you've built."

### If They Finish Early:

**Great problem! Additional challenges:**
- "Can you add input validation for date formats?"
- "How would you cache LLM responses?"
- "Can you refactor to reduce code duplication?"
- "Add a follow-up recommendations extractor"

Then move to discussion questions.

---

## 🚩 Red Flags to Watch For

### Critical Red Flags (Usually No Hire):

❌ **Can't get anything working** - Basic Flask syntax issues, can't debug
❌ **No error handling** - Doesn't think about failure cases at all
❌ **Doesn't test code** - Writes everything then tries to run once
❌ **Can't explain decisions** - "I don't know" to most questions
❌ **Copies AI code blindly** - Can't explain what it does

### Warning Signs (Maybe/Borderline):

⚠️ **Asks no questions** - Doesn't clarify ambiguous requirements
⚠️ **Poor time management** - Spends 40 min on one endpoint
⚠️ **Messy code** - Variable names like `x`, `data1`, `temp`
⚠️ **Analysis paralysis** - Overthinks design, doesn't start coding
⚠️ **Weak on discussion** - Can't think beyond the immediate solution

---

## ✅ Final Checklist

After the interview, evaluate:

- [ ] Did they ask good clarifying questions?
- [ ] Did they design a reasonable API?
- [ ] Did they implement error handling for LLM failures?
- [ ] Did they test their code?
- [ ] Is the code readable and organized?
- [ ] Did they use AI tools effectively?
- [ ] Could they explain their decisions?
- [ ] Did they show production thinking in discussion?
- [ ] Would they be productive with appropriate mentoring?
- [ ] Do they show potential for growth?

**Hire if:** 7+ checkmarks
**Maybe if:** 5-6 checkmarks
**No hire if:** <5 checkmarks

---

## 📚 Additional Notes

### This Interview Works Best For:

✅ Junior/New grad engineers (0-2 years)
✅ Candidates comfortable with Python
✅ Roles requiring API development
✅ Teams that use AI coding tools
✅ Open-ended problem solvers

### Alternative Use Cases:

- Remove AI tools requirement for traditional coding assessment
- Extend to 90 minutes for more thorough solutions
- Add specific requirements (auth, database) for mid-level candidates
- Use discussion only for senior candidates (assume implementation is easy)

### Tips for First-Time Interviewers:

1. **Read the solution first** - Understand what good looks like
2. **Let them struggle** - Don't jump in too quickly
3. **Take notes** - You'll forget details later
4. **Be consistent** - Use this rubric for all candidates
5. **Calibrate** - Discuss borderline cases with other interviewers

---

## 🎉 Good Luck!

Remember: You're evaluating **potential, not perfection**. Look for candidates who:
- Think clearly about problems
- Handle ambiguity well
- Write working code
- Show awareness of production concerns
- Can learn and grow

The goal is to find engineers who will be successful on your team, not to stump them with trick questions.

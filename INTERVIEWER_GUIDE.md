# Interviewer Guide

**70-minute service layer interview** - Algorithm design, error handling, clean code.

---

## Setup (5 min)

- Point them to `README.md` and `problem.md`  
- Confirm: `pip install -r requirements.txt`
- Show tests: `python run_tests.py phase1`

---

## Phase 1: Models (10 min)

**Complete Pydantic models**

Look for: Do they read existing code? Ask domain questions?

✅ Models complete, tests pass

---

## Phase 2: CRUD (15 min)

**Design first** (5 min): "How would you implement get_all_meetings()? Edge cases?"  
**Then implement** (10 min): Can use AI tools

Watch for: Input validation, error handling, clean code

✅ Functions work, proper errors, readable code

---

## Phase 3: Availability Algorithm (20 min) 🔥

**THE MAIN CHALLENGE** - Spend time here!

**Design** (10 min): Whiteboard the approach
- Get meetings → merge intervals → find gaps → filter to work hours

**Implement** (10 min): Code and debug with tests

Edge cases: Empty users? No meetings? Fully booked?

✅ Correct interval merging, handles edges, tests pass

---

## Phase 4: LLM Prep (10 min)

**Generate meeting prep using LLM**

Flow: Get meeting → fetch history → build prompt → parse JSON

Watch for: Prompt quality, JSON parsing, edge cases (first meeting)

✅ Reasonable prompt, parses response, handles no history

---

## Phase 5: Retry Logic (5 min)

**Add exponential backoff** (LLM fails ~30%)

Key: 3 retries, backoff 0.1s/0.2s/0.4s, don't retry ValueError

✅ Retry works, proper backoff, doesn't retry bad input

---

## Evaluation

**Must have:** Working CRUD + algorithm, most tests pass  
**Strong:** All tests pass, clean code, thinks about edges  
**Excellent:** Above + proactive, asks questions, discusses tradeoffs

---

## Common Struggles

**Phase 3:** Interval merging → walk through whiteboard example  
**Time:** Too long on Phase 2 → "Looks good, let's move on"

---

## If Time Permits

- "How would you scale to millions of meetings?"
- "Production changes? Monitoring?"
- "What other tests would you add?"

---

## Red Flags 🚩

- Can't implement basic CRUD
- No error handling  
- Messy code, doesn't test
- Gives up on algorithm

## Green Flags ✅

- Asks clarifying questions
- Thinks about edges proactively
- Tests frequently
- Explains reasoning clearly


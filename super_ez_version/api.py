"""
Meeting Intelligence API - Flask Backend

This is the main API file. Implement the TODO sections below.
Run this file with: python api.py
"""

from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import time
import json

# Import our mock database and LLM client
import data
from llm_client import MockLLMClient, LLMAPIError

app = Flask(__name__)

# Initialize the mock LLM client
# NOTE: This client fails randomly ~20% of the time!
# You MUST implement error handling and retry logic
llm_client = MockLLMClient(simulate_latency=False)


# ============================================================================
# PART 1: Create Meeting Endpoint
# ============================================================================

@app.route('/meetings', methods=['POST'])
def create_meeting():
    """
    Create a new meeting

    Request body:
    {
        "title": "Q4 Planning with Acme Corp",
        "contact_id": "contact_2",
        "user_id": "user_1",
        "scheduled_time": "2025-11-15T10:00:00",
        "status": "scheduled"
    }

    Response:
    {
        "meeting_id": "meeting_123",
        "message": "Meeting created successfully"
    }
    """
    # TODO: Implement this endpoint
    #
    # Steps:
    # 1. Get JSON data from request
    # 2. Validate required fields (title, contact_id, user_id, scheduled_time)
    # 3. Validate that user_id exists (use data.user_exists())
    # 4. Validate that contact_id exists (use data.contact_exists())
    # 5. Generate a unique meeting_id (hint: use str(uuid.uuid4()) or "meeting_" + str(uuid.uuid4())[:8])
    # 6. Create meeting object with all fields plus the generated ID
    # 7. Add meeting to database (use data.add_meeting())
    # 8. Return success response with meeting_id
    #
    # Error handling:
    # - Return 400 if required fields are missing
    # - Return 404 if user_id or contact_id don't exist
    # - Return 400 for any other validation errors

    pass  # Remove this and implement


# ============================================================================
# PART 2: Pre-Meeting Context Endpoint
# ============================================================================

@app.route('/meetings/<meeting_id>/prepare', methods=['POST'])
def prepare_meeting(meeting_id):
    """
    Generate pre-meeting context to help user prepare

    Request body:
    {
        "user_id": "user_1"
    }

    Response:
    {
        "meeting_id": "meeting_123",
        "context": {
            "contact_summary": "...",
            "recent_interactions": "...",
            "suggested_topics": [...],
            "pending_action_items": [...]
        }
    }
    """
    # TODO: Implement this endpoint
    #
    # Steps:
    # 1. Verify the meeting exists (use data.meeting_exists())
    # 2. Get the meeting details (use data.get_meeting())
    # 3. Get the contact information (use data.get_contact())
    # 4. Get historical meetings with this contact (use data.get_historical_meetings_for_contact())
    # 5. Build a prompt for the LLM that includes:
    #    - Meeting title
    #    - Contact name, role, company
    #    - Summaries from past meetings
    #    - Request for: contact summary, recent interactions, suggested topics, pending items
    # 6. Call llm_client.generate() with your prompt
    # 7. Parse the JSON response from the LLM
    # 8. Return structured response
    #
    # Error handling:
    # - Return 404 if meeting doesn't exist
    # - Return 400 if contact not found
    # - IMPORTANT: The LLM client fails randomly ~20% of the time!
    #   * Wrap llm_client.generate() in try-except to catch LLMAPIError
    #   * Implement retry logic (try 3 times with brief delays)
    #   * Return 503 (Service Unavailable) if all retries fail
    #   * Example:
    #       for attempt in range(3):
    #           try:
    #               result = llm_client.generate(prompt)
    #               break
    #           except LLMAPIError as e:
    #               if attempt == 2:  # Last attempt
    #                   return jsonify({"error": "LLM service unavailable"}), 503
    #               time.sleep(0.1)  # Brief delay before retry

    pass  # Remove this and implement


# ============================================================================
# PART 3: Post-Meeting Analysis Endpoint
# ============================================================================

@app.route('/meetings/<meeting_id>/analyze', methods=['POST'])
def analyze_meeting(meeting_id):
    """
    Extract insights from meeting transcript

    Request body:
    {
        "transcript": "Long transcript text...",
        "user_id": "user_1"
    }

    Response:
    {
        "meeting_id": "meeting_123",
        "insights": {
            "action_items": [...],
            "key_topics": [...],
            "sentiment": {...},
            "follow_ups": [...]
        }
    }
    """
    # TODO: Implement this endpoint
    #
    # Steps:
    # 1. Verify meeting exists
    # 2. Get transcript from request body
    # 3. Call the 4 insight extraction functions (implement below)
    # 4. Aggregate all insights into a single response
    # 5. Store insights with the meeting (use data.update_meeting())
    # 6. Return combined insights
    #
    # Error handling:
    # - Return 404 if meeting doesn't exist
    # - Return 400 if transcript is missing
    # - IMPORTANT: Handle partial failures gracefully!
    #   * Each extractor calls the LLM, which fails ~20% of the time
    #   * Wrap EACH extractor call in try-except
    #   * If one extractor fails (even after retries), still return results from others
    #   * Example structure:
    #       insights = {}
    #       errors = {}
    #
    #       try:
    #           insights["action_items"] = extract_action_items(transcript)
    #       except Exception as e:
    #           errors["action_items"] = str(e)
    #           insights["action_items"] = None
    #
    #       # Repeat for other extractors...
    #
    #       response = {
    #           "meeting_id": meeting_id,
    #           "insights": insights
    #       }
    #       if errors:
    #           response["errors"] = errors
    #           response["partial_success"] = True
    #
    # Question to think about: Should you return 200 (success) or 207 (partial success)
    # or 500 (error) if some extractors fail? What's best for the client?

    pass  # Remove this and implement


# ============================================================================
# Helper Functions for Insight Extraction
# ============================================================================

def extract_action_items(transcript):
    """
    Extract action items from transcript

    Args:
        transcript: The meeting transcript text

    Returns:
        List of action items with structure:
        [
            {
                "task": "Send pricing proposal",
                "owner": "John",
                "deadline": "2025-11-20",
                "priority": "high"
            },
            ...
        ]

    Raises:
        Exception: If LLM call fails after retries
    """
    # TODO: Implement this function
    #
    # Steps:
    # 1. Create a prompt asking the LLM to extract action items from the transcript
    # 2. Include instructions to identify: task, owner, deadline, priority
    # 3. Call llm_client.generate() with your prompt (with retry logic!)
    # 4. Parse the JSON response
    # 5. Return the action_items list
    #
    # IMPORTANT: Implement retry logic since LLM fails ~20% of the time
    # - Try up to 3 times
    # - Catch LLMAPIError
    # - Add small delay between retries (time.sleep(0.1))
    # - If all retries fail, raise an exception
    #
    # Example prompt structure:
    # "Extract action items from this meeting transcript. For each action item, identify
    #  the task, who is responsible (owner), deadline if mentioned, and priority level.
    #
    #  Transcript:
    #  {transcript}
    #
    #  Return a JSON object with an 'action_items' array."

    pass  # Remove this and implement


def extract_key_topics(transcript):
    """
    Extract key topics discussed in the meeting

    Args:
        transcript: The meeting transcript text

    Returns:
        List of key topics (strings)

    Raises:
        Exception: If LLM call fails after retries
    """
    # TODO: Implement this function
    #
    # Similar to extract_action_items but ask for key topics/themes discussed
    # Remember to implement retry logic for the LLM call!

    pass  # Remove this and implement


def analyze_sentiment(transcript):
    """
    Analyze sentiment and relationship health

    Args:
        transcript: The meeting transcript text

    Returns:
        Dictionary with structure:
        {
            "score": 0.8,  # 0-1 scale
            "summary": "Positive and collaborative",
            "relationship_health": "strong"
        }

    Raises:
        Exception: If LLM call fails after retries
    """
    # TODO: Implement this function
    #
    # Ask LLM to analyze the tone of the conversation and relationship health
    # Remember to implement retry logic for the LLM call!

    pass  # Remove this and implement


def generate_follow_ups(transcript):
    """
    Generate follow-up recommendations

    Args:
        transcript: The meeting transcript text

    Returns:
        List of follow-up action strings

    Raises:
        Exception: If LLM call fails after retries
    """
    # TODO: Implement this function
    #
    # Ask LLM for recommended next steps and follow-ups
    # Remember to implement retry logic for the LLM call!

    pass  # Remove this and implement


# ============================================================================
# Health Check Endpoint (Already Implemented)
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Meeting Intelligence API",
        "timestamp": datetime.utcnow().isoformat()
    })


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


# ============================================================================
# Run the Application
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Meeting Intelligence API")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    print()
    print("Available endpoints:")
    print("  GET  /health                         - Health check")
    print("  POST /meetings                       - Create a meeting")
    print("  POST /meetings/<id>/prepare          - Generate pre-meeting context")
    print("  POST /meetings/<id>/analyze          - Analyze meeting transcript")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)

    app.run(debug=True, port=5000)

"""
Meeting Intelligence API

Sample solution for the meeting intelligence platform.
This represents what a strong junior candidate might produce in ~70 minutes.
"""

from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import json
import time

import data
from llm_client import MockLLMClient, LLMAPIError

app = Flask(__name__)
llm_client = MockLLMClient()


# ============================================================================
# Helper Functions
# ============================================================================

def retry_llm_call(prompt, max_retries=3):
    """
    Simple retry wrapper for LLM calls
    Tries up to max_retries times with a small delay between attempts
    """
    for attempt in range(max_retries):
        try:
            response = llm_client.generate(prompt)
            return response
        except LLMAPIError as e:
            if attempt == max_retries - 1:
                raise  # Give up after max retries
            time.sleep(0.2)  # Wait a bit before retrying


# ============================================================================
# Endpoints
# ============================================================================

@app.route('/meetings', methods=['POST'])
def create_meeting():
    """
    Create a new meeting

    Expects JSON body with:
    - user_id
    - contact_id
    - title
    - scheduled_date
    """
    body = request.get_json()

    # Validate required fields
    if not body:
        return jsonify({"error": "Request body required"}), 400

    required = ['user_id', 'contact_id', 'title', 'scheduled_date']
    for field in required:
        if field not in body:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Check if user and contact exist
    if not data.user_exists(body['user_id']):
        return jsonify({"error": "User not found"}), 404

    if not data.contact_exists(body['contact_id']):
        return jsonify({"error": "Contact not found"}), 404

    # Create the meeting
    meeting_id = f"meeting_{uuid.uuid4().hex[:8]}"
    meeting = {
        "id": meeting_id,
        "user_id": body['user_id'],
        "contact_id": body['contact_id'],
        "title": body['title'],
        "scheduled_date": body['scheduled_date'],
        "created_at": datetime.utcnow().isoformat(),
        "transcript": None,
        "insights": None
    }

    data.add_meeting(meeting)

    return jsonify({"meeting_id": meeting_id, "meeting": meeting}), 201


@app.route('/meetings/<meeting_id>', methods=['GET'])
def get_meeting(meeting_id):
    """Get a specific meeting by ID"""
    meeting = data.get_meeting(meeting_id)

    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404

    return jsonify(meeting), 200


@app.route('/meetings/<meeting_id>/prepare', methods=['POST'])
def prepare_for_meeting(meeting_id):
    """
    Generate pre-meeting context and talking points
    Looks at past meetings with this contact to help prepare
    """
    meeting = data.get_meeting(meeting_id)
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404

    contact = data.get_contact(meeting['contact_id'])
    if not contact:
        return jsonify({"error": "Contact not found"}), 404

    # Get historical meetings with this contact
    past_meetings = data.get_historical_meetings_for_contact(meeting['contact_id'])

    # Build context for the LLM prompt
    contact_info = f"{contact['name']} - {contact['role']} at {contact['company']}"

    history = ""
    if past_meetings:
        history = f"\n\nPast meetings ({len(past_meetings)} total):\n"
        for m in past_meetings[:3]:  # Just show last 3
            history += f"- {m['date']}: {m['title']}\n"
            if 'summary' in m:
                history += f"  Summary: {m['summary']}\n"
    else:
        history = "\n\nThis is your first meeting with this contact."

    prompt = f"""Help me prepare for an upcoming meeting.

Contact: {contact_info}
{history}

Please provide:
1. A brief summary of our relationship with this contact
2. Key points from recent interactions
3. 3-5 suggested talking points for the meeting
4. Any pending action items we should follow up on

Return as JSON with keys: contact_summary, recent_interactions, suggested_topics (array), pending_action_items (array)
"""

    try:
        # Call LLM with retry logic
        response = retry_llm_call(prompt)
        prep_data = json.loads(response)

        # Save the prep data to the meeting
        data.update_meeting(meeting_id, {"prep": prep_data})

        return jsonify({
            "meeting_id": meeting_id,
            "preparation": prep_data
        }), 200

    except LLMAPIError as e:
        return jsonify({
            "error": "Failed to generate preparation context",
            "details": str(e)
        }), 503
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse LLM response"}), 500


@app.route('/meetings/<meeting_id>/analyze', methods=['POST'])
def analyze_transcript(meeting_id):
    """
    Analyze a meeting transcript and extract insights

    Expects JSON body with:
    - transcript: the meeting transcript text

    Extracts:
    - Action items
    - Key topics
    - Sentiment
    """
    meeting = data.get_meeting(meeting_id)
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404

    body = request.get_json()
    if not body or 'transcript' not in body:
        return jsonify({"error": "transcript field required"}), 400

    transcript = body['transcript']

    insights = {}
    errors = {}

    # Extract action items
    try:
        action_items_prompt = f"""Extract action items from this meeting transcript.
For each action item include: task, owner, deadline, priority.

Transcript: {transcript}

Return JSON: {{"action_items": [...]}}
"""
        response = retry_llm_call(action_items_prompt)
        action_items_data = json.loads(response)
        insights['action_items'] = action_items_data.get('action_items', [])
    except Exception as e:
        errors['action_items'] = str(e)
        insights['action_items'] = None

    # Extract key topics
    try:
        topics_prompt = f"""What were the main topics discussed in this meeting?

Transcript: {transcript}

Return JSON with: {{"key_topics": [...], "primary_focus": "..."}}
"""
        response = retry_llm_call(topics_prompt)
        topics_data = json.loads(response)
        insights['topics'] = topics_data
    except Exception as e:
        errors['topics'] = str(e)
        insights['topics'] = None

    # Analyze sentiment
    try:
        sentiment_prompt = f"""Analyze the sentiment and relationship health from this meeting.

Transcript: {transcript}

Return JSON: {{"sentiment": {{"score": 0.0-1.0, "summary": "...", "relationship_health": "strong/stable/at_risk"}}}}
"""
        response = retry_llm_call(sentiment_prompt)
        sentiment_data = json.loads(response)
        insights['sentiment'] = sentiment_data.get('sentiment')
    except Exception as e:
        errors['sentiment'] = str(e)
        insights['sentiment'] = None

    # Save insights to meeting
    data.update_meeting(meeting_id, {
        "transcript": transcript,
        "insights": insights,
        "analyzed_at": datetime.utcnow().isoformat()
    })

    response_data = {
        "meeting_id": meeting_id,
        "insights": insights
    }

    # Include errors if any extractors failed
    if errors:
        response_data['errors'] = errors
        response_data['message'] = "Some insights failed to extract"

    return jsonify(response_data), 200


# ============================================================================
# Utility
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/', methods=['GET'])
def home():
    """API info"""
    return jsonify({
        "name": "Meeting Intelligence API",
        "endpoints": {
            "POST /meetings": "Create a new meeting",
            "GET /meetings/<id>": "Get meeting details",
            "POST /meetings/<id>/prepare": "Get pre-meeting preparation",
            "POST /meetings/<id>/analyze": "Analyze meeting transcript",
            "GET /health": "Health check"
        }
    }), 200


# ============================================================================
# Run
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Meeting Intelligence API - Sample Solution")
    print("=" * 60)
    print("Server running on http://localhost:5000")
    print()
    print("Endpoints:")
    print("  POST /meetings              - Create meeting")
    print("  GET  /meetings/<id>         - Get meeting")
    print("  POST /meetings/<id>/prepare - Pre-meeting prep")
    print("  POST /meetings/<id>/analyze - Analyze transcript")
    print("=" * 60)

    app.run(debug=True, port=5000)

"""
Meeting Intelligence API

Implement the REST API endpoints for the meeting intelligence platform.
See problem.md for business requirements.
"""

from flask import Flask, request, jsonify
from datetime import datetime

# Import the mock database and LLM client
import data
from llm_client import MockLLMClient, LLMAPIError

app = Flask(__name__)

# Initialize the LLM client
llm_client = MockLLMClient()


# ============================================================================
# Your endpoints go here
# ============================================================================

@app.route('/meetings', methods=['POST'])
def create_meeting():
    """Create a new meeting"""
    # TODO: Implement this endpoint
    # 1. Validate required fields and check if user/contact exist
    # 2. Generate a meeting_id and create the meeting object
    # 3. Add to database and return success response

    # Error handling:
    # - Return 400 if required fields are missing
    # - Return 404 if user_id or contact_id don't exist
    # - Return 400 for any other validation errors
    pass


# TODO: Implement additional endpoints as needed (e.g., pre-meeting context, post-meeting analysis)



# ============================================================================
# Utility / Health Check
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })


# ============================================================================
# Run the application
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Meeting Intelligence API")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    print()
    print("Read problem.md for requirements")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    app.run(debug=True, port=5000)

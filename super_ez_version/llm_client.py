"""
Mock LLM Client for simulating AI-powered insight generation

In a real application, this would call OpenAI, Anthropic, or another LLM API.
This mock client simulates realistic responses without requiring API keys or costs.

IMPORTANT: This client fails randomly 20% of the time to simulate real-world API failures.
You MUST implement proper error handling and retry logic in your code.

Usage:
    client = MockLLMClient()

    # Will randomly fail ~20% of the time
    try:
        response = client.generate(
            prompt="Extract action items from this transcript: ...",
            system_prompt="You are a helpful meeting assistant"
        )
    except LLMAPIError as e:
        # Handle the error - retry? log? return partial results?
        print(f"LLM call failed: {e}")
"""

import json
import re
import time
import random
from typing import Optional


class LLMAPIError(Exception):
    """Custom exception for LLM API failures"""
    pass


class MockLLMClient:
    """
    Simulates an LLM API client with realistic response patterns

    IMPORTANT: This client randomly fails ~20% of the time to simulate real-world
    API reliability issues. You must implement proper error handling!
    """

    def __init__(self, simulate_latency=False, failure_rate=0.2):
        """
        Initialize the mock client

        Args:
            simulate_latency: If True, adds small delays to simulate network calls
            failure_rate: Probability of API failure (default 0.2 = 20% failure rate)
        """
        self.simulate_latency = simulate_latency
        self.failure_rate = failure_rate

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response based on the prompt

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt (instruction for the LLM)

        Returns:
            JSON-formatted string response

        Raises:
            LLMAPIError: Randomly raised ~20% of the time to simulate API failures
        """
        # Simulate random API failures (20% failure rate)
        if random.random() < self.failure_rate:
            error_types = [
                ("RateLimitError", "Rate limit exceeded. Please retry after a short delay."),
                ("TimeoutError", "Request timed out. The API took too long to respond."),
                ("ServiceUnavailableError", "Service temporarily unavailable. Please retry."),
                ("InvalidRequestError", "Invalid request format or parameters."),
            ]
            error_type, error_message = random.choice(error_types)
            raise LLMAPIError(f"{error_type}: {error_message}")

        # Simulate API latency
        if self.simulate_latency:
            time.sleep(0.5)

        # Analyze prompt to determine what type of response to generate
        prompt_lower = prompt.lower()

        # Pre-meeting context generation
        if "prepare" in prompt_lower or "context" in prompt_lower or "upcoming meeting" in prompt_lower:
            return self._generate_meeting_context(prompt)

        # Action items extraction
        elif "action item" in prompt_lower or "task" in prompt_lower or "todo" in prompt_lower:
            return self._generate_action_items(prompt)

        # Key topics extraction
        elif "topic" in prompt_lower or "theme" in prompt_lower or "discussed" in prompt_lower:
            return self._generate_key_topics(prompt)

        # Sentiment analysis
        elif "sentiment" in prompt_lower or "tone" in prompt_lower or "relationship" in prompt_lower:
            return self._generate_sentiment(prompt)

        # Follow-up recommendations
        elif "follow" in prompt_lower or "next step" in prompt_lower or "recommendation" in prompt_lower:
            return self._generate_follow_ups(prompt)

        # Generic response
        else:
            return json.dumps({
                "response": "I've analyzed the content and generated insights.",
                "note": "This is a generic mock response"
            })

    def _generate_meeting_context(self, prompt: str) -> str:
        """Generate pre-meeting context"""
        # Extract contact name if present
        contact_match = re.search(r"contact[:\s]+([A-Z][a-z]+ [A-Z][a-z]+)", prompt)
        contact_name = contact_match.group(1) if contact_match else "the contact"

        context = {
            "contact_summary": f"You have an established relationship with {contact_name}, having met multiple times over the past few months. They are engaged and responsive, showing strong interest in your solution.",
            "recent_interactions": "Your last meeting covered technical requirements and implementation timelines. The contact expressed enthusiasm about key features and mentioned they're in the decision-making phase with executive approval pending.",
            "suggested_topics": [
                "Follow up on action items from last meeting",
                "Discuss implementation timeline and milestones",
                "Address any remaining concerns or blockers",
                "Clarify next steps in the evaluation process"
            ],
            "pending_action_items": [
                "Review provided technical documentation",
                "Schedule meeting with decision makers",
                "Finalize contract terms and pricing"
            ]
        }

        return json.dumps(context, indent=2)

    def _generate_action_items(self, prompt: str) -> str:
        """Generate action items from transcript"""
        # Extract names mentioned in the prompt/transcript
        names = re.findall(r'\b([A-Z][a-z]+)\s*:', prompt)
        owner = names[0] if names else "Team member"

        action_items = [
            {
                "task": "Send follow-up email with discussed materials",
                "owner": owner,
                "deadline": "2025-11-20",
                "priority": "high"
            },
            {
                "task": "Schedule technical review session",
                "owner": owner,
                "deadline": "2025-11-22",
                "priority": "medium"
            },
            {
                "task": "Prepare proposal with updated pricing",
                "owner": owner,
                "deadline": "2025-11-25",
                "priority": "high"
            }
        ]

        return json.dumps({"action_items": action_items}, indent=2)

    def _generate_key_topics(self, prompt: str) -> str:
        """Generate key topics from transcript"""
        # Provide realistic topics based on a business meeting
        topics = [
            "Product capabilities and features",
            "Implementation timeline and resources",
            "Pricing and contract terms",
            "Technical integration requirements",
            "Team training and onboarding",
            "Success metrics and ROI"
        ]

        # Select 3-5 topics
        import random
        random.seed(len(prompt))  # Deterministic based on input
        selected_topics = random.sample(topics, k=min(4, len(topics)))

        return json.dumps({
            "key_topics": selected_topics,
            "primary_focus": selected_topics[0]
        }, indent=2)

    def _generate_sentiment(self, prompt: str) -> str:
        """Generate sentiment analysis"""
        # Analyze for positive/negative keywords
        positive_words = ["great", "excellent", "excited", "interested", "impressed", "perfect"]
        negative_words = ["concern", "worried", "issue", "problem", "disappointed", "confused"]

        prompt_lower = prompt.lower()
        positive_count = sum(1 for word in positive_words if word in prompt_lower)
        negative_count = sum(1 for word in negative_words if word in prompt_lower)

        if positive_count > negative_count:
            score = 0.75
            summary = "Positive and engaged. The conversation was productive with clear interest and forward momentum."
            relationship_health = "strong"
        elif negative_count > positive_count:
            score = 0.45
            summary = "Some concerns raised. Need to address blockers and rebuild confidence."
            relationship_health = "at_risk"
        else:
            score = 0.6
            summary = "Neutral and professional. Standard business discussion with no major issues."
            relationship_health = "stable"

        return json.dumps({
            "sentiment": {
                "score": score,
                "summary": summary,
                "relationship_health": relationship_health
            }
        }, indent=2)

    def _generate_follow_ups(self, prompt: str) -> str:
        """Generate follow-up recommendations"""
        follow_ups = [
            "Send meeting summary and action items within 24 hours",
            "Schedule follow-up meeting for next week to review progress",
            "Introduce relevant team members for technical discussion",
            "Share case studies and customer success stories",
            "Prepare detailed proposal addressing discussed requirements"
        ]

        # Select 3-4 follow-ups
        import random
        random.seed(len(prompt))  # Deterministic
        selected = random.sample(follow_ups, k=3)

        return json.dumps({"follow_ups": selected}, indent=2)


# Example usage (for testing)
if __name__ == "__main__":
    client = MockLLMClient()

    print("NOTE: The client will fail randomly ~20% of the time!")
    print("Run this multiple times to see failures in action.\n")

    # Test action items extraction with error handling
    print("=== Testing Action Items Extraction ===")
    try:
        result = client.generate(
            prompt="Extract action items from this transcript: Sarah said she will send the proposal by Friday. John agreed to review the technical docs and get back to us next week.",
            system_prompt="You are a helpful meeting assistant."
        )
        print("SUCCESS:", result)
    except LLMAPIError as e:
        print(f"FAILED: {e}")
    print()

    # Test pre-meeting context with error handling
    print("=== Testing Pre-Meeting Context ===")
    try:
        result = client.generate(
            prompt="Generate context for upcoming meeting with contact: Jennifer Liu. Past meetings discussed product demo and pricing.",
            system_prompt="You are a helpful meeting assistant."
        )
        print("SUCCESS:", result)
    except LLMAPIError as e:
        print(f"FAILED: {e}")
    print()

    # Test sentiment with error handling
    print("=== Testing Sentiment Analysis ===")
    try:
        result = client.generate(
            prompt="Analyze sentiment: The client was excited about the new features and said this looks great. They're ready to move forward.",
            system_prompt="You are a helpful meeting assistant."
        )
        print("SUCCESS:", result)
    except LLMAPIError as e:
        print(f"FAILED: {e}")
    print()

    # Demonstrate retry logic
    print("=== Testing Retry Logic (3 attempts) ===")
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = client.generate(
                prompt="Extract key topics from: We discussed pricing, timeline, and next steps.",
                system_prompt="You are a helpful meeting assistant."
            )
            print(f"SUCCESS on attempt {attempt + 1}:", result)
            break
        except LLMAPIError as e:
            print(f"Attempt {attempt + 1} FAILED: {e}")
            if attempt == max_retries - 1:
                print("All retries exhausted!")
            else:
                time.sleep(0.1)  # Brief delay before retry

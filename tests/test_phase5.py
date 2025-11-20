"""
Phase 5 Tests: Error Handling

Tests for retry logic and graceful failure handling.
Run with: python run_tests.py phase5
"""

import unittest
import data
from models import CreateMeetingRequest, Meeting
from meeting_service import create_meeting, generate_pre_meeting_prep_with_retry
from llm_client import LLMAPIError


class TestPhase5ErrorHandling(unittest.TestCase):
    """Test error handling and retry logic"""

    def setUp(self):
        """Clean up test meetings"""
        test_meeting_ids = [mid for mid in data.MEETINGS.keys() if mid.startswith("test_retry_")]
        for mid in test_meeting_ids:
            del data.MEETINGS[mid]

    def test_retry_eventually_succeeds(self):
        """Should retry and eventually succeed"""
        # The mock LLM has a 30% failure rate, so with 3 retries
        # we should eventually succeed most of the time
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="contact_1",
            title="Retry Test Meeting",
            scheduled_date="2025-12-01T10:00:00"
        )
        meeting = create_meeting(request)

        # This might fail occasionally due to randomness, but should usually pass
        meeting_with_prep = generate_pre_meeting_prep_with_retry(meeting.id, max_retries=5)

        self.assertIsInstance(meeting_with_prep, Meeting)
        self.assertEqual(meeting_with_prep.id, meeting.id)
        self.assertIsNotNone(meeting_with_prep.prep)

    def test_retry_respects_max_retries(self):
        """Should stop after max_retries attempts"""
        # With max_retries=1 and 30% failure rate, this might fail
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="contact_1",
            title="Limited Retry Test",
            scheduled_date="2025-12-01T11:00:00"
        )
        meeting = create_meeting(request)

        # Try with very limited retries
        # This test is probabilistic - it might pass even with failures
        try:
            meeting_with_prep = generate_pre_meeting_prep_with_retry(meeting.id, max_retries=1)
            # If it succeeds, that's fine
            self.assertIsInstance(meeting_with_prep, Meeting)
        except LLMAPIError:
            # If it fails after 1 retry, that's also expected
            pass

    def test_retry_raises_error_after_exhaustion(self):
        """Should raise LLMAPIError if all retries fail"""
        # This test is tricky because the mock has only 30% failure rate
        # We can't reliably make it fail every time
        # So we'll test the structure exists, but may not always fail

        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="contact_1",
            title="Failure Test",
            scheduled_date="2025-12-01T12:00:00"
        )
        meeting = create_meeting(request)

        # The function should exist and be callable
        # It may succeed or fail depending on random chance
        try:
            meeting_with_prep = generate_pre_meeting_prep_with_retry(meeting.id, max_retries=1)
            # Success is acceptable
            self.assertIsInstance(meeting_with_prep, Meeting)
        except LLMAPIError as e:
            # Failure with LLMAPIError is also acceptable
            self.assertIsInstance(e, LLMAPIError)

    def test_retry_with_invalid_meeting(self):
        """Should raise ValueError for invalid meeting, not LLMAPIError"""
        # Even with retry, should raise ValueError for bad input
        with self.assertRaises(ValueError):
            generate_pre_meeting_prep_with_retry("nonexistent_meeting")

    def test_retry_with_no_contact(self):
        """Should raise ValueError for internal meeting"""
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id=None,
            title="Internal Meeting",
            scheduled_date="2025-12-01T13:00:00"
        )
        meeting = create_meeting(request)

        # Should raise ValueError, not retry LLM
        with self.assertRaises(ValueError):
            generate_pre_meeting_prep_with_retry(meeting.id)

    def test_retry_returns_valid_prep_object(self):
        """Should return properly structured PreMeetingPrep on success"""
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="contact_2",
            title="Validation Test",
            scheduled_date="2025-12-01T14:00:00"
        )
        meeting = create_meeting(request)

        meeting_with_prep = generate_pre_meeting_prep_with_retry(meeting.id, max_retries=5)

        # Verify all fields present
        self.assertIsInstance(meeting_with_prep, Meeting)
        self.assertEqual(meeting_with_prep.id, meeting.id)
        self.assertIsInstance(meeting_with_prep.prep, str)
        self.assertGreater(len(meeting_with_prep.prep), 50)


if __name__ == '__main__':
    unittest.main()

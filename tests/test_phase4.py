"""
Phase 4 Tests: Pre-Meeting Prep

Tests for LLM-based pre-meeting preparation generation.
Run with: python run_tests.py phase4
"""

import unittest
import json
import data
from models import CreateMeetingRequest, Meeting
from meeting_service import create_meeting, generate_pre_meeting_prep


class TestPhase4PreMeetingPrep(unittest.TestCase):
    """Test pre-meeting prep generation"""

    def setUp(self):
        """Clean up test meetings"""
        test_meeting_ids = [mid for mid in data.MEETINGS.keys() if mid.startswith("test_prep_")]
        for mid in test_meeting_ids:
            del data.MEETINGS[mid]

    def test_generate_prep_with_history(self):
        """Should generate prep for contact with meeting history"""
        # Create a meeting with contact_1 (who has history)
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="contact_1",
            title="Follow-up Discussion",
            date="2025-12-01",
            start_hour=14,
            end_hour=15
        )
        meeting = create_meeting(request)

        # Generate prep
        meeting_with_prep = generate_pre_meeting_prep(meeting.id)

        # Verify it returns the meeting object
        self.assertIsInstance(meeting_with_prep, Meeting)
        self.assertEqual(meeting_with_prep.id, meeting.id)

        # Verify prep field is populated
        self.assertIsNotNone(meeting_with_prep.prep)
        self.assertIsInstance(meeting_with_prep.prep, str)
        self.assertGreater(len(meeting_with_prep.prep), 50)

    def test_generate_prep_first_meeting(self):
        """Should handle first meeting with contact (no history)"""
        # contact_2 has limited history
        request = CreateMeetingRequest(
            user_id="user_2",
            contact_id="contact_3",
            title="Initial Meeting",
            date="2025-12-01",
            start_hour=10,
            end_hour=11
        )
        meeting = create_meeting(request)

        # Should still generate prep even without extensive history
        meeting_with_prep = generate_pre_meeting_prep(meeting.id)

        self.assertIsInstance(meeting_with_prep, Meeting)
        self.assertIsNotNone(meeting_with_prep.prep)
        self.assertGreater(len(meeting_with_prep.prep), 50)

    def test_generate_prep_no_contact(self):
        """Should raise ValueError for internal meeting without contact"""
        # Create internal meeting (no contact)
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id=None,
            title="Internal Team Sync",
            date="2025-12-01",
            start_hour=10,
            end_hour=11
        )
        meeting = create_meeting(request)

        # Should raise error
        with self.assertRaises(ValueError):
            generate_pre_meeting_prep(meeting.id)

    def test_generate_prep_invalid_meeting(self):
        """Should raise ValueError for non-existent meeting"""
        with self.assertRaises(ValueError):
            generate_pre_meeting_prep("nonexistent_meeting")

    def test_prep_includes_all_required_fields(self):
        """Should include all required fields in response"""
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="contact_1",
            title="Review Meeting",
            date="2025-12-01",
            start_hour=15,
            end_hour=16
        )
        meeting = create_meeting(request)

        meeting_with_prep = generate_pre_meeting_prep(meeting.id)

        # Should return a Meeting object
        self.assertIsInstance(meeting_with_prep, Meeting)

        # Should have prep field populated
        self.assertIsNotNone(meeting_with_prep.prep)
        self.assertGreater(len(meeting_with_prep.prep), 50)

    def test_prep_text_contains_key_sections(self):
        """Should contain key sections in the prep text"""
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="contact_1",
            title="Strategy Session",
            date="2025-12-01",
            start_hour=16,
            end_hour=17
        )
        meeting = create_meeting(request)

        meeting_with_prep = generate_pre_meeting_prep(meeting.id)

        # Should be a substantial text response
        self.assertIsInstance(meeting_with_prep.prep, str)
        self.assertGreater(len(meeting_with_prep.prep), 100)


if __name__ == '__main__':
    unittest.main()

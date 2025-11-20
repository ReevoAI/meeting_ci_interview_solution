"""
Phase 1 Tests: Pydantic Models

Tests for data model definitions and validation.
Run with: python run_tests.py phase1
"""

import unittest
from models import User, Contact, Meeting, CreateMeetingRequest, TimeSlot, PreMeetingPrep


class TestPhase1Models(unittest.TestCase):
    """Test Pydantic model creation and validation"""

    def test_user_model_creation(self):
        """Should create user with all required fields"""
        user = User(
            id="user_1",
            name="John Doe",
            email="john@example.com",
            role="Engineer"
        )
        self.assertEqual(user.id, "user_1")
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(user.role, "Engineer")

    def test_contact_model_creation(self):
        """Should create contact with all required fields"""
        contact = Contact(
            id="contact_1",
            name="Jane Smith",
            email="jane@company.com",
            company="Acme Corp",
            role="CTO"
        )
        self.assertEqual(contact.id, "contact_1")
        self.assertEqual(contact.company, "Acme Corp")

    def test_meeting_model_creation(self):
        """Should create meeting with required fields"""
        meeting = Meeting(
            id="meeting_1",
            user_id="user_1",
            contact_id="contact_1",
            title="Kickoff Meeting",
            scheduled_date="2025-11-20T14:00:00"
        )
        self.assertEqual(meeting.id, "meeting_1")
        self.assertEqual(meeting.title, "Kickoff Meeting")

    def test_meeting_optional_contact(self):
        """Should allow meeting without contact (internal meeting)"""
        meeting = Meeting(
            id="meeting_1",
            user_id="user_1",
            contact_id=None,
            title="Team Sync",
            scheduled_date="2025-11-20T14:00:00"
        )
        self.assertIsNone(meeting.contact_id)

    def test_create_meeting_request(self):
        """Should create meeting request"""
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="contact_1",
            title="Demo",
            scheduled_date="2025-11-20T15:00:00"
        )
        self.assertEqual(request.user_id, "user_1")
        self.assertEqual(request.title, "Demo")

    def test_timeslot_model(self):
        """Should create timeslot"""
        slot = TimeSlot(
            start_time="2025-11-20T10:00:00",
            end_time="2025-11-20T11:00:00"
        )
        self.assertEqual(slot.start_time, "2025-11-20T10:00:00")
        self.assertEqual(slot.end_time, "2025-11-20T11:00:00")

    def test_pre_meeting_prep_model(self):
        """Should create pre-meeting prep"""
        prep = PreMeetingPrep(
            meeting_id="meeting_1",
            prep_text="This is a comprehensive meeting preparation with all necessary details."
        )
        self.assertEqual(prep.meeting_id, "meeting_1")
        self.assertGreater(len(prep.prep_text), 20)

    def test_meeting_action_items_default(self):
        """Should default action_items to empty list, not None"""
        meeting = Meeting(
            id="meeting_2",
            user_id="user_1",
            title="Planning Session",
            scheduled_date="2025-11-21T10:00:00"
        )
        self.assertIsNotNone(meeting.action_items)
        self.assertIsInstance(meeting.action_items, list)
        self.assertEqual(len(meeting.action_items), 0)

    def test_meeting_with_all_optional_fields(self):
        """Should accept all optional fields when provided"""
        meeting = Meeting(
            id="meeting_3",
            user_id="user_1",
            contact_id="contact_1",
            title="Complete Meeting",
            scheduled_date="2025-11-22T14:00:00",
            created_at="2025-11-01T08:00:00",
            transcript="Sarah: Hello... John: Hi...",
            summary="We discussed the project timeline and deliverables.",
            action_items=["Send proposal", "Schedule followup"],
            sentiment="positive"
        )
        self.assertEqual(meeting.transcript, "Sarah: Hello... John: Hi...")
        self.assertEqual(meeting.summary, "We discussed the project timeline and deliverables.")
        self.assertEqual(len(meeting.action_items), 2)
        self.assertEqual(meeting.sentiment, "positive")

    def test_meeting_optional_fields_can_be_omitted(self):
        """Should allow optional fields to be omitted"""
        meeting = Meeting(
            id="meeting_4",
            user_id="user_2",
            title="Brief Sync",
            scheduled_date="2025-11-23T09:00:00"
        )
        # These should be None or default values
        self.assertIsNone(meeting.contact_id)
        self.assertIsNone(meeting.created_at)
        self.assertIsNone(meeting.transcript)
        self.assertIsNone(meeting.summary)
        self.assertIsNone(meeting.sentiment)
        self.assertEqual(meeting.action_items, [])  # Should be empty list, not None

    def test_create_meeting_request_without_contact(self):
        """Should allow creating internal meeting request without contact"""
        request = CreateMeetingRequest(
            user_id="user_1",
            title="Team Meeting",
            scheduled_date="2025-11-24T15:00:00"
        )
        self.assertIsNone(request.contact_id)
        self.assertEqual(request.title, "Team Meeting")


if __name__ == '__main__':
    unittest.main()

"""
Phase 2 Tests: CRUD Operations

Tests for basic Create, Read, Update, Delete operations.
Run with: python run_tests.py phase2
"""

import unittest
import data
from models import CreateMeetingRequest, Meeting
from meeting_service import (
    get_all_meetings,
    get_meeting,
    create_meeting,
    update_meeting,
    delete_meeting
)


class TestPhase2CRUD(unittest.TestCase):
    """Test CRUD operations on meetings"""

    def setUp(self):
        """Reset meetings before each test"""
        # Keep only the historical meetings, remove any test meetings
        test_meeting_ids = [mid for mid in data.MEETINGS.keys() if mid.startswith("test_")]
        for mid in test_meeting_ids:
            del data.MEETINGS[mid]

    def test_get_all_meetings_for_user(self):
        """Should return all meetings for a user"""
        meetings = get_all_meetings("user_1")
        self.assertIsInstance(meetings, list)
        self.assertGreater(len(meetings), 0)
        # All meetings should be for user_1
        for meeting in meetings:
            self.assertEqual(meeting.user_id, "user_1")

    def test_get_all_meetings_with_contact_filter(self):
        """Should filter meetings by contact"""
        meetings = get_all_meetings("user_1", filters={"contact_id": "contact_1"})
        self.assertGreater(len(meetings), 0)
        for meeting in meetings:
            self.assertEqual(meeting.contact_id, "contact_1")

    def test_get_all_meetings_invalid_user(self):
        """Should raise ValueError for invalid user"""
        with self.assertRaises(ValueError):
            get_all_meetings("invalid_user")

    def test_get_meeting_by_id(self):
        """Should retrieve specific meeting"""
        meeting = get_meeting("hist_meeting_1")
        self.assertIsInstance(meeting, Meeting)
        self.assertEqual(meeting.id, "hist_meeting_1")

    def test_get_meeting_not_found(self):
        """Should raise ValueError for non-existent meeting"""
        with self.assertRaises(ValueError):
            get_meeting("nonexistent_meeting")

    def test_create_meeting_success(self):
        """Should create a new meeting"""
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="contact_1",
            title="Test Meeting",
            scheduled_date="2025-11-25T10:00:00"
        )
        meeting = create_meeting(request)

        self.assertIsInstance(meeting, Meeting)
        self.assertEqual(meeting.user_id, "user_1")
        self.assertEqual(meeting.title, "Test Meeting")
        self.assertIsNotNone(meeting.id)

        # Verify it was added to database
        self.assertTrue(data.meeting_exists(meeting.id))

    def test_create_meeting_invalid_user(self):
        """Should raise ValueError for invalid user"""
        request = CreateMeetingRequest(
            user_id="invalid_user",
            contact_id="contact_1",
            title="Test Meeting",
            scheduled_date="2025-11-25T10:00:00"
        )
        with self.assertRaises(ValueError):
            create_meeting(request)

    def test_create_meeting_invalid_contact(self):
        """Should raise ValueError for invalid contact"""
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="invalid_contact",
            title="Test Meeting",
            scheduled_date="2025-11-25T10:00:00"
        )
        with self.assertRaises(ValueError):
            create_meeting(request)

    def test_create_meeting_no_contact(self):
        """Should allow creating internal meeting without contact"""
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id=None,
            title="Internal Team Sync",
            scheduled_date="2025-11-25T10:00:00"
        )
        meeting = create_meeting(request)

        self.assertIsNone(meeting.contact_id)
        self.assertEqual(meeting.title, "Internal Team Sync")

    def test_update_meeting_title(self):
        """Should update meeting fields"""
        # First create a meeting
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="contact_1",
            title="Original Title",
            scheduled_date="2025-11-25T10:00:00"
        )
        meeting = create_meeting(request)

        # Update it
        updated = update_meeting(meeting.id, {"title": "Updated Title"})

        self.assertEqual(updated.title, "Updated Title")
        self.assertEqual(updated.id, meeting.id)

    def test_update_meeting_multiple_fields(self):
        """Should update multiple fields at once"""
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="contact_1",
            title="Original",
            scheduled_date="2025-11-25T10:00:00"
        )
        meeting = create_meeting(request)

        updated = update_meeting(meeting.id, {
            "title": "New Title",
            "transcript": "Meeting transcript here"
        })

        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.transcript, "Meeting transcript here")

    def test_update_meeting_not_found(self):
        """Should raise ValueError for non-existent meeting"""
        with self.assertRaises(ValueError):
            update_meeting("nonexistent", {"title": "New"})

    def test_delete_meeting_success(self):
        """Should delete a meeting"""
        # Create a meeting
        request = CreateMeetingRequest(
            user_id="user_1",
            contact_id="contact_1",
            title="To Be Deleted",
            scheduled_date="2025-11-25T10:00:00"
        )
        meeting = create_meeting(request)

        # Delete it
        result = delete_meeting(meeting.id)

        self.assertTrue(result)
        self.assertFalse(data.meeting_exists(meeting.id))

    def test_delete_meeting_not_found(self):
        """Should raise ValueError for non-existent meeting"""
        with self.assertRaises(ValueError):
            delete_meeting("nonexistent")


if __name__ == '__main__':
    unittest.main()

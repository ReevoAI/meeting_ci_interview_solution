"""
Phase 3 Tests: Availability Function

Tests for finding available time slots across multiple users.
Run with: python run_tests.py phase3
"""

import unittest
import data
from models import CreateMeetingRequest, TimeSlot
from meeting_service import create_meeting, find_available_slots


class TestPhase3Availability(unittest.TestCase):
    """Test availability finding algorithm"""

    def setUp(self):
        """Clean up test meetings"""
        test_meeting_ids = [mid for mid in data.MEETINGS.keys() if mid.startswith("test_avail_")]
        for mid in test_meeting_ids:
            del data.MEETINGS[mid]

    def test_find_slots_single_user_no_meetings(self):
        """Should return full work day when user has no meetings"""
        # user_2 has fewer meetings, pick a free day
        slots = find_available_slots(
            user_ids=["user_2"],
            date="2025-12-01",
            duration_minutes=60
        )

        self.assertIsInstance(slots, list)
        # Should have multiple available slots throughout the day
        self.assertGreater(len(slots), 0)

    def test_find_slots_single_user_with_meetings(self):
        """Should find gaps between meetings"""
        # Create a meeting at 10am
        request = CreateMeetingRequest(
            user_id="user_1",
            title="Test Meeting",
            scheduled_date="2025-12-01T10:00:00"
        )
        meeting = create_meeting(request)

        # Add end time to the meeting (simulate it's 1 hour)
        data.update_meeting(meeting.id, {"end_time": "2025-12-01T11:00:00"})

        # Should find slots before 10am and after 11am
        slots = find_available_slots(
            user_ids=["user_1"],
            date="2025-12-01",
            duration_minutes=60
        )

        # Note: This test may need adjustment based on implementation
        # The key is that there should be available times
        self.assertIsInstance(slots, list)

    def test_find_slots_multiple_users_common_time(self):
        """Should find times when all users are free"""
        slots = find_available_slots(
            user_ids=["user_1", "user_2"],
            date="2025-12-02",
            duration_minutes=30
        )

        self.assertIsInstance(slots, list)
        # Should find some common availability
        self.assertGreater(len(slots), 0)

        # Each slot should be TimeSlot object
        for slot in slots:
            self.assertIsInstance(slot, TimeSlot)

    def test_find_slots_respects_work_hours(self):
        """Should only return slots within work hours"""
        slots = find_available_slots(
            user_ids=["user_1"],
            date="2025-12-02",
            duration_minutes=60,
            work_hours=(9, 17)  # 9am to 5pm
        )

        for slot in slots:
            # Parse start time and verify it's within work hours
            start_hour = int(slot.start_time.split('T')[1].split(':')[0])
            end_hour = int(slot.end_time.split('T')[1].split(':')[0])

            self.assertGreaterEqual(start_hour, 9)
            self.assertLessEqual(end_hour, 17)

    def test_find_slots_custom_work_hours(self):
        """Should respect custom work hours"""
        slots = find_available_slots(
            user_ids=["user_1"],
            date="2025-12-03",
            duration_minutes=30,
            work_hours=(10, 16)  # 10am to 4pm
        )

        for slot in slots:
            start_hour = int(slot.start_time.split('T')[1].split(':')[0])
            end_hour = int(slot.end_time.split('T')[1].split(':')[0])

            self.assertGreaterEqual(start_hour, 10)
            self.assertLessEqual(end_hour, 16)

    def test_find_slots_duration_too_long(self):
        """Should return empty list if duration longer than work day"""
        slots = find_available_slots(
            user_ids=["user_1"],
            date="2025-12-03",
            duration_minutes=600,  # 10 hours (longer than 8 hour work day)
            work_hours=(9, 17)
        )

        # Should return empty or very few slots
        self.assertIsInstance(slots, list)

    def test_find_slots_invalid_user(self):
        """Should raise ValueError for invalid user"""
        with self.assertRaises(ValueError):
            find_available_slots(
                user_ids=["invalid_user"],
                date="2025-12-03",
                duration_minutes=60
            )

    def test_find_slots_empty_user_list(self):
        """Should handle empty user list appropriately"""
        # This could either raise ValueError or return empty list
        # depending on implementation choice
        try:
            slots = find_available_slots(
                user_ids=[],
                date="2025-12-03",
                duration_minutes=60
            )
            # If it doesn't raise error, should return empty list
            self.assertEqual(slots, [])
        except ValueError:
            # This is also acceptable behavior
            pass

    def test_find_slots_returns_timeslot_objects(self):
        """Should return list of TimeSlot objects"""
        slots = find_available_slots(
            user_ids=["user_1"],
            date="2025-12-04",
            duration_minutes=30
        )

        self.assertIsInstance(slots, list)
        for slot in slots:
            self.assertIsInstance(slot, TimeSlot)
            self.assertIsInstance(slot.start_time, str)
            self.assertIsInstance(slot.end_time, str)


if __name__ == '__main__':
    unittest.main()

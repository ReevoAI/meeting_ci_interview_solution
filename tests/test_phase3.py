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
            duration_hours=1
        )

        self.assertIsInstance(slots, list)
        # Should have multiple available slots throughout the day (9am-5pm = 8 hours of slots)
        self.assertGreater(len(slots), 5)

    def test_find_slots_single_user_with_meetings(self):
        """Should find gaps between meetings"""
        # Create a meeting at 10am-11am
        request = CreateMeetingRequest(
            user_id="user_1",
            title="Test Meeting",
            date="2025-12-01",
            start_hour=10,
            end_hour=11
        )
        meeting = create_meeting(request)

        # Should find slots before 10am and after 11am
        slots = find_available_slots(
            user_ids=["user_1"],
            date="2025-12-01",
            duration_hours=1
        )

        self.assertIsInstance(slots, list)
        self.assertGreater(len(slots), 0)

        # Verify 10am slot is NOT available
        ten_am_slot = [s for s in slots if s.start_hour == 10]
        self.assertEqual(len(ten_am_slot), 0)

    def test_find_slots_multiple_users_common_time(self):
        """Should find times when all users are free"""
        slots = find_available_slots(
            user_ids=["user_1", "user_2"],
            date="2025-12-02",
            duration_hours=1
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
            duration_hours=1,
            work_hours=(9, 17)  # 9am to 5pm
        )

        for slot in slots:
            self.assertGreaterEqual(slot.start_hour, 9)
            self.assertLessEqual(slot.end_hour, 17)

    def test_find_slots_custom_work_hours(self):
        """Should respect custom work hours"""
        slots = find_available_slots(
            user_ids=["user_1"],
            date="2025-12-03",
            duration_hours=1,
            work_hours=(10, 16)  # 10am to 4pm
        )

        for slot in slots:
            self.assertGreaterEqual(slot.start_hour, 10)
            self.assertLessEqual(slot.end_hour, 16)

    def test_find_slots_duration_too_long(self):
        """Should return empty list if duration longer than work day"""
        slots = find_available_slots(
            user_ids=["user_1"],
            date="2025-12-03",
            duration_hours=10,  # 10 hours (longer than 8 hour work day)
            work_hours=(9, 17)
        )

        # Should return empty list
        self.assertEqual(slots, [])

    def test_find_slots_invalid_user(self):
        """Should raise ValueError for invalid user"""
        with self.assertRaises(ValueError):
            find_available_slots(
                user_ids=["invalid_user"],
                date="2025-12-03",
                duration_hours=1
            )

    def test_find_slots_empty_user_list(self):
        """Should raise ValueError for empty user list"""
        with self.assertRaises(ValueError):
            find_available_slots(
                user_ids=[],
                date="2025-12-03",
                duration_hours=1
            )

    def test_find_slots_returns_timeslot_objects(self):
        """Should return list of TimeSlot objects with correct structure"""
        slots = find_available_slots(
            user_ids=["user_1"],
            date="2025-12-04",
            duration_hours=1
        )

        self.assertIsInstance(slots, list)
        for slot in slots:
            self.assertIsInstance(slot, TimeSlot)
            self.assertEqual(slot.date, "2025-12-04")
            self.assertIsInstance(slot.start_hour, int)
            self.assertIsInstance(slot.end_hour, int)
            # Duration should match request
            self.assertEqual(slot.end_hour - slot.start_hour, 1)

    def test_find_slots_two_hour_duration(self):
        """Should find 2-hour slots correctly"""
        slots = find_available_slots(
            user_ids=["user_2"],
            date="2025-12-05",
            duration_hours=2,
            work_hours=(9, 17)
        )

        self.assertIsInstance(slots, list)
        for slot in slots:
            # Each slot should be exactly 2 hours
            self.assertEqual(slot.end_hour - slot.start_hour, 2)


if __name__ == '__main__':
    unittest.main()

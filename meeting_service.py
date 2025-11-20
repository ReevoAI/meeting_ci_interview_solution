"""
Meeting Intelligence Service Layer - SOLUTION

Fully implemented solution for all phases.
"""

import data
from models import Meeting, User, Contact, CreateMeetingRequest, TimeSlot, PreMeetingPrep
from llm_client import MockLLMClient, LLMAPIError
from typing import List, Optional
from datetime import datetime, timedelta
import time
import uuid
import json

llm = MockLLMClient(failure_rate=0.0)


# ============================================================================
# PHASE 2: CRUD Operations
# ============================================================================

def get_all_meetings(user_id: str, filters: Optional[dict] = None) -> List[Meeting]:
    """
    Get all meetings for a user with optional filtering.
    """
    # Validate user exists
    if not data.user_exists(user_id):
        raise ValueError(f"User {user_id} not found")

    # Get all meetings for user
    meetings = [
        meeting for meeting in data.MEETINGS.values()
        if meeting["user_id"] == user_id
    ]

    # Apply filters if provided
    if filters:
        if "contact_id" in filters:
            meetings = [m for m in meetings if m.get("contact_id") == filters["contact_id"]]

        if "date_from" in filters:
            meetings = [m for m in meetings if m.get("scheduled_date", m.get("date", "")) >= filters["date_from"]]

        if "date_to" in filters:
            meetings = [m for m in meetings if m.get("scheduled_date", m.get("date", "")) <= filters["date_to"]]

    # Sort by date (most recent first)
    meetings.sort(key=lambda x: x.get("scheduled_date", x.get("date", "")), reverse=True)

    # Convert to Meeting objects
    return [Meeting(**meeting) for meeting in meetings]


def get_meeting(meeting_id: str) -> Meeting:
    """
    Get a specific meeting by ID.
    """
    meeting = data.get_meeting(meeting_id)
    if not meeting:
        raise ValueError(f"Meeting {meeting_id} not found")

    return meeting


def create_meeting(meeting_request: CreateMeetingRequest) -> Meeting:
    """
    Create a new meeting.
    """
    # Validate user exists
    if not data.user_exists(meeting_request.user_id):
        raise ValueError(f"User {meeting_request.user_id} not found")

    # Validate contact exists (if provided)
    if meeting_request.contact_id and not data.contact_exists(meeting_request.contact_id):
        raise ValueError(f"Contact {meeting_request.contact_id} not found")

    # Generate unique meeting ID
    meeting_id = f"meeting_{uuid.uuid4().hex[:8]}"

    # Create Meeting object
    meeting = Meeting(
        id=meeting_id,
        user_id=meeting_request.user_id,
        contact_id=meeting_request.contact_id,
        title=meeting_request.title,
        scheduled_date=meeting_request.scheduled_date,
        created_at=datetime.utcnow().isoformat()
    )

    # Add to database (data.py handles Pydantic models)
    data.add_meeting(meeting)

    return meeting


def update_meeting(meeting_id: str, updates: dict) -> Meeting:
    """
    Update a meeting with new data.
    """
    if not data.meeting_exists(meeting_id):
        raise ValueError(f"Meeting {meeting_id} not found")

    # Don't allow updating ID
    if "id" in updates:
        del updates["id"]

    # Update in database
    updated_meeting = data.update_meeting(meeting_id, updates)

    if not updated_meeting:
        raise ValueError(f"Meeting {meeting_id} not found")

    return updated_meeting


def delete_meeting(meeting_id: str) -> bool:
    """
    Delete a meeting.
    """
    if not data.meeting_exists(meeting_id):
        raise ValueError(f"Meeting {meeting_id} not found")

    # Delete from database
    del data.MEETINGS[meeting_id]
    return True


# ============================================================================
# PHASE 3: Availability Function
# ============================================================================

def find_available_slots(
    user_ids: List[str],
    date: str,
    duration_minutes: int,
    work_hours: tuple = (9, 17)
) -> List[TimeSlot]:
    """
    Find time slots when all users are available.
    """
    # Validate inputs
    if not user_ids:
        raise ValueError("user_ids cannot be empty")

    # Validate all users exist
    for user_id in user_ids:
        if not data.user_exists(user_id):
            raise ValueError(f"User {user_id} not found")

    # Get all meetings for all users on this date
    busy_intervals = []

    for user_id in user_ids:
        user_meetings = [
            m for m in data.MEETINGS.values()
            if m["user_id"] == user_id and m.get("scheduled_date", m.get("date", "")).startswith(date)
        ]

        # Convert meetings to time intervals
        for meeting in user_meetings:
            meeting_date = meeting.get("scheduled_date", meeting.get("date"))
            if meeting_date:
                try:
                    start = datetime.fromisoformat(meeting_date)
                    # Assume 1 hour meeting if no end time specified
                    end = start + timedelta(hours=1)
                    busy_intervals.append((start, end))
                except:
                    pass

    # Merge overlapping intervals
    if not busy_intervals:
        # No meetings, entire work day is free
        work_start = datetime.fromisoformat(f"{date}T{work_hours[0]:02d}:00:00")
        work_end = datetime.fromisoformat(f"{date}T{work_hours[1]:02d}:00:00")

        # Generate slots for the entire work day
        available_slots = []
        current = work_start
        while current + timedelta(minutes=duration_minutes) <= work_end:
            slot_end = current + timedelta(minutes=duration_minutes)
            available_slots.append(TimeSlot(
                start_time=current.isoformat(),
                end_time=slot_end.isoformat()
            ))
            current += timedelta(minutes=30)  # 30 min increments

        return available_slots

    # Sort intervals by start time
    busy_intervals.sort(key=lambda x: x[0])

    # Merge overlapping intervals
    merged = [busy_intervals[0]]
    for start, end in busy_intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            # Overlapping, merge
            merged[-1] = (last_start, max(last_end, end))
        else:
            # Non-overlapping, add new interval
            merged.append((start, end))

    # Find gaps
    work_start = datetime.fromisoformat(f"{date}T{work_hours[0]:02d}:00:00")
    work_end = datetime.fromisoformat(f"{date}T{work_hours[1]:02d}:00:00")

    available_slots = []

    # Check gap before first meeting
    first_meeting_start = merged[0][0]
    if work_start + timedelta(minutes=duration_minutes) <= first_meeting_start:
        # Add slots in this gap
        current = work_start
        while current + timedelta(minutes=duration_minutes) <= first_meeting_start:
            slot_end = current + timedelta(minutes=duration_minutes)
            available_slots.append(TimeSlot(
                start_time=current.isoformat(),
                end_time=slot_end.isoformat()
            ))
            current += timedelta(minutes=30)  # 30 min increments

    # Check gaps between meetings
    for i in range(len(merged) - 1):
        gap_start = merged[i][1]
        gap_end = merged[i + 1][0]

        if gap_end - gap_start >= timedelta(minutes=duration_minutes):
            current = gap_start
            while current + timedelta(minutes=duration_minutes) <= gap_end:
                slot_end = current + timedelta(minutes=duration_minutes)
                if slot_end <= work_end:
                    available_slots.append(TimeSlot(
                        start_time=current.isoformat(),
                        end_time=slot_end.isoformat()
                    ))
                current += timedelta(minutes=30)

    # Check gap after last meeting
    last_meeting_end = merged[-1][1]
    if last_meeting_end < work_end:
        current = last_meeting_end
        while current + timedelta(minutes=duration_minutes) <= work_end:
            slot_end = current + timedelta(minutes=duration_minutes)
            available_slots.append(TimeSlot(
                start_time=current.isoformat(),
                end_time=slot_end.isoformat()
            ))
            current += timedelta(minutes=30)

    # Filter to work hours only
    available_slots = [
        slot for slot in available_slots
        if (datetime.fromisoformat(slot.start_time).hour >= work_hours[0] and
            datetime.fromisoformat(slot.end_time).hour <= work_hours[1])
    ]

    return available_slots


# ============================================================================
# PHASE 4: Pre-Meeting Prep
# ============================================================================

def generate_pre_meeting_prep(meeting_id: str) -> Meeting:
    """
    Generate pre-meeting preparation for external meetings.
    """
    # Get meeting
    meeting = data.get_meeting(meeting_id)
    if not meeting:
        raise ValueError(f"Meeting {meeting_id} not found")

    # Check if meeting has contact (external meeting)
    if not meeting.contact_id:
        raise ValueError("Meeting has no external contact")

    # Get contact details
    contact = data.get_contact(meeting.contact_id)
    if not contact:
        raise ValueError(f"Contact {meeting.contact_id} not found")

    # Get historical meetings with this contact
    past_meetings = data.get_historical_meetings_for_contact(meeting.contact_id, limit=5)

    # Build prompt
    contact_info = f"{contact.name} - {contact.role} at {contact.company}"

    history_str = ""
    if past_meetings:
        history_str = f"\n\nPast meetings ({len(past_meetings)} total):\n"
        for m in past_meetings[:3]:  # Just include last 3
            history_str += f"- {m.scheduled_date}: {m.title}\n"
            if m.summary:
                history_str += f"  Summary: {m.summary}\n"
            if m.action_items:
                history_str += f"  Action items: {', '.join(m.action_items[:2])}\n"
    else:
        history_str = "\n\nThis is your first meeting with this contact."

    prompt = f"""You are helping prepare someone for an upcoming meeting.

Contact Information:
{contact_info}
{history_str}

Please provide a comprehensive meeting preparation including:
1. A brief contact summary (2-3 sentences about who they are and your relationship)
2. Summary of recent interactions (what you've discussed before)
3. 3-5 suggested talking points for the upcoming meeting
4. Any pending action items from past meetings that should be followed up on

Format this as clear, readable text that someone can quickly review before their meeting.
"""

    # Call LLM to get prep text
    prep_text = llm.generate(prompt)

    # Update meeting with prep text
    data.update_meeting(meeting_id, {"prep": prep_text})

    # Return updated meeting
    updated_meeting = data.get_meeting(meeting_id)
    if not updated_meeting:
        raise ValueError(f"Failed to retrieve updated meeting {meeting_id}")

    return updated_meeting


# ============================================================================
# PHASE 5: Error Handling
# ============================================================================

def generate_pre_meeting_prep_with_retry(
    meeting_id: str,
    max_retries: int = 3
) -> Meeting:
    """
    Generate pre-meeting prep with retry logic for LLM failures.
    """
    for attempt in range(max_retries):
        try:
            return generate_pre_meeting_prep(meeting_id)
        except LLMAPIError as e:
            if attempt == max_retries - 1:
                # Last attempt failed, raise error
                raise LLMAPIError(f"Failed to generate prep after {max_retries} attempts: {str(e)}")

            # Calculate exponential backoff
            wait_time = 0.1 * (2 ** attempt)
            time.sleep(wait_time)
        except ValueError as e:
            # Don't retry on ValueError (bad input)
            raise

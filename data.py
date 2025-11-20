"""
Mock database for the Meeting Intelligence API
In a real application, this would be a proper database (PostgreSQL, MongoDB, etc.)
"""

from typing import Optional, List
from models import User, Contact, Meeting

# Users database
USERS = {
    "user_1": {
        "id": "user_1",
        "name": "Sarah Chen",
        "email": "sarah.chen@company.com",
        "role": "Account Executive"
    },
    "user_2": {
        "id": "user_2",
        "name": "Michael Rodriguez",
        "email": "michael.r@company.com",
        "role": "Customer Success Manager"
    }
}

# Contacts database
CONTACTS = {
    "contact_1": {
        "id": "contact_1",
        "name": "Jennifer Liu",
        "email": "jennifer.liu@acmecorp.com",
        "company": "Acme Corp",
        "role": "VP of Engineering"
    },
    "contact_2": {
        "id": "contact_2",
        "name": "David Thompson",
        "email": "david.t@techstartup.io",
        "company": "TechStartup Inc",
        "role": "CTO"
    },
    "contact_3": {
        "id": "contact_3",
        "name": "Amanda Foster",
        "email": "amanda@globalservices.com",
        "company": "Global Services Ltd",
        "role": "Director of Operations"
    }
}

# Meetings database (includes historical and current meetings)
MEETINGS = {
    "hist_meeting_1": {
        "id": "hist_meeting_1",
        "user_id": "user_1",
        "contact_id": "contact_1",
        "title": "Product Demo and Q&A",
        "date": "2025-07-10",
        "start_hour": 14,
        "end_hour": 15,
        "prep": """First meeting with Jennifer Liu (VP Engineering, Acme Corp). Focus: demo automation/API features, understand workflow pain points.""",
        "summary": "Initial product demo with Jennifer. She was impressed with the automation features and asked detailed questions about API integration capabilities. Expressed concern about data security and compliance. She mentioned they're evaluating 3 vendors and will make a decision by end of Q3.",
        "transcript": "Sarah: Thanks for taking the time today Jennifer. Let me walk you through our platform... Jennifer: This automation feature is interesting. How does the API integration work? Sarah: Great question, let me show you... [continues]",
        "action_items": [
            "Sarah to send security compliance documentation",
            "Jennifer to review with engineering team",
            "Schedule technical deep-dive for next week"
        ],
        "sentiment": "positive"
    },
    "hist_meeting_2": {
        "id": "hist_meeting_2",
        "user_id": "user_1",
        "contact_id": "contact_1",
        "title": "Technical Deep Dive",
        "date": "2025-07-18",
        "start_hour": 15,
        "end_hour": 16,
        "prep": """Follow-up with Jennifer. Last meeting positive. Open items: security docs, API deep dive. Address compliance concerns.""",
        "summary": "Technical session with Jennifer and her engineering team. Covered API architecture, data models, and integration patterns. Team was satisfied with technical approach. Jennifer mentioned they're leaning towards our solution but need executive buy-in on pricing.",
        "transcript": "Jennifer: Our engineering team has reviewed the docs. Can you explain the webhook system? Sarah: Absolutely, we use a event-driven architecture... [continues]",
        "action_items": [
            "Sarah to prepare executive summary for Jennifer's VP",
            "Engineering team to start POC next week",
            "Schedule pricing discussion with procurement"
        ],
        "sentiment": "very_positive"
    },
    "hist_meeting_3": {
        "id": "hist_meeting_3",
        "user_id": "user_1",
        "contact_id": "contact_1",
        "title": "Pricing and Contract Discussion",
        "date": "2025-08-05",
        "start_hour": 10,
        "end_hour": 11,
        "prep": """Pricing discussion with Jennifer. Strong relationship, tech team satisfied. Open: exec summary for VP, POC follow-up.""",
        "summary": "Discussed pricing tiers and contract terms. Jennifer mentioned budget constraints for Q3 but has approval for Q4. She wants to move forward with annual contract starting October. Asked about professional services for implementation.",
        "transcript": "Jennifer: We're ready to move forward but need to align on implementation timeline and pricing... Sarah: I can offer professional services support... [continues]",
        "action_items": [
            "Sarah to send revised proposal for Q4 start date",
            "Jennifer to get final approval from CFO",
            "Schedule implementation kickoff for October"
        ],
        "sentiment": "positive"
    },
    "hist_meeting_4": {
        "id": "hist_meeting_4",
        "user_id": "user_2",
        "contact_id": "contact_3",
        "title": "Quarterly Business Review",
        "date": "2025-10-15",
        "start_hour": 11,
        "end_hour": 12,
        "prep": """QBR with Amanda (customer since Jan 2025). Review Q3 metrics, adoption rates, identify friction points.""",
        "summary": "Reviewed Q3 performance metrics with Amanda. Overall positive results but she raised concerns about user adoption in the operations team. Discussed training needs and change management strategy.",
        "transcript": "Michael: Let's review the usage data from last quarter... Amanda: The results are good but I'm concerned about the ops team adoption rate... [continues]",
        "action_items": [
            "Michael to schedule training sessions for ops team",
            "Amanda to identify power users for peer mentoring",
            "Follow-up QBR in 30 days to track improvement"
        ],
        "sentiment": "neutral"
    },
    "hist_meeting_5": {
        "id": "hist_meeting_5",
        "user_id": "user_1",
        "contact_id": "contact_2",
        "title": "Discovery Call",
        "date": "2025-09-15",
        "start_hour": 13,
        "end_hour": 14,
        "prep": """Discovery call with David (CTO, TechStartup). Understand workflow pain points, team needs, evaluation timeline.""",
        "summary": "First meeting with David from TechStartup. They're a fast-growing Series B startup looking for meeting intelligence tools. David is evaluating solutions for his 50-person engineering team. Key pain point is keeping track of customer feedback from product calls.",
        "transcript": "David: We're drowning in meeting notes and customer feedback. How can your platform help? Sarah: We specialize in exactly this problem... [continues]",
        "action_items": [
            "Sarah to send case studies from similar startups",
            "David to share current workflow documentation",
            "Schedule product demo for next week"
        ],
        "sentiment": "positive"
    },
    "hist_meeting_6": {
        "id": "hist_meeting_6",
        "user_id": "user_1",
        "contact_id": "contact_2",
        "title": "Product Demo",
        "date": "2025-09-22",
        "start_hour": 14,
        "end_hour": 15,
        "prep": """Demo for David. Last meeting positive. Focus: customer feedback tracking, API integrations. Tight Q4 deadline.""",
        "summary": "Product demo with David and two of his engineering managers. They were particularly interested in the API and custom integration options. David mentioned they have a tight timeline - need to implement something by end of Q4. Budget is approved.",
        "transcript": "Sarah: Let me show you how the action item extraction works... David: This is great. Can we customize the categories? Sarah: Absolutely, let me show you the configuration options... [continues]",
        "action_items": [
            "Sarah to provide API documentation and integration guide",
            "David to loop in procurement for contract terms",
            "Schedule technical Q&A with engineering team"
        ],
        "sentiment": "very_positive"
    },
    "future_meeting_1": {
        "id": "future_meeting_1",
        "user_id": "user_1",
        "contact_id": "contact_1",
        "title": "Q4 Planning Session",
        "date": "2025-12-15",
        "start_hour": 14,
        "end_hour": 15
    },
    "future_meeting_2": {
        "id": "future_meeting_2",
        "user_id": "user_2",
        "contact_id": "contact_2",
        "title": "Technical Architecture Review",
        "date": "2025-12-20",
        "start_hour": 10,
        "end_hour": 11
    }
}


# Helper functions

def get_user(user_id: str) -> Optional[User]:
    """Get user by ID, returns User model or None"""
    user_data = USERS.get(user_id)
    return User(**user_data) if user_data else None


def get_contact(contact_id: str) -> Optional[Contact]:
    """Get contact by ID, returns Contact model or None"""
    contact_data = CONTACTS.get(contact_id)
    return Contact(**contact_data) if contact_data else None


def get_meeting(meeting_id: str) -> Optional[Meeting]:
    """Get meeting by ID, returns Meeting model or None"""
    meeting_data = MEETINGS.get(meeting_id)
    return Meeting(**meeting_data) if meeting_data else None


def get_historical_meetings_for_contact(contact_id: str, limit: int = 10) -> List[Meeting]:
    """
    Get meetings with a specific contact
    Returns list of Meeting models sorted by date (most recent first)
    """
    meetings = [
        Meeting(**meeting) for meeting in MEETINGS.values()
        if meeting["contact_id"] == contact_id
    ]
    # Sort by date descending (date + start_hour for proper ordering)
    meetings.sort(key=lambda x: (x.date, x.start_hour), reverse=True)
    return meetings[:limit]


def add_meeting(meeting: Meeting) -> str:
    """
    Add a new meeting to the database
    Accepts a Meeting Pydantic model
    Returns the meeting_id
    """
    meeting_dict = meeting.model_dump()
    meeting_id = meeting.id
    MEETINGS[meeting_id] = meeting_dict
    return meeting_id


def update_meeting(meeting_id: str, updates: dict) -> Optional[Meeting]:
    """
    Update a meeting with new data
    Returns updated Meeting model or None if not found
    """
    if meeting_id in MEETINGS:
        MEETINGS[meeting_id].update(updates)
        return Meeting(**MEETINGS[meeting_id])
    return None


def user_exists(user_id: str) -> bool:
    """Check if user exists"""
    return user_id in USERS


def contact_exists(contact_id: str) -> bool:
    """Check if contact exists"""
    return contact_id in CONTACTS


def meeting_exists(meeting_id: str) -> bool:
    """Check if meeting exists"""
    return meeting_id in MEETINGS

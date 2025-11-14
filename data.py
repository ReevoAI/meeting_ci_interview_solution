"""
Mock database for the Meeting Intelligence API
In a real application, this would be a proper database (PostgreSQL, MongoDB, etc.)
"""

# Users database
USERS = {
    "user_1": {
        "id": "user_1",
        "name": "Sarah Chen",
        "email": "sarah.chen@company.com",
        "role": "Account Executive",
        "preferences": {
            "timezone": "America/Los_Angeles",
            "meeting_prep_detail": "high"
        }
    },
    "user_2": {
        "id": "user_2",
        "name": "Michael Rodriguez",
        "email": "michael.r@company.com",
        "role": "Customer Success Manager",
        "preferences": {
            "timezone": "America/New_York",
            "meeting_prep_detail": "medium"
        }
    }
}

# Contacts database
CONTACTS = {
    "contact_1": {
        "id": "contact_1",
        "name": "Jennifer Liu",
        "email": "jennifer.liu@acmecorp.com",
        "company": "Acme Corp",
        "role": "VP of Engineering",
        "relationship_start": "2024-06-15",
        "tags": ["champion", "technical"]
    },
    "contact_2": {
        "id": "contact_2",
        "name": "David Thompson",
        "email": "david.t@techstartup.io",
        "company": "TechStartup Inc",
        "role": "CTO",
        "relationship_start": "2025-09-01",
        "tags": ["decision_maker", "technical", "new_relationship"]
    },
    "contact_3": {
        "id": "contact_3",
        "name": "Amanda Foster",
        "email": "amanda@globalservices.com",
        "company": "Global Services Ltd",
        "role": "Director of Operations",
        "relationship_start": "2025-01-20",
        "tags": ["operations", "stakeholder"]
    }
}

# Historical meetings database
HISTORICAL_MEETINGS = {
    "hist_meeting_1": {
        "id": "hist_meeting_1",
        "user_id": "user_1",
        "contact_id": "contact_1",
        "title": "Product Demo and Q&A",
        "date": "2025-07-10T14:00:00",
        "prep": {
            "contact_summary": "Jennifer Liu is the VP of Engineering at Acme Corp. This is your first meeting with her. She's tagged as a champion and technical buyer. The relationship started in June 2024.",
            "recent_interactions": "No previous meetings on record. This is your initial product demo.",
            "suggested_talking_points": [
                "Understand their current meeting workflow and pain points",
                "Demo automation features and API capabilities",
                "Discuss technical requirements and integration needs",
                "Learn about their evaluation process and timeline"
            ],
            "pending_action_items": []
        },
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
        "date": "2025-07-18T15:00:00",
        "prep": {
            "contact_summary": "Jennifer Liu, VP of Engineering at Acme Corp. You had a successful initial product demo on July 10th. She was impressed with automation features and expressed interest in API integration capabilities. She mentioned concerns about data security and compliance.",
            "recent_interactions": "Last meeting (July 10): Product demo went well. Jennifer asked detailed questions about API integration. She mentioned Acme Corp is evaluating 3 vendors and will decide by end of Q3. Overall sentiment was positive.",
            "suggested_talking_points": [
                "Follow up on security compliance documentation that was promised",
                "Provide technical deep dive on API architecture and webhooks",
                "Address data security and compliance concerns in detail",
                "Discuss integration patterns and technical requirements",
                "Understand timeline for engineering team review"
            ],
            "pending_action_items": [
                "Sarah to send security compliance documentation",
                "Jennifer to review with engineering team",
                "Schedule technical deep-dive for next week"
            ]
        },
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
        "date": "2025-08-05T10:00:00",
        "prep": {
            "contact_summary": "Jennifer Liu, VP of Engineering at Acme Corp. Strong relationship with 2 successful meetings completed. She's championing your solution internally. Technical team is satisfied with the platform and they're leaning toward selecting you over other vendors.",
            "recent_interactions": "July 10: Initial demo - Jennifer impressed with automation and API features. July 18: Technical deep dive - engineering team satisfied with architecture. Sentiment has been very positive. They're in evaluation phase comparing 3 vendors.",
            "suggested_talking_points": [
                "Discuss pricing options and contract terms",
                "Address any questions from the executive summary provided to her VP",
                "Understand budget constraints and approval process",
                "Propose implementation timeline and professional services",
                "Clarify POC results and next steps toward closing"
            ],
            "pending_action_items": [
                "Sarah to prepare executive summary for Jennifer's VP",
                "Engineering team to start POC next week",
                "Schedule pricing discussion with procurement"
            ]
        },
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
        "date": "2025-10-15T11:00:00",
        "prep": {
            "contact_summary": "Amanda Foster is the Director of Operations at Global Services Ltd. She's been a customer since January 2025. Tagged as operations lead and key stakeholder. This is your quarterly business review to assess platform performance and adoption.",
            "recent_interactions": "This is a scheduled QBR. Previous interactions have established a working relationship. Amanda's team has been using the platform for several months. Focus on reviewing metrics and ensuring successful adoption.",
            "suggested_talking_points": [
                "Review Q3 usage metrics and platform adoption rates",
                "Discuss ROI and value delivered to the operations team",
                "Identify any challenges or friction points with the platform",
                "Explore opportunities for increased usage and engagement",
                "Plan for Q4 goals and success metrics"
            ],
            "pending_action_items": []
        },
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
        "date": "2025-09-15T13:00:00",
        "prep": {
            "contact_summary": "David Thompson is the CTO at TechStartup Inc. This is your first meeting with him. He's tagged as a decision maker, technical, and new relationship. TechStartup is a Series B company that started their relationship with you in September 2025.",
            "recent_interactions": "No previous meetings on record. This is your initial discovery call.",
            "suggested_talking_points": [
                "Understand their current meeting workflow and pain points",
                "Learn about their team structure (engineering, product, sales)",
                "Discuss how they currently capture and organize customer feedback",
                "Understand evaluation criteria and timeline",
                "Gauge technical requirements and integration needs",
                "Identify key stakeholders and decision-making process"
            ],
            "pending_action_items": []
        },
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
        "date": "2025-09-22T14:00:00",
        "prep": {
            "contact_summary": "David Thompson, CTO at TechStartup Inc. You had a successful discovery call on September 15th. TechStartup is a fast-growing Series B startup with a 50-person engineering team. Key pain point is tracking customer feedback from product calls.",
            "recent_interactions": "Last meeting (Sept 15): Discovery call went well. David shared that they're drowning in meeting notes and need a solution to organize customer feedback. Sentiment was positive and he's actively evaluating solutions.",
            "suggested_talking_points": [
                "Deliver product demo focused on their customer feedback use case",
                "Show API capabilities and custom integration options",
                "Demo action item extraction and categorization features",
                "Discuss implementation timeline (they need something by end of Q4)",
                "Review case studies from similar startups",
                "Address questions from their current workflow documentation"
            ],
            "pending_action_items": [
                "Sarah to send case studies from similar startups",
                "David to share current workflow documentation",
                "Schedule product demo for next week"
            ]
        },
        "summary": "Product demo with David and two of his engineering managers. They were particularly interested in the API and custom integration options. David mentioned they have a tight timeline - need to implement something by end of Q4. Budget is approved.",
        "transcript": "Sarah: Let me show you how the action item extraction works... David: This is great. Can we customize the categories? Sarah: Absolutely, let me show you the configuration options... [continues]",
        "action_items": [
            "Sarah to provide API documentation and integration guide",
            "David to loop in procurement for contract terms",
            "Schedule technical Q&A with engineering team"
        ],
        "sentiment": "very_positive"
    }
}

# Current meetings database (starts empty, candidates will add to this)
MEETINGS = {}


# Helper functions

def get_user(user_id):
    """Get user by ID"""
    return USERS.get(user_id)


def get_contact(contact_id):
    """Get contact by ID"""
    return CONTACTS.get(contact_id)


def get_meeting(meeting_id):
    """Get meeting by ID"""
    return MEETINGS.get(meeting_id)


def get_historical_meetings_for_contact(contact_id, limit=10):
    """
    Get historical meetings with a specific contact
    Returns list of meetings sorted by date (most recent first)
    """
    meetings = [
        meeting for meeting in HISTORICAL_MEETINGS.values()
        if meeting["contact_id"] == contact_id
    ]
    # Sort by date descending
    meetings.sort(key=lambda x: x["date"], reverse=True)
    return meetings[:limit]


def add_meeting(meeting_data):
    """
    Add a new meeting to the database
    Returns the meeting_id
    """
    meeting_id = meeting_data["id"]
    MEETINGS[meeting_id] = meeting_data
    return meeting_id


def update_meeting(meeting_id, updates):
    """
    Update a meeting with new data
    """
    if meeting_id in MEETINGS:
        MEETINGS[meeting_id].update(updates)
        return True
    return False


def user_exists(user_id):
    """Check if user exists"""
    return user_id in USERS


def contact_exists(contact_id):
    """Check if contact exists"""
    return contact_id in CONTACTS


def meeting_exists(meeting_id):
    """Check if meeting exists"""
    return meeting_id in MEETINGS

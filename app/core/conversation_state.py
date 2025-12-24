from enum import Enum, auto

class ConversationState(Enum):
    """
    Represents the different stages of the chatbot conversation.
    This acts as a finite state machine (FSM) for controlling flow.
    """
    
    GREETING = auto()
    COMPANY_OVERVIEW = auto()
    REQUIREMENT_GATHERING = auto()
    PRODUCT_RECOMMENDATION = auto()
    PRODUCT_EXPLANATION = auto()
    LEAD_CAPTURE = auto()
    HUMAN_HANDOFF = auto()
    END = auto()

class ConversationContext:
    """
    Stores information collected during the conversation.
    Acts as the chatbot's memory.
    """

    def __init__(self):
        self.state = ConversationState.GREETING
        self.business_type = None
        self.team_size = None
        self.needs = []
        self.recommended_products = []
        self.lead_info = {}


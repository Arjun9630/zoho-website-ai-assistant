from app.core.conversation_state import ConversationState, ConversationContext


class ConversationOrchestrator:
    """
    Controls the flow of the chatbot conversation.
    Determines responses and state transitions.
    """

    def __init__(self):
        self.context = ConversationContext()

    def handle_message(self, user_message: str) -> str:
        """
        Main entry point for processing user messages.
        """
        state = self.context.state

        if state == ConversationState.GREETING:
            return self._handle_greeting()

        elif state == ConversationState.COMPANY_OVERVIEW:
            return self._handle_company_overview()

        elif state == ConversationState.REQUIREMENT_GATHERING:
            return self._handle_requirement_gathering(user_message)

        elif state == ConversationState.PRODUCT_RECOMMENDATION:
            return self._handle_product_recommendation()

        elif state == ConversationState.PRODUCT_EXPLANATION:
            return self._handle_product_explanation(user_message)

        elif state == ConversationState.LEAD_CAPTURE:
            return self._handle_lead_capture(user_message)

        elif state == ConversationState.HUMAN_HANDOFF:
            return self._handle_human_handoff()

        else:
            self.context.state = ConversationState.END
            return "Thank you for your time! Have a great day."

    # -------------------------
    # State Handlers
    # -------------------------

    def _handle_greeting(self) -> str:
        self.context.state = ConversationState.COMPANY_OVERVIEW
        return (
            "Hello! 👋 Welcome to Zoho.\n"
            "I can help you understand Zoho’s products and find solutions "
            "that fit your business needs."
        )

    def _handle_company_overview(self) -> str:
        self.context.state = ConversationState.REQUIREMENT_GATHERING
        return (
            "Zoho offers cloud-based software for sales, finance, HR, "
            "customer support, and collaboration.\n\n"
            "To help you better, could you tell me a bit about your business?"
        )

    def _handle_requirement_gathering(self, user_message: str) -> str:
        # Placeholder logic (will be improved later)
        self.context.needs.append(user_message)
        self.context.state = ConversationState.PRODUCT_RECOMMENDATION
        return (
            "Thanks for sharing! Based on what you've told me, "
            "I can recommend some Zoho products for you."
        )

    def _handle_product_recommendation(self) -> str:
        self.context.recommended_products = ["Zoho CRM", "Zoho Desk"]
        self.context.state = ConversationState.LEAD_CAPTURE
        return (
            "I recommend starting with Zoho CRM for sales management "
            "and Zoho Desk for customer support.\n\n"
            "Would you like our onboarding team to contact you for a detailed discussion?"
        )

    def _handle_product_explanation(self, user_message: str) -> str:
        return (
            "This feature is coming soon. "
            "I’ll be happy to explain specific products in detail."
        )

    def _handle_lead_capture(self, user_message: str) -> str:
        self.context.lead_info["response"] = user_message
        self.context.state = ConversationState.HUMAN_HANDOFF
        return (
            "Got it 👍\n"
            "Our onboarding team will reach out to you soon."
        )

    def _handle_human_handoff(self) -> str:
        self.context.state = ConversationState.END
        return (
            "Thank you! A Zoho representative will contact you shortly.\n"
            "Have a great day!"
        )
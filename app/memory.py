class ConversationMemory:
    """
    Session-scoped memory with summarization.
    """

    def __init__(self, system_prompt: str, max_turns: int = 6):
        self.system_prompt = system_prompt
        self.max_turns = max_turns

        self.summary = ""  # long-term compressed memory

        self.recent_messages = [
            {"role": "system", "content": system_prompt}
        ]

        self.known_info = {
            "business_background": None,
            "company_size": None,
            "needs": [],
            "wants_human_contact": False
        }

    def add_user_message(self, message: str):
        self.recent_messages.append(
            {"role": "user", "content": message}
        )

    def add_assistant_message(self, message: str):
        self.recent_messages.append(
            {"role": "assistant", "content": message}
        )

    def update_known_info(self, extracted_info: dict):
        for key, value in extracted_info.items():
            if value is None:
                continue

            if isinstance(value, list):
                for item in value:
                    if item not in self.known_info[key]:
                        self.known_info[key].append(item)
            else:
                self.known_info[key] = value

    def should_summarize(self) -> bool:
        return len(self.recent_messages) > self.max_turns + 1

    def build_prompt_messages(self):
        messages = [{"role": "system", "content": self.system_prompt}]

        if self.summary:
            messages.append({
                "role": "system",
                "content": f"Conversation summary so far:\n{self.summary}"
            })

        messages.extend(self.recent_messages[1:])  # exclude duplicate system

        return messages

    def apply_summary(self, summary_text: str):
        self.summary = summary_text
        # keep only system + last 2 turns
        self.recent_messages = [
            self.recent_messages[0]
        ] + self.recent_messages[-4:]

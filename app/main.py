from app.memory import ConversationMemory
from app.llm import OpenAILLM
from app.prompt import SYSTEM_PROMPT

# Static first greeting (no LLM call → saves cost, consistent UX)
INITIAL_GREETING = (
    "Hey! 👋 I’m Pluto, Zoho’s website assistant.\n\n"
    "I can help you understand what Zoho does, explore products that fit your needs, "
    "and guide you toward the right solutions — all at your own pace.\n\n"
    "Feel free to tell me a bit about your business or what you’re looking for, "
    "and we’ll take it from there."
)


def run_chatbot():
    # Initialize session memory and LLM
    memory = ConversationMemory(SYSTEM_PROMPT)
    llm = OpenAILLM()

    print("Pluto – Zoho Website Assistant")
    print("--------------------------------")

    # Add greeting to memory and display
    memory.add_assistant_message(INITIAL_GREETING)
    print(f"\nPluto: {INITIAL_GREETING}")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("\nPluto: It was great talking to you! 👋")
            break

        # Add user message
        memory.add_user_message(user_input)

        # Build prompt with summary + recent context
        prompt_messages = memory.build_prompt_messages()

        # Generate response
        llm_response = llm.generate(prompt_messages)

        # Update structured memory (business info, intent, etc.)
        memory.update_known_info(llm_response.get("extracted_info", {}))

        assistant_reply = llm_response.get("reply", "")
        memory.add_assistant_message(assistant_reply)

        print(f"\nPluto: {assistant_reply}")

        # Summarize if conversation is getting long
        if memory.should_summarize():
            summary = llm.summarize_conversation(memory.recent_messages)
            memory.apply_summary(summary)

        # Optional debug
        # print("\n[DEBUG] Known Info:", memory.known_info)


if __name__ == "__main__":
    run_chatbot()

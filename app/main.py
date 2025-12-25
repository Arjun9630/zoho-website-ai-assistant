from app.core.orchestrator import ConversationOrchestrator

def run_cli_chatbot():
    bot = ConversationOrchestrator()
    print("Zoho Website Assistant (CLI Mode)")
    print("--------------------------------")

    while bot.context.state.name != "END":
        user_input = input("\nYou: ")
        response = bot.handle_message(user_input)
        print(f"\nBot: {response}")


if __name__ == "__main__":
    run_cli_chatbot()

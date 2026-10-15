from chatbot import ChatbotManager


def main():
    print("=" * 60)
    print("  COLLEGE ENQUIRY CHATBOT (Terminal Version)")
    print("=" * 60)
    print("Type 'exit' to quit, 'help' for commands.\n")

    mgr = ChatbotManager("college_faq_dataset.csv")

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        if user_input.lower() == "help":
            print("Commands: exit, help, categories, clear, stats")
            continue
        if user_input.lower() == "categories":
            print("Categories:", mgr.get_all_categories())
            continue
        if user_input.lower() == "clear":
            mgr.clear_history()
            print("History cleared.")
            continue
        if user_input.lower() == "stats":
            s = mgr.get_session_stats()
            print(f"Messages: {s['total_messages']}, Duration: {s['session_duration']}")
            continue

        resp = mgr.process_user_query(user_input)
        icon = "❓" if resp["is_fallback"] else "✅"
        print(f"\nBot: {resp['answer']}")
        print(
            f"  {icon} Confidence: {resp['confidence']:.1%} | Category: {resp.get('category', 'N/A')}"
        )


if __name__ == "__main__":
    main()

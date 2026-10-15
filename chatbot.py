from nlp_model import CollegeEnquiryChatbot
from datetime import datetime
import json


class ChatbotManager:

    def __init__(self, dataset_path="college_faq_dataset.csv"):
        self.chatbot = CollegeEnquiryChatbot(dataset_path)
        self.conversation_history = []
        self.session_start = datetime.now()

    def process_user_query(self, user_message):
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.conversation_history.append(
            {"timestamp": timestamp, "sender": "user", "message": user_message}
        )

        response = self.chatbot.get_response(user_message)

        self.conversation_history.append(
            {
                "timestamp": timestamp,
                "sender": "bot",
                "message": response["answer"],
                "confidence": response.get("confidence", 0),
                "is_fallback": response.get("is_fallback", False),
                "category": response.get("category", "N/A"),
            }
        )

        return response

    def get_conversation_history(self):
        return self.conversation_history

    def clear_history(self):
        self.conversation_history = []
        self.session_start = datetime.now()

    def get_session_stats(self):
        user_msgs = [m for m in self.conversation_history if m["sender"] == "user"]
        bot_msgs = [m for m in self.conversation_history if m["sender"] == "bot"]
        duration = datetime.now() - self.session_start
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": len(user_msgs),
            "bot_messages": len(bot_msgs),
            "session_duration": str(duration).split(".")[0],
        }

    def get_all_categories(self):
        return self.chatbot.get_all_categories()

    def get_faq_by_category(self, category):
        return self.chatbot.get_category_faq(category)

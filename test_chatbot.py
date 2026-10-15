import unittest
from nlp_model import CollegeEnquiryChatbot
from chatbot import ChatbotManager


class TestChatbot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bot = CollegeEnquiryChatbot("college_faq_dataset.csv")
        cls.mgr = ChatbotManager("college_faq_dataset.csv")

    def test_dataset_loaded(self):
        self.assertEqual(len(self.bot.faq_df), 50)

    def test_preprocessing(self):
        result = self.bot.preprocess_text("What are the ADMISSION requirements?")
        self.assertTrue(len(result) > 0)
        self.assertTrue(result.islower() or result == "")

    def test_known_query(self):
        resp = self.bot.get_response("What courses do you offer?")
        self.assertFalse(resp["is_fallback"])
        self.assertGreater(resp["confidence"], 0.2)

    def test_unknown_query(self):
        resp = self.bot.get_response("xyzabc random nonsense")
        self.assertTrue(resp["is_fallback"])

    def test_empty_query(self):
        resp = self.bot.get_response("")
        self.assertEqual(resp["status"], "error")

    def test_admission_query(self):
        resp = self.bot.get_response("How to apply for admission?")
        self.assertFalse(resp["is_fallback"])

    def test_fee_query(self):
        resp = self.bot.get_response("What are the fees?")
        self.assertGreater(resp["confidence"], 0.2)

    def test_hostel_query(self):
        resp = self.bot.get_response("Tell me about hostel facilities")
        self.assertGreater(resp["confidence"], 0.2)

    def test_conversation_history(self):
        self.mgr.clear_history()
        self.mgr.process_user_query("What is the placement rate?")
        self.assertEqual(len(self.mgr.get_conversation_history()), 2)

    def test_session_stats(self):
        self.mgr.clear_history()
        self.mgr.process_user_query("Test")
        stats = self.mgr.get_session_stats()
        self.assertEqual(stats["user_messages"], 1)
        self.assertEqual(stats["bot_messages"], 1)

    def test_categories(self):
        cats = self.mgr.get_all_categories()
        self.assertIn("Admissions", cats)
        self.assertIn("Courses", cats)
        self.assertIn("Fees", cats)


if __name__ == "__main__":
    unittest.main(verbosity=2)

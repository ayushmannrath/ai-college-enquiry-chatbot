import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import random
import warnings

warnings.filterwarnings("ignore")

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("tokenizers/punkt_tab")  # required by NLTK >= 3.9
except LookupError:
    nltk.download("punkt_tab", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)


class CollegeEnquiryChatbot:

    def __init__(self, dataset_path="college_faq_dataset.csv"):
        self.dataset_path = dataset_path
        self.faq_df = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words("english"))
        self.load_dataset()
        self.build_tfidf_model()

    def load_dataset(self):
        self.faq_df = pd.read_csv(self.dataset_path)
        print(f"Dataset loaded: {len(self.faq_df)} FAQs")

    def preprocess_text(self, text):
        text = text.lower()
        tokens = word_tokenize(text)
        processed = [
            self.stemmer.stem(token)
            for token in tokens
            if token.isalnum() and token not in self.stop_words
        ]
        return " ".join(processed)

    def build_tfidf_model(self):
        processed_questions = [self.preprocess_text(q) for q in self.faq_df["question"]]
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000, min_df=1, max_df=0.8, ngram_range=(1, 2)
        )
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(processed_questions)
        print("TF-IDF model built successfully!")

    def find_best_match(self, user_query, threshold=0.25):
        processed_query = self.preprocess_text(user_query)
        query_vector = self.tfidf_vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]

        if best_score >= threshold:
            return {
                "found": True,
                "question": self.faq_df.loc[best_idx, "question"],
                "answer": self.faq_df.loc[best_idx, "answer"],
                "category": self.faq_df.loc[best_idx, "category"],
                "similarity_score": float(best_score),
            }
        else:
            return {"found": False, "similarity_score": float(best_score)}

    def get_response(self, user_query):
        if not user_query or not user_query.strip():
            return {
                "status": "error",
                "answer": "Please enter a valid question.",
                "is_fallback": True,
                "confidence": 0.0,
                "category": "N/A",
            }

        match = self.find_best_match(user_query)

        if match["found"]:
            return {
                "status": "success",
                "question": match["question"],
                "answer": match["answer"],
                "category": match["category"],
                "confidence": match["similarity_score"],
                "is_fallback": False,
            }
        else:
            fallbacks = [
                "I'm sorry, I couldn't find a specific answer. Please contact our admissions office at admissions@college.edu or call +91-XXXXXXXXXX.",
                "I don't have detailed information about that topic. Please visit our official website or contact our support team.",
                "That's an interesting question! I don't have enough information to answer it accurately. Please contact our admissions team for assistance.",
                "I couldn't match your query to our knowledge base. For help, email admissions@college.edu or call +91-XXXXXXXXXX (9 AM - 5 PM, Mon-Fri).",
            ]
            return {
                "status": "no_match",
                "answer": random.choice(fallbacks),
                "confidence": match["similarity_score"],
                "is_fallback": True,
                "category": "N/A",
            }

    def get_all_categories(self):
        return self.faq_df["category"].unique().tolist()

    def get_category_faq(self, category):
        return self.faq_df[self.faq_df["category"].str.lower() == category.lower()]

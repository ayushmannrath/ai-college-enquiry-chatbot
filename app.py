import streamlit as st
import time
from datetime import datetime
from chatbot import ChatbotManager

# Page setup
st.set_page_config(page_title="College Enquiry Chatbot", page_icon="🎓", layout="wide")

# Custom CSS
st.markdown(
    """
<style>
    .user-msg {
        background-color: #e3f2fd;
        padding: 12px 16px;
        border-radius: 10px;
        border-left: 4px solid #1976d2;
        margin: 8px 0;
    }
    .bot-msg {
        background-color: #f3e5f5;
        padding: 12px 16px;
        border-radius: 10px;
        border-left: 4px solid #7b1fa2;
        margin: 8px 0;
    }
    .meta {
        font-size: 0.75em;
        color: gray;
        margin-top: 6px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "manager" not in st.session_state:
    st.session_state.manager = ChatbotManager("college_faq_dataset.csv")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.markdown("# 🎓 College Enquiry Chatbot")
st.markdown(
    "Ask questions about **admissions, courses, fees, scholarships, placements, and facilities**."
)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Options")

    stats = st.session_state.manager.get_session_stats()
    st.metric("Total Messages", stats["total_messages"])
    st.metric("Your Questions", stats["user_messages"])
    st.metric("Session Duration", stats["session_duration"])

    st.markdown("---")
    st.subheader("🏷️ Browse by Category")
    categories = st.session_state.manager.get_all_categories()
    selected_cat = st.selectbox("Pick a category:", ["-- Select --"] + categories)

    if selected_cat != "-- Select --":
        faqs = st.session_state.manager.get_faq_by_category(selected_cat)
        for _, row in faqs.head(4).iterrows():
            if st.button(
                f"📌 {row['question'][:45]}...", key=f"cat_{row['question_id']}"
            ):
                st.session_state.pending_query = row["question"]
                st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.manager.clear_history()
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.info("""
    **📞 Contact Us**
    📧 admissions@college.edu
    📞 +91-XXXXXXXXXX
    🕐 9 AM – 5 PM (Mon–Fri)
    """)

# Display chat history
for msg in st.session_state.messages:
    if msg["sender"] == "user":
        st.markdown(
            f"""
        <div class="user-msg">
            <b>👤 You</b> ({msg['timestamp']})<br>
            {msg['message']}
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        icon = "❓" if msg.get("is_fallback") else "✅"
        st.markdown(
            f"""
        <div class="bot-msg">
            <b>🤖 Chatbot</b> ({msg['timestamp']})<br>
            {msg['message']}
            <div class="meta">
                {icon} Confidence: {msg.get('confidence', 0):.1%} |
                Category: {msg.get('category', 'N/A')}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# Handle pending query from sidebar button click
pending = st.session_state.pop("pending_query", None)

# User input
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "Type your question:",
        value=pending if pending else "",
        placeholder="e.g. What are the admission requirements?",
        key="input_box",
    )
with col2:
    send_clicked = st.button("Send 📤", use_container_width=True)

# Process input
if (send_clicked or pending) and (user_input or pending):
    query = pending if pending else user_input
    if query.strip():
        with st.spinner("🤖 Thinking..."):
            time.sleep(0.3)
            response = st.session_state.manager.process_user_query(query)

        ts = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append(
            {"sender": "user", "message": query, "timestamp": ts}
        )
        st.session_state.messages.append(
            {
                "sender": "bot",
                "message": response["answer"],
                "timestamp": ts,
                "confidence": response.get("confidence", 0),
                "is_fallback": response.get("is_fallback", False),
                "category": response.get("category", "N/A"),
            }
        )
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<center><i>Made with ❤️ | College Enquiry Chatbot v1.0</i></center>",
    unsafe_allow_html=True,
)

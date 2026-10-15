import streamlit as st
import time
from datetime import datetime
from chatbot import ChatbotManager

# Page setup
st.set_page_config(
    page_title="College Enquiry Chatbot",
    page_icon="🎓",
    layout="wide",
)

# Session state
if "manager" not in st.session_state:
    st.session_state.manager = ChatbotManager("college_faq_dataset.csv")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Theme palette
if st.session_state.dark_mode:
    app_background = "#0f172a"
    surface = "#1e293b"
    surface_alt = "#263449"
    text = "#f8fafc"
    muted = "#cbd5e1"
    border = "#475569"
    input_background = "#111827"
    user_background = "#12345b"
    bot_background = "#352d55"
    header_background = "#172554"
else:
    app_background = "#f7f9fc"
    surface = "#ffffff"
    surface_alt = "#f8fafc"
    text = "#172033"
    muted = "#64748b"
    border = "#cbd5e1"
    input_background = "#ffffff"
    user_background = "#e3f2fd"
    bot_background = "#f3e5f5"
    header_background = "#ffffff"

# Contrast-safe styling. Keep selectors scoped; do not color every div globally.
st.markdown(
    f"""
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {app_background} !important;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        background-color: {app_background} !important;
    }}

    [data-testid="stHeader"] {{
        background-color: {app_background} !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: {surface} !important;
        border-right: 1px solid {border} !important;
    }}

    [data-testid="stSidebar"] section,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6 {{
        color: {text} !important;
    }}

    .app-title {{
        background: {header_background} !important;
        border: 1px solid {border} !important;
        border-radius: 16px !important;
        padding: 20px 24px !important;
        margin: 0 0 10px 0 !important;
    }}

    .app-title h1 {{
        color: {text} !important;
        margin: 0 0 6px 0 !important;
        font-size: 2rem !important;
    }}

    .app-title p {{
        color: {muted} !important;
        margin: 0 !important;
        font-size: 0.98rem !important;
    }}

    .user-msg {{
        background-color: {user_background} !important;
        color: {text} !important;
        padding: 12px 16px;
        border-radius: 10px;
        border: 1px solid {border} !important;
        border-left: 4px solid #1976d2 !important;
        margin: 8px 0;
    }}

    .bot-msg {{
        background-color: {bot_background} !important;
        color: {text} !important;
        padding: 12px 16px;
        border-radius: 10px;
        border: 1px solid {border} !important;
        border-left: 4px solid #a855f7 !important;
        margin: 8px 0;
    }}

    .user-msg b, .bot-msg b,
    .user-msg span, .bot-msg span,
    .user-msg div, .bot-msg div,
    .user-msg br, .bot-msg br {{
        color: {text} !important;
    }}

    .meta {{
        color: {muted} !important;
        font-size: 0.75em;
        margin-top: 6px;
    }}

    /* Normal Streamlit markdown text, excluding the custom title and messages. */
    [data-testid="stAppViewContainer"] .stMarkdown:not(:has(.app-title)):not(:has(.user-msg)):not(:has(.bot-msg)) p,
    [data-testid="stAppViewContainer"] .stMarkdown:not(:has(.app-title)):not(:has(.user-msg)):not(:has(.bot-msg)) li,
    [data-testid="stAppViewContainer"] .stMarkdown:not(:has(.app-title)):not(:has(.user-msg)):not(:has(.bot-msg)) h1,
    [data-testid="stAppViewContainer"] .stMarkdown:not(:has(.app-title)):not(:has(.user-msg)):not(:has(.bot-msg)) h2,
    [data-testid="stAppViewContainer"] .stMarkdown:not(:has(.app-title)):not(:has(.user-msg)):not(:has(.bot-msg)) h3,
    [data-testid="stAppViewContainer"] .stMarkdown:not(:has(.app-title)):not(:has(.user-msg)):not(:has(.bot-msg)) h4,
    [data-testid="stAppViewContainer"] .stMarkdown:not(:has(.app-title)):not(:has(.user-msg)):not(:has(.bot-msg)) label {{
        color: {text} !important;
    }}

    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {{
        color: {muted} !important;
    }}

    input, textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] > div {{
        background-color: {input_background} !important;
        color: {text} !important;
        -webkit-text-fill-color: {text} !important;
        border: 1px solid {border} !important;
    }}

    input::placeholder, textarea::placeholder {{
        color: {muted} !important;
        -webkit-text-fill-color: {muted} !important;
    }}

    div[data-baseweb="select"] *,
    div[data-baseweb="input"] *,
    div[data-baseweb="textarea"] * {{
        color: {text} !important;
    }}

    .stButton > button {{
        background-color: {surface} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
    }}

    .stButton > button:hover {{
        border-color: #60a5fa !important;
        color: {text} !important;
    }}

    [data-testid="stMetric"] {{
        background-color: {surface_alt} !important;
        border: 1px solid {border} !important;
    }}

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {{
        color: {text} !important;
    }}

    [data-testid="stExpander"] {{
        background-color: {surface} !important;
        border: 1px solid {border} !important;
    }}

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] details {{
        color: {text} !important;
    }}

    .stAlert, .stAlert * {{
        color: {text} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Options")

    st.toggle(
        "🌙 Dark mode",
        key="dark_mode",
        help="Switch between light and dark mode",
    )

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
                f"📌 {row['question'][:45]}...",
                key=f"cat_{row['question_id']}",
            ):
                st.session_state.pending_query = row["question"]
                st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.manager.clear_history()
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.info(
        """
        **📞 Contact Us**
        
        📧 admissions@college.edu  
        📞 +91-XXXXXXXXXX  
        🕐 9 AM – 5 PM (Mon–Fri)
        """
    )

# Main header
st.markdown(
    """
    <div class="app-title">
        <h1>🎓 College Enquiry Chatbot</h1>
        <p>Ask questions about admissions, courses, fees, scholarships, placements, and facilities.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

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

        timestamp = datetime.now().strftime("%H:%M:%S")

        st.session_state.messages.append(
            {
                "sender": "user",
                "message": query,
                "timestamp": timestamp,
            }
        )

        st.session_state.messages.append(
            {
                "sender": "bot",
                "message": response["answer"],
                "timestamp": timestamp,
                "confidence": response.get("confidence", 0),
                "is_fallback": response.get("is_fallback", False),
                "category": response.get("category", "N/A"),
            }
        )

        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:" + muted + ";'><i>Made with ❤️ | College Enquiry Chatbot v1.0</i></div>",
    unsafe_allow_html=True,
)

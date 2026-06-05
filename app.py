from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import os
st.set_page_config(
    page_title="InAmigos AI Assistant",
    page_icon="🤝",
    layout="wide"
)
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

h1 {
    text-align: center;
}

div[data-testid="stMetric"] {
    background-color: rgba(250,250,250,0.05);
    border-radius: 12px;
    padding: 12px;
}

.stChatMessage {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# Load API key
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# Load NGO data
with open(
    "ngo_data.txt",
    "r",
    encoding="utf-8"
) as f:
    ngo_data = f.read()

SYSTEM_PROMPT = """
You are the official AI Assistant for InAmigos Foundation.

Rules:
1. Answer ONLY using the NGO information provided.
2. Be professional and concise.
3. Do not invent information.
4. Use conversation history to understand follow-up questions.
5. If the answer is not found in the NGO information, reply exactly:
'I could not find that information on the InAmigos Foundation website.'
"""
with st.sidebar:

    st.image(
    "https://inamigosfoundation.org.in/wp-content/uploads/2024/11/logo.png",
    width=180
)

    st.write("""
    InAmigos Foundation is a Section 8
    non-profit organization working in:
    
    • Education
    • Women Empowerment
    • Animal Welfare
    • Environment
    • Social Development
    """)

    st.header("💡 Sample Questions")

    st.write("• Who founded InAmigos Foundation?")
    st.write("• What is Project Udaan?")
    st.write("• What is Project Jeev?")
    st.write("• How can I contact the NGO?")
    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
st.title("🤝 InAmigos Foundation AI Assistant")

st.caption(
    "Empowering Communities Through AI-Powered Support"
)
st.markdown("""
### 🌍 Creating Impact Across India

InAmigos Foundation works in education, women empowerment,
animal welfare, environmental sustainability, and social development.

Ask me anything about our initiatives, events, volunteering opportunities,
or contact information.
""")
with st.container():

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Volunteers", "200+")

    with col2:
        st.metric("States", "28")

    with col3:
        st.metric("Beneficiaries", "50,000+")

    with col4:
        st.metric("Projects", "6")
st.subheader("🌟 Our Major Initiatives")

with st.expander("🚀 Project Udaan"):
    st.write(
        "Women empowerment through skill development and financial independence."
    )

with st.expander("🐾 Project Jeev"):
    st.write(
        "Animal welfare, rescue, protection and feeding."
    )

with st.expander("📚 Project BachpanSala"):
    st.write(
        "Quality education for underprivileged children."
    )

with st.expander("🌱 Project Prakriti"):
    st.write(
        "Environmental conservation and sustainability."
    )
st.markdown(
    "Ask questions about InAmigos Foundation, its projects, events, and initiatives."
)

# Session state for memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
st.info(
    "Ask me anything about InAmigos Foundation, volunteering, projects, events, or contact information."
)
st.subheader("⚡ Quick Questions")

col1, col2 = st.columns(2)

if col1.button("Who founded InAmigos Foundation?"):
    st.session_state.quick_question = (
        "Who founded InAmigos Foundation?"
    )

if col2.button("What is Project Udaan?"):
    st.session_state.quick_question = (
        "What is Project Udaan?"
    )
# Chat input
user_input = st.chat_input("Ask a question...")
if "quick_question" in st.session_state:
    user_input = st.session_state.quick_question
    del st.session_state.quick_question

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Build history
    history_text = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in st.session_state.messages[-10:]
        ]
    )

    prompt = f"""
{SYSTEM_PROMPT}

NGO Information:
{ngo_data}

Conversation History:
{history_text}

Current User Question:
{user_input}
"""

    try:
        with st.spinner("Thinking..."):
             response = model.generate_content(prompt)

        answer = response.text.strip()

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

        # Save log
        with open(
            "chat_log.txt",
            "a",
            encoding="utf-8"
        ) as log:
            log.write(f"User: {user_input}\n")
            log.write(f"Bot: {answer}\n")
            log.write("-" * 50 + "\n")

    except Exception as e:
        st.error(str(e))
st.markdown("---")

st.caption(
    "Powered by Gemini AI | Built for InAmigos Foundation"
)
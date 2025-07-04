# tgp_v1_O2Xw6iZvD3rf4JVgxDG1A4uvnV0zpKPAaVOJ9wAR3Mg
import streamlit as st
import requests

# Your Together.ai API key
API_KEY = "tgp_v1_O2Xw6iZvD3rf4JVgxDG1A4uvnV0zpKPAaVOJ9wAR3Mg"

st.set_page_config(page_title="🧠 Memory Chatbot")
st.title("🧠 Chatbot with Memory")

# for pdf uploading
uploaded_pdf = st.sidebar.file_uploader("📄 Upload a PDF", type="pdf")

pdf_text = ""
if uploaded_pdf:
    import fitz  # PyMuPDF
    with fitz.open(stream=uploaded_pdf.read(), filetype="pdf") as doc:
        for page in doc:
            pdf_text += page.get_text()

    st.sidebar.success("PDF content loaded!")

    # Add PDF content as a system message context
    st.session_state.messages.insert(1, {
        "role": "system",
        "content": f"The user uploaded this PDF. Here's the content:\n\n{pdf_text}"
    })

# 🎭 Personality Selector
personality = st.sidebar.selectbox(
    "Choose Personality",
    ["Friendly", "Formal", "Developer", "Funny", "Jerk" ],
    index=0
)

# 🧠 Define system prompts
system_prompts = {
    "Friendly": "You are a friendly and helpful assistant. Keep responses warm and conversational.",
    "Formal": "You are a professional assistant. Respond in a clear, concise, and formal tone.",
    "Developer": "You are a helpful programming assistant. Focus on tech and explain code clearly.",
    "Funny": "You are a witty and humorous assistant. Add light humor where possible.",
    "Jerk": "You are a rude and lazy assistant. Act sarcastic, dismissive, and give unhelpful or annoying replies. Always act like you're too tired to help.",
   
}

# 🔁 Track personality changes and reset memory if needed
if "personality" not in st.session_state:
    st.session_state.personality = personality

if personality != st.session_state.personality:
    st.session_state.messages = [
        {"role": "system", "content": system_prompts[personality]}
    ]
    st.session_state.personality = personality
    st.experimental_rerun()

# 🧠 Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompts[personality]}
    ]

# 💬 Display chat history
for msg in st.session_state.messages[1:]:  # skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ✍️ User input
prompt = st.chat_input("Say something...")

if prompt:
    # Add user message to memory
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 🚀 API call to Together.ai
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": st.session_state.messages,
        "temperature": 0.7,
        "max_tokens": 300
    }

    with st.spinner("Thinking..."):
        res = requests.post(url, headers=headers, json=data)
        reply = res.json()["choices"][0]["message"]["content"]

    # Save reply to memory and display
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

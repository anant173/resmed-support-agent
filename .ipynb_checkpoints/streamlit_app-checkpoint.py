import asyncio
import uuid
import streamlit as st
# Import the run_agent function from the new project structure
from src.agent.graph import run_agent

# Note: The location of this function might change in future Streamlit versions.
# We keep it here to detect direct run vs. 'streamlit run'
from streamlit.runtime.scriptrunner import get_script_run_ctx

# Check if run correctly
ctx = get_script_run_ctx()
if ctx is None:
    print("************")
    print("PLEASE NOTE: run this app with `streamlit run streamlit_app.py`")
    print("************")
    exit(1)

# Suggested questions customized for the ResMed Agent
SUGGESTED_QUESTIONS = [
    "What devices are connected to my account?",
    "Check my compliance for the AirSense 10 model.",
    "I hear a clicking sound in my AirSense 10, what should I do?",
    "I'm feeling very dry in the morning, what is the fix?",
]


def initialize_session_state():
    """Initializes the thread ID and chat message history."""
    if "thread_id" not in st.session_state:
        # A unique ID for this conversation thread, used by LangGraph for memory
        st.session_state.thread_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello, I am your Certified Sleep Therapist Agent. I can help you with device troubleshooting and compliance checks. How may I assist you?",
            }
        ]


async def process_input(user_input):
    """Handles user input, calls the async agent, and updates the chat UI."""
    # Add user message to the chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Consulting device metrics and clinical guidelines..."):
            # AWAIT the asynchronous run_agent function
            response = await run_agent(st.session_state.thread_id, user_input)
            
            # Extract and display the final response
            if response and response.get("response"):
                assistant_response = response["response"]
                st.write(assistant_response)
                # Save the assistant's response to the chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            else:
                 st.write("I'm sorry, I couldn't process that request.")
                 st.session_state.messages.append({"role": "assistant", "content": "I'm sorry, I couldn't process that request."})


# --- Application Setup ---

# Initialize session state (must happen before UI elements)
initialize_session_state()

# Set page config
st.set_page_config(page_title="ResMed Sleep Therapist Agent")
st.title("💤 ResMed Sleep Therapist Agent")

# Sidebar for suggestions and file upload (File upload is kept but may not be relevant 
# for a RAG agent without file processing tools)
with st.sidebar:
    st.header("Quick Questions")
    for question in SUGGESTED_QUESTIONS:
        # Use asyncio.run since Streamlit's context is synchronous
        if st.button(question, key=question, use_container_width=True):
            asyncio.run(process_input(question))
            st.rerun()

    st.header("Upload File")
    uploaded_file = st.file_uploader("Upload device log file", type=["txt"])
    if uploaded_file is not None:
        file_contents = uploaded_file.getvalue().decode("utf-8")
        if st.button("Process File"):
            asyncio.run(process_input(file_contents))
            st.rerun()

# Display existing chat messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Prompt for user input and save
if prompt := st.chat_input("Ask about your device, compliance, or troubleshooting..."):
    # Run the processing function when the user submits input
    asyncio.run(process_input(prompt))
    st.rerun()
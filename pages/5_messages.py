# Import Streamlit for rendering UI components
import streamlit as st
# Let's import the specific Message Objects that Langchain uses under the hood 
# to represent a history of text between an AI, a User, and a System.
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# Import our AI model connection
from langchain_google_genai import ChatGoogleGenerativeAI
# Import tool to safely load our hidden API key
from dotenv import load_dotenv

# Run the dotenv command to fetch the API Key mapping from the hidden file
load_dotenv()
# Bind our model instance to Gemini 2.5 Flash
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Configure tab/page metadata
st.set_page_config(page_title="5. Raw Messages", layout="wide")
# Main visual title for the UI
st.title("📚 5. Raw Message Objects")

# Show an informational box explaining WHY we have these distinct classes instead of strings.
st.info("""
**What is this?** LangChain represents conversation using distinct objects: `SystemMessage`, `HumanMessage`, and `AIMessage`. 
**Why?** This is the underlying format Chat LLMs natively speak. By chaining these objects in a Python list directly, you simulate a conversation history.
""")

st.write("### Code Implementation:")
# Show the literal python object definitions
st.code('''messages = [
    SystemMessage(content='You are a helpful assistant'),
    HumanMessage(content='What is the capital of France?'),
    AIMessage(content='The capital of France is Paris.'),
    HumanMessage(content='How many people live there?')
]
result = model.invoke(messages)''', language='python')

st.write("---")
st.write("### See It Working!")

st.write("Below is a hardcoded conversation list. We are sending the AI the past context so it can answer the final question intelligently.")

# We are defining a static list of python objects representing a conversation timeline. 
# System > Human > AI responds > Human asks follow-up. 
# Without the AI's prior response and the Human's original question in 'memory', the last question "What were their names again?" makes zero sense!
messages = [
    SystemMessage(content='You are a helpful assistant'), # Sets the initial rule that dictates AI behavior
    HumanMessage(content='I have two dogs. Their names are Max and Bella.'), # Initial fact established
    AIMessage(content='Nice to meet you! How can I help you and your dogs today?'), # The AI response to that fact
    HumanMessage(content='What were their names again?') # A question relying ENTIRELY on conversational history
]

# We loop through those messages to draw them to the UI as an interactive chat log
for msg in messages:
    # A ternary expression to figure out what Role the message belongs to based on its Type
    with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant" if isinstance(msg, AIMessage) else "system"):
        # Output the text content of that specific message step
        st.write(msg.content)

# The user clicks the button
if st.button("Invoke Model (Test its Memory)"):
    # While it waits, we tell the user a network call is processing
    with st.spinner("Gemini is reading the history..."):
        # We invoke the model, passing the ENTIRE LIST of 4 messages, not just the last one. 
        # The AI reads the entire chain to understand context, then generates a single AIMessage back.
        result = model.invoke(messages)
        # We render the final returned element as an assistant's response in the UI chat box
        with st.chat_message("assistant"):
            # Output the raw textual content of the AI's response
            st.success(result.content)

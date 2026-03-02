# Import Streamlit for standard UI design
import streamlit as st
# Import ChatPromptTemplate (to manage roles like System vs Human)
# Import MessagesPlaceholder (a specialized tool to inject arbitrary lists of messages rapidly)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# Import standard message objects
from langchain_core.messages import HumanMessage, AIMessage
# Import connection to Gemini model endpoint
from langchain_google_genai import ChatGoogleGenerativeAI
# Import to fetch passwords/keys from .env file securely
from dotenv import load_dotenv

# Load all variables internally
load_dotenv()
# Bind 'model' to Google Generative AI
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Set basic page configuration parameters
st.set_page_config(page_title="6. Message Placeholders", layout="wide")
# Establish the UI title header
st.title("📚 6. Message Placeholders")

# Give context as to what a MessagesPlaceholder achieves
st.info("""
**What is this?** `MessagesPlaceholder` lets you inject a dynamic LIST of past messages directly into your prompt sequence.
**Why?** Instead of manually managing lists of `SystemMessage` strings like in Example 5, you can use a Template to easily inject dynamic memory history right before the newest Human question.
""")

st.write("### Code Implementation:")
# Embed code demonstration for visual learning
st.code('''chat_template = ChatPromptTemplate([
    ('system', 'You are a customer support agent.'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human', '{query}')
])''', language='python')

# The implementation involves mapping three distinct parts to a Template array:
# 1. Provide the fixed, static system context (defining rules and boundaries)
# 2. Open up a dynamic hole labeled 'chat_history' via MessagesPlaceholder. 
#    This explicitly tells LangChain "When invoked, expect me to hand you an actual Python List of messages to inject here".
# 3. Add the new immediate action via a dynamic {query} string for the Human.
chat_template = ChatPromptTemplate([
    ('system', 'You are a customer support agent.'),
    MessagesPlaceholder(variable_name='chat_history'), # Look here: It accepts a whole block of chat history!
    ('human', '{query}')
])

st.write("---")
st.write("### Try it out!")

# Provide a fixed "Dummy History" list object to show what happens when history exists
st.write("**Pre-loaded History list injecting into `chat_history` variable:**")
dummy_history = [
    HumanMessage(content="My order #12345 hasn't arrived."), # Past User question
    AIMessage(content="I'm sorry to hear that. I see it is delayed in transit.") # Past AI reply
]
# For instructional clarity, display that history block as a JSON string to visually confirm what it holds
st.json([{"Role": msg.type, "Content": msg.content} for msg in dummy_history])

# Expose a text box so we can simulate the MOST RECENT new question they are asking right now
query = st.text_input("New 'human' Query:", "Where is my refund?")

# Trigger the invocation test
if st.button("Send to AI"):
    # When invoking, we provide the dummy_history list to map to the 'chat_history' placeholder
    # And we map our text_input string 'query' to the {query} placeholder
    prompt = chat_template.invoke({
        'chat_history': dummy_history, 
        'query': query
    })
    
    # We display what the fully assembled list of messages looks like when flattened by LangChain
    st.write("**Final Assembled Messages List (Under the hood):**")
    st.json([{"Role": msg.type, "Content": msg.content} for msg in prompt.messages])
    
    # Execute the request to the network
    with st.spinner("Connecting to Gemini..."):
        # The AI responds successfully using the provided context mapped seamlessly
        result = model.invoke(prompt)
        # And renders out
        st.success(result.content)

# Import Streamlit for rendering UI components
import streamlit as st
# Import generative AI client package
from langchain_google_genai import ChatGoogleGenerativeAI
# Import specialized classes representing our system boundaries, our user inputs, and our AI outputs
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# Import function for keeping secrets out of code
from dotenv import load_dotenv

# Extract tokens
load_dotenv()
# Bind specific model to the environment
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Map standard properties for an individual browser page
st.set_page_config(page_title="7. Continuous Chatbot", layout="wide")
# Provide header description
st.title("📚 7. A Real Continuous Chatbot")

# Explain the culmination of these techniques
st.info("""
**What is this?** This brings everything together into a fully functional memory-based chatbot using Streamlit's session state.
""")

st.write("### Code Concept:")
# Detail out exactly the procedural flow of how standard Chatbots (like ChatGPT or Character.AI) function under the hood!
st.markdown("""
1. Store a list of messages in memory (`st.session_state`).
2. Every time the user types, append a `HumanMessage`.
3. Pass the *entire list* to `model.invoke()`.
4. Append the returned `AIMessage` to memory.
""")

st.write("---")

# Memory Architecture: Initialize a session state entry. Streamlit re-runs scripts top to bottom constantly, 
# so 'st.session_state' is a special dictionary that persists data between those renders!
if "chat_history" not in st.session_state:
    # If starting fresh, set list up with a default SystemMessage dictating behavior
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful, extremely polite AI assistant.")
    ]

# Each time the script re-renders, immediately iterate through that stored memory array
for msg in st.session_state.chat_history:
    # We purposefully exclude rendering 'SystemMessages' because the user shouldn't see developer backend instructions in their Chat UI!
    if isinstance(msg, SystemMessage):
        continue # Skip this loop sequence
    
    # Determine the role dynamically based on the exact Class type
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    # Create the visual chat bubble element on the Streamlit web app mapped to that role
    with st.chat_message(role):
        # Insert the message's written content inside the chat bubble
        st.markdown(msg.content)

# Define an input bar at the bottom of the form for new chat commands
new_input = st.chat_input("Ask a question...")

# An implicit 'if something was typed into the box' check
if new_input:
    # 1. Immediately append their new text line formatted as a HumanMessage object, adding it to the end of the history array
    st.session_state.chat_history.append(HumanMessage(content=new_input))
    # Draw it locally to their screen as well so they see it instantly while loading
    with st.chat_message("user"):
        st.markdown(new_input)
        
    # 2. Invoke the model over the network
    with st.spinner("Thinking..."):
        # Notice we are passing the ENTRIE expanded memory list 'st.session_state.chat_history' through LangChain every single time
        result = model.invoke(st.session_state.chat_history)
        
    # Create an assistant chat bubble and render what it finally decided to say back
    with st.chat_message("assistant"):
        st.markdown(result.content)
        
    # 3. Add the newly generated AI response object back into our array history! 
    # This prepares the list for the NEXT time they type something into the input box!
    st.session_state.chat_history.append(AIMessage(content=result.content))
    
st.write("---")
# Map an optional UI button allowing power users to 'flush' their history manually by defaulting the variable!
if st.button("Clear History"):
    # Purge everything except the original underlying SystemMessage foundation!
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful, extremely polite AI assistant.")
    ]
    # Programmatically trigger a re-render to erase chat bubbles from screen
    st.rerun()

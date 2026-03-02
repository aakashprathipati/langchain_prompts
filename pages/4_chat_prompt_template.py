# Import Streamlit for web interface
import streamlit as st
# Import ChatPromptTemplate (special template that handles message roles instead of raw strings)
from langchain_core.prompts import ChatPromptTemplate
# Import generative AI link to Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
# Import to pull keys from the .env environment
from dotenv import load_dotenv

# Pull Keys
load_dotenv()
# Bind model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Set the window title
st.set_page_config(page_title="4. Chat Prompt Template", layout="wide")
# Set the main header text
st.title("📚 4. Chat Prompt Templates")

# Output an info message explaining the difference between a normal template and a Chat template
st.info("""
**What is this?** Unlike normal Prompts that create a single string, `ChatPromptTemplate` builds a list of messages based on **Roles**. 
**Why?** Modern LLMs are trained to understand the difference between 'System' (instructions), 'Human' (user input), and 'AI' (previous outputs).
""")

st.write("### Code Implementation:")
# Show the code representation
st.code('''chat_template = ChatPromptTemplate([
    ('system', 'You are an expert in {domain}. Reply concisely.'),
    ('human', 'Can you explain {topic}?')
])''', language='python')

# The implementation: We give ChatPromptTemplate a list of tuples. 
# The left side identifies the ROLE (system = rules, human = the request).
# The right side holds the actual text to pass, containing dynamic '{placeholder}' markers.
chat_template = ChatPromptTemplate([
    ('system', 'You are an expert in {domain}. Reply concisely.'),
    ('human', 'Can you explain {topic}?')
])

st.write("---")
st.write("### Try it out!")

# Spilt view evenly
col1, col2 = st.columns(2)
with col1:
    # A dropdown allowing us to dynamically change the 'System' instruction parameters
    domain = st.selectbox("Select System Domain (How it behaves):", ["Cooking", "Quantum Physics", "Video Games"])
with col2:
    # A text box to type 'Human' questions into
    topic = st.text_input("Human Topic (What you ask):", "How do I make a good sauce?")

# Generate UI Button
if st.button("Generate Response"):
    
    # Fill in the placeholders mapping both the system domain and human topic simultaneously
    prompt = chat_template.invoke({'domain': domain, 'topic': topic})
    
    # For educational purposes, expose what LangChain assembled using JSON formatting
    st.write("**What LangChain generated under the hood (A list of formatted Messages):**")
    # Loop over the message list from the prompt and draw it to the UI
    st.json([{"Role": msg.type, "Content": msg.content} for msg in prompt.messages])
    
    # Finally, execute this list of messages against the AI model
    with st.spinner("Connecting to Gemini..."):
        result = model.invoke(prompt)
        # Yield the response
        st.success(result.content)

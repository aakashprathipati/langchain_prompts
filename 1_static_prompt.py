# Import the Streamlit library for building the web interface
import streamlit as st
# Import PromptTemplate to create prompt structures around our strings
from langchain_core.prompts import PromptTemplate
# Import ChatGoogleGenerativeAI to connect and interact with the Gemini model
from langchain_google_genai import ChatGoogleGenerativeAI
# Import load_dotenv to automatically load environment variables (like API keys) from a .env file
from dotenv import load_dotenv

# Execute the function to load the variables from the .env file hidden in the directory
load_dotenv()
# Initialize the Gemini model, specifically asking for the fast 'gemini-2.5-flash' version
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Set the initial configuration for the Streamlit page (browser tab metadata and layout)
st.set_page_config(page_title="1. Static Prompt", layout="wide")
# Display the main large title of the web page
st.title("📚 1. Static Prompts")

# Display a blue informational message box explaining the concept
st.info("""
**What is this?** A Static Prompt is completely hardcoded. It has NO placeholders and asks the AI for the exact same thing every single time.
**When to use it:** For fixed actions that never change based on user input. For example: Generating a random daily fact, extracting fixed keywords, or evaluating standard criteria.
""")

# Write a subtitle for the code snippet section directly to the UI
st.write("### Code Implementation:")
# Display the raw python code inside a formatted block on the UI for learning purposes
st.code('''static_template = PromptTemplate.from_template(
    "Tell me a random fun fact about outer space. Be concise."
)''', language='python')

# Actually create the static prompt template in Python with our hardcoded string
static_template = PromptTemplate.from_template(
    "Tell me a random fun fact about outer space. Be concise."
)

# Draw a horizontal separation line on the web page GUI
st.write("---")
# Write a subtitle to introduce the testing section
st.write("### Try it out!")
# Write a basic string noticing the lack of inputs
st.write("Notice how there are no input fields. The prompt is fixed.")

# Render a button in Streamlit; the 'if' triggers only when the user clicks the button
if st.button("Generate Random Space Fact"):
    # Trigger a loading spinner animation on the screen while waiting for the network call
    with st.spinner("Connecting to Gemini..."):
        # Invoke the template to build the prompt value. We pass an empty dictionary {} because there are no variables.
        prompt = static_template.invoke({})
        # Send the constructed prompt over the internet to the Gemini model and retrieve the response
        result = model.invoke(prompt)
        # Display the text content of the result in a green success box on the UI
        st.success(result.content)

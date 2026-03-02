# Import the Streamlit library to build the front-end UI
import streamlit as st
# Import PromptTemplate to work with prompt structures
from langchain_core.prompts import PromptTemplate
# Import ChatGoogleGenerativeAI to communicate with the Google AI models
from langchain_google_genai import ChatGoogleGenerativeAI
# Import environment loader to securely fetch our API Keys
from dotenv import load_dotenv

# Load those variables into the active environment so LangChain can find GOOGLE_API_KEY
load_dotenv()
# Set up the model connection to the specific gemini 2.5 flash model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Set up the UI layout to take up the full width of the browser and set the tab title
st.set_page_config(page_title="2. Dynamic Prompt (Inline)", layout="wide")
# Add a massive H1 title to the UI
st.title("📚 2. Dynamic Prompts (Inline)")

# Show an info box explaining how inline dynamic mapping works
st.info("""
**What is this?** A Dynamic Prompt changes based on user input. Using `{braces}` directly inside your string creates *placeholders*. LangChain automatically finds `{topic}` and `{tone}`.
**When to use it:** When your application needs to combine a fixed instruction with user-provided data, like writing emails or generating tailored content.
""")

# Show the code section label
st.write("### Code Implementation:")
# Render a code block purely for reading
st.code('''inline_template = PromptTemplate.from_template(
    "Write a short, engaging description about {topic}. Make it sound {tone}."
)''', language='python')

# The actual creation of the dynamic prompt template. Notice the curly braces {topic} and {tone}. 
# `from_template` magically scans the string and figures out what variables are needed.
inline_template = PromptTemplate.from_template(
    "Write a short, engaging description about {topic}. Make it sound {tone}."
)

# Draw a divider
st.write("---")
st.write("### Try it out!")

# Split the UI into two equal columns side-by-side
col1, col2 = st.columns(2)
with col1:
    # In the first column, render a text input box and store what the user types in the 'topic' variable
    topic = st.text_input("Enter a topic:", "Artificial Intelligence")
with col2:
    # In the second column, render a dropdown select box and store the choice in the 'tone' variable
    tone = st.selectbox("Select a tone:", ["Professional", "Humorous", "Sarcastic", "Pirate"])

# When the user clicks the Generate button...
if st.button("Generate Description"):
    # While it's processing, show a loading spinner
    with st.spinner("Connecting to Gemini..."):
        # We pass a dictionary to `.invoke()` to map our UI variables into the string's {placeholders}
        prompt = inline_template.invoke({'topic': topic, 'tone': tone})
        
        # Display exactly what string text was assembled and about to be sent to the AI
        st.write("**Actual Prompt Sent to AI:**", prompt.text)
        
        # Finally, ask the AI to generate a response using that final formatted string
        result = model.invoke(prompt)
        
        # Render the AI's content response in a green box to the screen
        st.success(result.content)

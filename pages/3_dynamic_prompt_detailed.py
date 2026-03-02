# Import Streamlit for web app creation
import streamlit as st
# Import PromptTemplate for handling variables in strings
from langchain_core.prompts import PromptTemplate
# Import generative AI client connection for Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
# Import function to fetch keys securely
from dotenv import load_dotenv

# Execute it to load GOOGLE_API_KEY
load_dotenv()
# Bind our model instance to Gemini 2.5 Flash
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Setup page properties
st.set_page_config(page_title="3. Dynamic Prompt (Detailed)", layout="wide")
# Setup the UI title
st.title("📚 3. Dynamic Prompts (Detailed Mapping)")

# Render an explanation of explicitly mapping variables
st.info("""
**What is this?** Similar to inline prompts, but we explicitly list out the `input_variables`.
**Why do this?** It provides strict validation. If an app expects 3 variables but the user/code only provides 2, LangChain will immediately throw an error rather than sending a broken prompt to the AI.
**When to use it:** In complex production apps where missing data should crash the process cleanly, ensuring safety.
""")

st.write("### Code Implementation:")
# Show what we are coding
st.code('''template = PromptTemplate(
    template="Extract the {data_type} from this text: '{source_text}'",
    input_variables=["data_type", "source_text"] # Strictly defining required inputs
)''', language='python')

# The actual code. Notice how we use the PromptTemplate class directly, passing the string AND a list telling it exactly what to expect.
# If it expects 'data_type' and 'source_text', and doesn't get both later, it will forcefully block execution.
template = PromptTemplate(
    template="Extract the {data_type} from this text: '{source_text}'",
    input_variables=["data_type", "source_text"]
)

st.write("---")
st.write("### Try it out!")

# Provide a dropdown menu so the user can select an extraction type
data_type = st.selectbox("What to extract:", ["Names", "Dates", "Locations"])
# Provide a multi-line text area for the user to provide the source block of text
source_text = st.text_area("Source Text:", "On July 4th, 1776, Thomas Jefferson was in Philadelphia.")

# Create a highly visible warning box on the UI
st.warning("Experiment: Try checking the box below to simulate a developer forgetting to pass the 'source_text' variable.")
# Create a checkbox. If clicked, this variable returns True.
simulate_error = st.checkbox("Intentionally omit 'source_text' to trigger validation error")

# The button triggers the workflow
if st.button("Extract Data"):
    # Try block catches errors so our whole app doesn't unexpectedly crash from the experiment
    try:
        if simulate_error:
            # If the box is checked, we purposely invoke the template passing ONLY one variable. It expects two.
            prompt = template.invoke({'data_type': data_type})
        else:
            # Standard flow: pass all required parameters securely
            prompt = template.invoke({'data_type': data_type, 'source_text': source_text})
            
        with st.spinner("Connecting to Gemini..."):
            # Call the AI model
            result = model.invoke(prompt)
            # Make sure we print the text returned to the screen
            st.success(result.content)
            
    # If standard LangChain validation fails (because we omitted something required)
    except Exception as e:
        # Display the red error directly in the UI for the user to learn from
        st.error(f"🚨 LANGCHAIN ERROR CAUGHT: {e}")
        # Append a footnote to the error
        st.markdown("*Notice how it safely prevented the AI call because a required variable was missing.*")

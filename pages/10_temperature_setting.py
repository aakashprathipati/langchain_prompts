# Import Streamlit for fast UI interactions
import streamlit as st
# Import generative models representing AI back-ends
from langchain_google_genai import ChatGoogleGenerativeAI
# Import loader to initialize external variables
from dotenv import load_dotenv

# Ensure secrets load properly
load_dotenv()

# Setup primary tabs parameters
st.set_page_config(page_title="10. Temperature Setting", layout="wide")
# Page Header
st.title("📚 10. AI Temperature (Creativity)")

# Explaining thoroughly what LLM Temperature equates to 
st.info("""
**What is this?** The `temperature` parameter controls the creativity or randomness of the AI model.
- **Low (0.0 - 0.3):** Deterministic, factual, repetitive. Usually best for extracting data.
- **Medium (0.4 - 0.7):** Conversational, standard behavior. 
- **High (0.8 - 2.0+):** Highly creative, wildly different each run, sometimes chaotic behavior.
""")

st.write("### Try it out! Let's generate a Poem!")

# Let's map a visual Slider to the UI. The variable 'temp_value' dynamically changes whenever a user drags the bar left or right!
# Max limits are defined explicitly for floating point constraints
temp_value = st.slider("Select Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)

st.write("### Code Implementation:")
# Show what that dynamically changes in the code below via an f-string parsing the temp_value!
st.code(f'''model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature={temp_value})
result = model.invoke("Write a 5 line poem about cricket.")''', language='python')

st.write("---")

# Render Generate button
if st.button("Generate Poem"):
    # Wait, we need to Re-initialize the model! 
    # Because we are dynamically allowing the user to pick a new temperature natively, we must re-bind ChatGoogleGenerativeAI 
    # using the parameter `temperature=temp_value` to force the updated constraints!
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=temp_value)
    
    # Process the loading animation
    with st.spinner("Connecting to Gemini..."):
        # We simply invoke a standard static prompt string since the variable in question affects the Model, not the String!
        result = model.invoke("Write a 5 line poem about cricket.")
        # Surface the generated text response! 
        # HINT: High temperatures usually cause rhyming chaos!
        st.success(result.content)

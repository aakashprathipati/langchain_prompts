# Import Streamlit for interface components
import streamlit as st
# Import generative model handler
from langchain_google_genai import ChatGoogleGenerativeAI
# Import the specialized 'load_prompt' helper function from LangChain 
# This scans for formatted JSON templates on disk and automatically parses them!
from langchain_core.prompts import load_prompt
# Import environment loading scripts
from dotenv import load_dotenv

# Execute it so Keys load properly
load_dotenv()
# Bind our model object
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Adjust properties
st.set_page_config(page_title="9. Loading Prompts", layout="wide")
# Main header
st.title("📚 9. Loading Prompts & Piping (LCEL)")

# Description of the LCEL phenomenon 
st.info("""
**What is this?** This script serves as the UI for the prompt we saved in the previous script. We use `load_prompt` to grab the JSON file, and then we use LangChain Expression Language (LCEL) passing it as `chain = template | model`.
""")

st.write("### Code Implementation:")
# Add code example of LCEL Piping functionality
st.code('''template = load_prompt('template.json')

# Pipe the template output DIRECTLY into the model
chain = template | model

result = chain.invoke({'paper_input': paper, 'style_input': style, 'length_input': length})''', language='python')

st.write("---")

# Safety try-catch block wrapping the actual loading logic just in case the file doesn't exist
try:
    # Use load_prompt to target the JSON file that exists in the root directory!
    # This automatically instantiates a fully functional PromptTemplate without writing any code!
    template = load_prompt('template.json')
    # Label saying where it was pulled from
    st.write("**Loaded strictly from `template.json`:**")
    # Display the literal string embedded inside the JSON class
    st.text(template.template)
    
    # Let's map 3 horizontal columns to simulate UI parameters we intend to pass along
    col1, col2, col3 = st.columns(3)
    with col1:
        # A dropdown binding 'paper_input' variable with 4 popular subjects
        paper_input = st.selectbox("Research Paper", ["Attention Is All You Need", "BERT", "GPT-3", "Diffusion Models Beat GANs"])
    with col2:
        # A dropdown binding 'style_input' with standard audience ranges
        style_input = st.selectbox("Style", ["Beginner-friendly", "Code-Oriented", "Mathematical"])
    with col3:
        # A dropdown requesting a rough output size bound to 'length_input'
        length_input = st.selectbox("Length", ["Short (1 paragraph)", "Medium", "Long (detailed)"])
        
    # Render execution button
    if st.button("Summarize (Run Chain)"):
        
        # NOTE: THIS IS LCEL PIPING.
        # It's unique syntax to LangChain where the vertical bar ( | ) basically means "PASS RESULT TO".
        # We tell the system: take our loaded `template` object, and PASS IT natively to the `model` object. 
        # `chain` now represents an unbroken execution sequence without creating intermediate 'prompt_text = ...' variables! 
        chain = template | model
        
        # Send processing notification
        with st.spinner("Connecting to Gemini using LCEL piping..."):
            
            # Now we use `.invoke` on the unified CHAIN, passing only the dictionary of variables.
            # The Template receives the variables, parses them, constructs the string, and automatically hands it to the Model immediately!
            result = chain.invoke({
                'paper_input': paper_input,
                'style_input': style_input,
                'length_input': length_input
            })
            
            # Draw AI returned text stream to the screen beautifully
            st.success(result.content)
            
# A failsafe triggered because `load_prompt` crashed if it couldn't find the .json
except Exception as e:
    st.error(f"Cannot load template.json! Make sure you didn't accidentally delete the file. Error: {e}")

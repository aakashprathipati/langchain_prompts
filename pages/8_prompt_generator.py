# Import web GUI library
import streamlit as st
# Import standard dynamic string PromptTemplate
from langchain_core.prompts import PromptTemplate
# Import standard JSON writing/reading utility inherent to python
import json

# Initialize window titles
st.set_page_config(page_title="8. Prompt Generator & Saving", layout="wide")
# Set header
st.title("📚 8. Saving Prompts to Disk")

# Give context as to what we are trying to achieve
st.info("""
**What is this?** Sometimes you have a massive, highly structured PromptTemplate. Instead of hardcoding it into your UI app, you can construct it in a separate Python script, save it to a `.json` file, and load it from anywhere.
""")

st.write("### Code Implementation:")
# Embed code to visually display the .save functionality
st.code('''template = PromptTemplate(
    template="Summarize this paper \\"{paper_input}\\" in {style_input} style.",
    input_variables=['paper_input', 'style_input']
)
# PromptTemplate objects inherently contain a .save() function natively!
template.save('template.json')''', language='python')

st.write("---")
st.write("### Try it out! Create your Template File!")
# Expose a very large text-area meant to simulate a complex, multi-paragraph prompt template being built by a developer
custom_prompt_text = st.text_area("Define your Large Prompt Template String", "Please summarize the research paper titled '{paper_input}' using a {style_input} explanation style.")
# Because LangChain mapping is strict, we need them to explicitly type out a comma-list of variables they expect inside that template above!
variables_input = st.text_input("Comma-separated variables:", "paper_input, style_input")

# A button checking to see if they want to physically write this to their hard-drive
if st.button("Save this Template to 'custom_template.json'"):
    # We use a quick python list expression: separate the string array by Commas, and strip the whitespace off any of those separated segments! 
    # Example: 'Hello, World' creates ['Hello', 'World']
    variables_list = [v.strip() for v in variables_input.split(',')]
    try:
        # We explicitly configure a new class instance
        template = PromptTemplate(
            template=custom_prompt_text, # Passed string
            input_variables=variables_list, # Passed comma-separated validation list
            validate_template=True # Double checks if they made a mistake matching variables to placeholders
        )
        # Execute the native file writing mechanic. 
        # This will create a local 'custom_template.json' payload inside the directory containing the prompt instructions!
        template.save('custom_template.json')
        # Notify the user it was safely saved!
        st.success("Successfully saved to `custom_template.json`!")
        
        # Read the file we just created right back off the disk momentarily to prove we did it!
        with open('custom_template.json', 'r') as f:
            # We pass the JSON string read from the file to the browser renderer to be displayed clearly
            st.json(json.load(f))
    # Failsafe in case they formatted their string variables improperly!
    except Exception as e:
        # Displays the red error box directly explaining their failure
        st.error(f"Error creating template: {e}")

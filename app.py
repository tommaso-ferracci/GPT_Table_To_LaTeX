import os
import streamlit as st
from io import StringIO
from rebuff import Rebuff
from utils import get_completion
from utils import count_tokens
from utils import convert_to_latex
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.buy_me_a_coffee import button

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
rb = Rebuff(api_token=st.secrets['REBUFF_API_KEY'])
st.title("Convert CSV to $\LaTeX$ with ChatGPT")
st.write("Please upload your CSV file below.")
uploaded_file = st.file_uploader(".", label_visibility="collapsed")

if uploaded_file is not None:
    data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
    delimiter = "####"
    context = []
    system_message = f"""
    Your task is to convert the following text, delimited by {delimiter}, into a LaTeX table. 
    Return only the LaTeX code needed for the table. By default, round all floats to 2 decimal places unless the start with 0.00, in which case round them 
    to the first non-null digit. By default, leave integers as they are. By default, center and separate all columns. By default, use \hline at the beginning and end of
    the table. By default, use \hline after the header. Remember to close all environments.
    {delimiter}{data}{delimiter} 
    The user might prompt you with personal stylistic preferences. Remember to always output only LaTeX code.
    """
    context.append({"role": "system", "content": system_message})
    num_tokens = count_tokens(context)

    if num_tokens > 4096:
        st.write(f"Table is too long. GPT-3.5-turbo supports up to 4096 tokens, while your prompt requires {num_tokens} tokens.")
    else:
        st.write("Converting... this might take a minute...")
        result = convert_to_latex(context)
        st.code(result, language='latex')

        satisfaction = selectbox("Are you satisfied with the result?", ['Yes', 'No'], no_selection_label="")

        if satisfaction == 'Yes':
            st.write("*Using the GPT-3.5-turbo API costs money. If you want to help keep the project free:*")
            button(username='risiandbisi', floating=False, width=220)
        elif satisfaction == 'No': 
            user_input = st.text_input("Please provide specific stylistic preferences:", "")

            if user_input == "":
                st.stop()
            else:
                _, is_injection = rb.detect_injection(user_input)

            if is_injection:
                st.write("It looks like you are attempting a prompt injection. Please provide only specific stylistic preferences.")
            else:
                result = convert_to_latex(context, user_input)
                st.code(result, language='latex')
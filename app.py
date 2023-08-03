import os
import streamlit as st
from io import StringIO
from utils import get_completion
from utils import convert_to_latex
from streamlit_extras.buy_me_a_coffee import button

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

st.title("Convert CSV to $\LaTeX$ with ChatGPT")

st.write("Please upload your CSV file below.")

uploaded_file = st.file_uploader("Upload a CSV")

if uploaded_file is not None:

    data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()

    st.write("Converting... this might take a minute...")

    result = convert_to_latex(data)

    if type(result) != str:
        st.write(f"Table is too long. GPT-3.5-turbo supports up to 4096 tokens, while your prompt requires {result} tokens.")
    else:
        st.code(result, language='latex')

        st.write("*Using the GPT-3.5-turbo API costs money. If you are satisfied with the result and want to help keep the project free, consider donating a coffee:*")

        button(username="risiandbisi", floating=False, width=221)
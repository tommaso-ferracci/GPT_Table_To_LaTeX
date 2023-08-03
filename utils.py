import openai
import tiktoken

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0): 
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message["content"]

def convert_to_latex(data):

    delimiter = "####"

    prompt = f"""
    Your task is to convert the following text, delimited by {delimiter}, into a LaTeX table. 
    Return only the LaTeX code needed for the table. By default, round all floats to 2 decimal places unless the start with 0.00, in which case round them 
    to the first non-null digit. Leave integers as they are. By default, center and separate all columns. By default, use \hline at the beginning and end of
    the table. By default, use \hline after the header. Remember to close all environments.
    {delimiter}{data}{delimiter} 
    """

    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(tokenizer.encode(prompt))

    if num_tokens < 4096:
        return get_completion(prompt)
    else:
        return num_tokens
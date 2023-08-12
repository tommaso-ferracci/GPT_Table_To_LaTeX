import openai
import tiktoken

def get_completion(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message["content"]

def count_tokens(messages):
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(tokenizer.encode(messages[0]["content"]))
    return num_tokens

def convert_to_latex(messages, user_input=None):
    if user_input == None:
        return get_completion(messages)
    else:
        messages.append({"role": "user", "content": user_input})
        response = get_completion(messages)
        messages.append({"role": "assistant", "content": response})
        return response
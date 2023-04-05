import os
import glob
import importlib
import ipywidgets as widgets
from IPython.display import display, clear_output
import openai

# This function finds all the ".txt" files in the "system_prompts/starting_contexts" directory
# and returns their contents as a list of strings.
def load_starting_contexts(dir_path):
    starting_context_files = glob.glob(os.path.join(dir_path, "*.txt"))
    starting_contexts = []
    for file_path in starting_context_files:
        with open(file_path, "r") as file:
            starting_contexts.append(file.read())
    return starting_contexts

# This function generates a system prompt by concatenating the specified string
# with the contents of the specified file.
def generate_system_prompt(prompt_string, starting_context_file):
    with open(starting_context_file, "r") as file:
        starting_context = file.read()
    return f"{prompt_string} {starting_context}"

# This function sends an API call to OpenAI's Chat API with the specified chat history.
def send_api_call(chat_history):
    model = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model,
        messages=chat_history,
        max_tokens=150,
        temperature=0,
    )
    return response

def display_starter_contexts(system_prompt):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    starting_contexts_dir = os.path.join(file_dir, "..", "system_prompts", "starting_contexts")
    starting_context_files = glob.glob(os.path.join(starting_contexts_dir, "*.txt"))
    starting_contexts = [os.path.splitext(os.path.basename(file))[0].replace("_", " ").replace("-", " ") for file in starting_context_files]
    button_layout = widgets.Layout(width='auto', margin='5px')
    buttons = [widgets.Button(description=context[:20] + '...', layout=button_layout) for context in starting_contexts]
    button_box = widgets.VBox(children=buttons)

    def on_button_click(button):
        index = buttons.index(button)
        starting_context_file = starting_context_files[index]
        with open(starting_context_file, "r") as file:
            starting_context = file.read()
        system_prompt_with_context = f"{system_prompt}\n\n{starting_context}"
        initial_system_message = {"role": "system", "content": system_prompt_with_context}

        # New code to display the starter prompt in the output widget
        output_widget = widgets.Output()
        display(output_widget)
        with output_widget:
            display(widgets.HTML(value=f"<p>{starting_context}</p>"))
        # End of new code

        display_new_form([initial_system_message], starting_context=os.path.splitext(os.path.basename(starting_context_file))[0])


    for button, file in zip(buttons, starting_context_files):
        button.description = os.path.splitext(os.path.basename(file))[0].replace("_", " ").replace("-", " ")
        button.on_click(lambda x: on_button_click(x))

    display(button_box)


import pprint
import re
import re

def display_chat_response(output_widget, input_widget, send_button, chat_history):
    with output_widget:
        clear_output()
        display(widgets.Label(value="⏳ Please wait..."))
    massage_prompt = "Always include the sentiment analysis and then --- and then your response.  The customer's question is:\n\n"
    
    # Check if input_widget is not None before appending the user message
    if input_widget is not None:
        chat_history.append({"role": "user", "content": massage_prompt + input_widget.value.strip()})
    else:
        chat_history.append({"role": "user", "content": massage_prompt})
    
    if input_widget is not None:
        input_widget.disabled = True
    send_button.disabled = True
    send_button.close()
    response = send_api_call(chat_history)

    # Extract sentiment analysis and the main message
    content = response["choices"][0]["message"]["content"]
    delimiter = "---"
    parts = content.split(delimiter, 1)
    sentiment_analysis = parts[0].strip() if len(parts) > 1 else ""
    main_message = parts[-1].strip()

    chat_history.append({"role": "assistant", "content": main_message})

    # Display the main message
    with output_widget:
        clear_output()
        display(widgets.HTML(value=f"<p>{main_message}</p>"))

    # Extract token information from the API response
    prompt_tokens = response['usage']['prompt_tokens']
    completion_tokens = response['usage']['completion_tokens']
    total_tokens = response['usage']['total_tokens']

    # Display token information
    display(widgets.HTML(value=f'<p style="font-family:monospace; font-size:small; color:gray; margin-bottom: 0;">{sentiment_analysis}<br/>Prompt tokens: {prompt_tokens}<br>Response tokens: {completion_tokens}<br>Total tokens: {total_tokens}</p>'))

    display_new_form(chat_history)

# This function handles the send button click event.
def send_message_handler(output_widget, input_widget, send_button, chat_history):
    if input_widget is None or not input_widget.disabled:
        display_chat_response(output_widget, input_widget, send_button, chat_history)

# This function displays the chat form with an optional initial message.
def display_new_form(chat_history=None, starting_context=None):
    if chat_history is None:
        chat_history = []
    
    if starting_context is not None and "popup" in starting_context:
        input_field = None
    else:
        input_field = widgets.Text(
            placeholder='Enter your message...',
            layout=widgets.Layout(width='100%')
        )
    
    send_button = widgets.Button(
        description='Send',
        button_style='success'
    )
    output_widget = widgets.Output()
    
    if input_field:
        display(input_field, send_button, output_widget)
    else:
        display(send_button, output_widget)
    
    if input_field:
        send_button.on_click(lambda x: send_message_handler(output_widget, input_field, send_button, chat_history))
        input_field.on_submit(lambda x: send_message_handler(output_widget, input_field, send_button, chat_history))
    else:
        send_button.on_click(lambda x: send_message_handler(output_widget, None, send_button, chat_history))



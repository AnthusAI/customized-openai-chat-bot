import os
import openai
import ipywidgets as widgets
from IPython.display import display, clear_output

def send_api_call(chat_history):
    model = "gpt-3.5-turbo"  # Choose the model you want to use

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model=model,
        messages=chat_history,
        max_tokens=150,
        temperature=0.5,
    )

    return response.choices[0].message['content'].strip()

def display_chat_response(output_widget, input_widget, send_button, chat_history):
    with output_widget:
        clear_output()
        display(widgets.Label(value="⏳ Please wait..."))

    chat_history.append({"role": "user", "content": input_widget.value.strip()})

    input_widget.disabled = True
    send_button.disabled = True
    send_button.close()

    response = send_api_call(chat_history)
    chat_history.append({"role": "assistant", "content": response})

    with output_widget:
        clear_output()
        display(widgets.HTML(value=f"<p>{response}</p>"))

    display_new_form(chat_history)

def send_message_handler(output_widget, input_widget, send_button, chat_history):
    if not input_widget.disabled:
        display_chat_response(output_widget, input_widget, send_button, chat_history)

def display_new_form(chat_history):
    input_field = widgets.Text(
        placeholder='Enter your message...',
        layout=widgets.Layout(width='100%')
    )

    send_button = widgets.Button(
        description='Send',
        button_style='success'
    )

    output_widget = widgets.Output()

    display(input_field, send_button, output_widget)

    send_button.on_click(lambda x: send_message_handler(output_widget, input_field, send_button, chat_history))
    input_field.on_submit(lambda x: send_message_handler(output_widget, input_field, send_button, chat_history))


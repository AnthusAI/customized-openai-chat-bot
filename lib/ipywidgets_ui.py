import ipywidgets as widgets
from IPython.display import display, clear_output
import time

# Suppress a deprecation warning.
# More info: https://github.com/jupyter-widgets/ipywidgets/issues/2446
import warnings

def simulate_api_call():
    time.sleep(3)
    response = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed malesuada turpis vel odio bibendum pretium. Donec sit amet vehicula enim."
    return response

def display_chat_response(output_widget, input_widget, send_button):
    with output_widget:
        clear_output()
        display(widgets.Label(value="⏳ Please wait..."))

    # Simulate API call
    response = simulate_api_call()

    # Update chat output with API response
    with output_widget:
        clear_output()
        display(widgets.HTML(value=f"<p>{response}</p>"))

    # Disable input field and send button
    input_widget.disabled = True
    send_button.disabled = True

    # Display the new form
    display_new_form()

def send_message_handler(output_widget, input_widget, send_button):
    if not input_widget.disabled:
        display_chat_response(output_widget, input_widget, send_button)

def display_new_form():
    # Create text input field
    input_field = widgets.Text(
        placeholder='Enter your message...',
        layout=widgets.Layout(width='100%')
    )

    # Create "Send" button
    send_button = widgets.Button(
        description='Send',
        button_style='success'
    )

    # Create output widget
    output_widget = widgets.Output()

    # Display input field, button, and output widget
    display(input_field, send_button, output_widget)

    # Call display_chat_response when the button is clicked
    send_button.on_click(lambda x: send_message_handler(output_widget, input_field, send_button))

    # Call display_chat_response when the Enter key is pressed in the input field
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        input_field.on_submit(lambda x: send_message_handler(output_widget, input_field, send_button))
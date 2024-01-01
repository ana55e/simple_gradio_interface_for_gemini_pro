import gradio as gr
import google.generativeai as genai
import PIL
genai.configure(api_key='enter your gemini api')  # Replace with your API key
history = []  

def generate_text(text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(text)
    return response.text

def generate_text_from_image(image, text):
    global history
    model = genai.GenerativeModel('gemini-pro-vision')
    image = PIL.Image.fromarray(image.astype('uint8'), 'RGB')
    history.append(("User", text))
    response = model.generate_content([text, image])
    history.append(("Bot", response.text))
    return response.text,history


def interactive_chat(message, chat_history=None):
    if chat_history is None:
        chat_history = []
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat()
    response = chat.send_message(message)
    chat_history.append(("User", message))
    chat_history.append(("Bot", response.text))
    return chat_history

# Creating interfaces for each function
text_interface = gr.Interface(
    fn=generate_text,
    inputs=gr.inputs.Textbox(label="Enter text"),
    outputs=gr.outputs.Textbox(label="Generated Text")
)

image_interface = gr.Interface(
    fn=generate_text_from_image,
    inputs=[gr.inputs.Image(label="Upload Image"), gr.inputs.Textbox(label="Enter text")],
    outputs=[gr.outputs.Textbox(label="Generated Text"), gr.outputs.Textbox(label="Chat History", type="text")]
)

chat_interface = gr.Interface(
    fn=interactive_chat,
    inputs=gr.inputs.Textbox(label="Chat with the bot"),
    outputs=gr.outputs.Chatbot(label="Chatbot Response")
)

# Launching all interfaces together in a tabbed view
iface = gr.TabbedInterface([text_interface, image_interface, chat_interface])
iface.launch()
# share=True to share your interface publicly

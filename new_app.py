import gradio as gr
import google.generativeai as genai
import PIL

# Replace with your API key
genai.configure(api_key='Enter your authentification tokens')

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
    return response.text, history

def interactive_chat(message, chat_history=None):
    if chat_history is None:
        chat_history = []
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat()
    response = chat.send_message(message)
    chat_history.append(("User", message))
    chat_history.append(("Bot", response.text))
    return chat_history



# Using the specified Gradio theme
theme =theme = gr.themes.Soft()

# Creating interfaces with the specified theme
text_interface = gr.Interface(
    fn=generate_text,
    inputs=gr.components.Textbox(label="Enter text"),
    outputs=gr.components.Textbox(label="Generated Text"),
    theme=theme
)

image_interface = gr.Interface(
    fn=generate_text_from_image,
    inputs=[gr.components.Image(label="Upload Image"), gr.components.Textbox(label="Enter text")],
    outputs=[gr.components.Textbox(label="Generated Text"), gr.components.Textbox(label="Chat History", type="text")],
    theme=theme
)

chat_interface = gr.Interface(
    fn=interactive_chat,
    inputs=gr.components.Textbox(label="Chat with the bot"),
    outputs=gr.components.Chatbot(label="Chatbot Response"),
    theme=theme
)

# Launching all interfaces together in a tabbed view
iface = gr.TabbedInterface(
    [text_interface, image_interface, chat_interface],
    tab_names=["Text", "Image", "Chat"],
    theme=theme
)
iface.launch(share=True,server_port=7865) # you can change this parametres

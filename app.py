import gradio as gr
from main import chat

# gr.ChatInterface handles history automatically.
# Your function just needs to return the bot's reply as a string.
def respond(message, history, language, native, level, mode):
    return chat(message, history, language, native, level, mode)

demo = gr.ChatInterface(
    fn=respond,
    additional_inputs=[
        gr.Textbox(value="German",  label="Language to Learn"),
        gr.Textbox(value="English", label="Native Language"),
        gr.Dropdown(["A1/A2", "B1/B2", "C1/C2"], value="A1/A2", label="Level"),
        gr.Dropdown(["learn", "practice", "test", 'Dictionary'],  value="Dictionary",   label="Mode"),
    ],
    title="Your Language Tutor",
    description="Learn, practice, and test languages interactively.",
)

demo.launch()

# close the model connection when the app is closed
def on_close():
    print("App is closing. Cleaning up resources...")
    
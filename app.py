import gradio as gr
from main import chat

def respond(message, history, language, native, level, mode):
    reply = chat(message, history, language, native, level, mode)

    # Build history in dict format that gr.Chatbot expects
    history = history + [
        {"role": "user",      "content": message},
        {"role": "assistant", "content": reply},
    ]

    return "", history, history   # clear textbox | update chatbot | save state

with gr.Blocks(title="Your Language Tutor") as demo:
    gr.Markdown("# 🌍 Your Language Tutor")
    gr.Markdown("Learn, practice, and test languages interactively.")

    with gr.Row():
        # LEFT SIDE → Chat
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="Tutor")
            msg     = gr.Textbox(label="Your Message")
            history = gr.State([])

        # RIGHT SIDE → Settings Panel
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Learning Settings")
            language = gr.Textbox(value="German",  label="Language to Learn")
            native   = gr.Textbox(value="English", label="Native Language")
            level    = gr.Dropdown(["A1/A2", "B1/B2", "C1/C2"], value="A1/A2",      label="Level")
            mode     = gr.Dropdown(["learn", "practice", "test", "Dictionary"],      label="Mode", value="Dictionary")

    msg.submit(
        respond,
        inputs=[msg, history, language, native, level, mode],
        outputs=[msg, chatbot, history]
    )

demo.launch()
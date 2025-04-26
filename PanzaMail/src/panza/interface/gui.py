from panza.entities.instruction import EmailInstruction, Instruction
from panza.writer import PanzaWriter
import gradio as gr
import json


class PanzaGUI:
    def __init__(self, writer: PanzaWriter, **kwargs):
        self.writer = writer

        with gr.Blocks(css=self.custom_css()) as panza:
            with gr.Column(elem_classes="main-container"):
                gr.Markdown("### <span class='title'>PANZA WRITER 🐉</span>", elem_id="title")
                gr.Markdown("<span class='subtitle'>Let Panza write email for you, tailored to your unique style become more professional!</span>", elem_id="subtitle")

                with gr.Row(elem_classes="content-box"):
                    with gr.Column():
                        gr.Markdown("**Tell us about your email**")
                        inputbox = gr.Textbox(
                            placeholder="Example: Write an email planning an epic trip with friends",
                            lines=10,
                            elem_id="inputbox"
                        )
                    with gr.Column():
                        gr.Markdown("**Email result**")
                        outputbox = gr.Textbox(
                            placeholder="Your email content will appear here...",
                            lines=10,
                            interactive=False,
                            elem_id="outputbox" 
                        )
                # Generate button functionality
                gr.Button("Generate ➜", elem_id="generate-btn").click(
                    self.get_execute(), inputs=[inputbox], outputs=[outputbox]
                )
                # Copy button functionality
                def copy_to_clipboard(text):
                    return text
                gr.Button("Copy to Clipboard", elem_id="copy-btn").click(
                    fn=copy_to_clipboard,
                    inputs=[outputbox],
                    outputs=[],
                    js="async (text) => { await navigator.clipboard.writeText(text); alert('Copied to clipboard!'); }"
                )

        panza.queue().launch(server_name="localhost", server_port=5002, share=True)

    def get_execute(self):
        def execute(input):
            instruction: Instruction = EmailInstruction(input)
            stream = self.writer.run(instruction, stream=True)
            output = ""
            for chunk in stream:
                try:
                    # Ensure proper JSON encoding/decoding
                    if isinstance(chunk, str):
                        chunk = json.loads(json.dumps(chunk))
                    output += str(chunk)
                except json.JSONDecodeError:
                    output += str(chunk)
                yield output
        return execute


    def custom_css(self):
        return """
        body {
            background-color: #1f1f1f;
        }
        #title {
            text-align: center;
            font-size: 2.5rem;
            font-family: 'Orbitron', sans-serif;
            color: #bb6bff;
            margin-top: 20px;
        }
        #subtitle {
            text-align: center;
            font-size: 1rem;
            color: #ccc;
            margin-bottom: 20px;
        }
        .main-container {
            max-width: 900px;
            margin: auto;
            padding: 20px;
        }
        .content-box {
            background: linear-gradient(145deg, #2b2b2b, #1a1a1a);
            border-radius: 25px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(187, 107, 255, 0.4);
        }
        #inputbox, #outputbox {
            border-radius: 10px;
            background-color: #333;
            color: #eee;
            border: 1px solid #555;
        }
        #generate-btn {
            background: linear-gradient(to right, #bb6bff, #ff6bcb);
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 10px 30px;
            margin: 20px auto;
            display: block;
            transition: all 0.3s ease;
        }
        #generate-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px #bb6bff;
        }
        #copy-btn {
            background: linear-gradient(to right, #6bafff, #6bffcb);
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 10px 30px;
            margin: 10px auto;
            display: block;
            transition: all 0.3s ease;
        }
        #copy-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px #6bafff;
        }
        """




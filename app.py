import os
from loader import load_vectorstore
from utils import get_best_answer
import gradio as gr
import shutil


def ask_rag_assistant(pdf, question, dev_mode=False):
    if pdf is None or question.strip() == "":
        return "❌ Please upload a PDF and enter a question."

    if dev_mode:
        return f"🧪 [Dev Mode] Would answer: '{question}'", "boo"

    try:
        # Get filename and path
        filename = os.path.basename(pdf)
        save_path = os.path.join("documents", filename)

        # Copy uploaded file to documents folder if needed
        if os.path.abspath(pdf) != os.path.abspath(save_path):
            shutil.copy(pdf, save_path)

        # Load vectorstore and answer
        vectorstore, split_docs = load_vectorstore(filename)
        answer = get_best_answer(question, vectorstore, split_docs)
        return answer, "✅ Answer generated successfully."

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Gradio UI
demo = gr.Blocks(css="""
    #title {
        text-align: center;
        font-size: 22px;
        color: #2c3e50;
        margin-bottom: 10px;
    }

    .gr-button {
        font-weight: bold;
        background-color: #4CAF50;
        color: white;
    }

    #title-row {
        justify-content: center;
        align-items: center;
        display: flex;
        gap: 10px;
        margin-bottom: 10px;
    }

    #answer-row {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-top: 20px;
    }

    #answer-bubble {
        background-color: #f0f0f0;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #ccc;
        max-width: 80%;
        font-size: 15px;
        line-height: 1.5;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.05);
    }
""")

with demo:
    with gr.Column():
        with gr.Row(elem_id="title-row"):
            # gr.Image("static/popavatar.jpg", width=70, show_label=False, show_download_button=False)
            gr.Markdown("### <div id='title'>Ghazal's AI Research Assistant</div>")

        gr.Markdown("---")

        pdf_input = gr.File(label="📄 Upload your PDF", file_types=[".pdf"])
        question_input = gr.Textbox(label="🔎 Ask a question", placeholder="e.g. What is the conclusion?", lines=2)
        dev_toggle = gr.Checkbox(label="🧪 Dev Mode (skip API)", value=False)
        submit_btn = gr.Button("Get Answer")

        # 🧠 Answer shown as avatar + speech bubble
        with gr.Row(elem_id="answer-row"):
            gr.Image("static/popavatar.jpg", width=70, show_label=False, show_download_button=False)
            answer_output = gr.Markdown(elem_id="answer-bubble")

        status_label = gr.Label()

        submit_btn.click(
            ask_rag_assistant,
            inputs=[pdf_input, question_input, dev_toggle],
            outputs=[answer_output, status_label]
        )


demo.launch()
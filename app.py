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


#gradio UI
demo = gr.Blocks(css="""  # ← One single CSS declaration
#layout {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    padding: 30px;
    gap: 12px;
    font-family: 'Segoe UI', sans-serif;
}

#avatar {
    width: 70px;
    border-radius: 12px;
}

#right-col {
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex: 1;
}

#speech {
    background-color: #f0f0f0;
    padding: 16px 18px;
    border-radius: 12px;
    border: 1px solid #ccc;
    position: relative;
    font-size: 15px;
    line-height: 1.5;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.05);
    min-height: 60px;
}

#speech::before {
    content: "";
    position: absolute;
    top: 18px;
    left: -10px;
    width: 0;
    height: 0;
    border-top: 10px solid transparent;
    border-right: 10px solid #f0f0f0;
    border-bottom: 10px solid transparent;
}

#question-box textarea {
    height: 40px !important;
    font-size: 15px;
    padding: 8px 10px;
}

#input-row {
    display: flex;
    gap: 10px;
}

#upload-btn .gr-file {
    height: 36px !important;
    width: 120px !important;
    font-size: 13px;
    padding: 2px 6px !important;
    background-color: #eaeaea;
}

.gr-button {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
    height: 40px;
    padding: 0 16px;
}
""")  # ✅ End of CSS

with demo:  # 👈 No need to re-declare gr.Blocks
    with gr.Row(elem_id="layout"):
        gr.Image("static/avatar.png", elem_id="avatar", show_label=False)

        with gr.Column(elem_id="right-col"):
            answer_output = gr.Markdown("💬 Ask me something about your research paper!", elem_id="speech")
            question_input = gr.Textbox(label="", placeholder="Ask a question...", lines=1, elem_id="question-box")

            with gr.Row(elem_id="input-row"):
                pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"], elem_id="upload-btn")
                submit_btn = gr.Button("Get Answer")
                dev_toggle = gr.Checkbox(label="🧪 Dev Mode", value=False)

        def run_assistant(pdf, question, dev_mode):
            result = ask_rag_assistant(pdf, question, dev_mode)
            return result if isinstance(result, str) else result[0]

        submit_btn.click(
            fn=run_assistant,
            inputs=[pdf_input, question_input, dev_toggle],
            outputs=answer_output
        )

demo.launch()

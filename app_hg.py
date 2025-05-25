import os
import shutil
import gradio as gr
from loader import load_vectorstore
from utils import get_best_answer
from llm_provider import get_llm
from config import OPENAI_MODEL, HF_MODEL


GPT_PASSWORD = os.getenv("GPT_ACCESS_PASSWORD")


def ask_rag_assistant(pdf, question, history, dev_mode, selected_model, password):
    if pdf is None or question.strip() == "":
        return "❌ Please upload a PDF and enter a question.", history or "", "⚠️ No file uploaded."

    if selected_model == "openai" and password != GPT_PASSWORD:
        return "🔒 Incorrect or missing password for GPT usage.", history or "", "❌ Access denied"

    filename = os.path.basename(pdf)

    if dev_mode:
        fake_answer = f"🧪 [Dev Mode] Would answer: '{question}'"
        new_turn = f"\n\n**❓ You:** {question}\n\n**🧠 Assistant:** {fake_answer}\n"
        updated_history = (history or "") + new_turn
        return fake_answer, updated_history, f"📄 Uploaded: `{filename}`"

    try:
        save_path = os.path.join("documents", filename)
        if os.path.abspath(pdf) != os.path.abspath(save_path):
            shutil.copy(pdf, save_path)

        # Inject runtime LLM backend
        os.environ["LLM_BACKEND"] = selected_model

        vectorstore, split_docs = load_vectorstore(filename)
        answer = get_best_answer(question, vectorstore, split_docs)

        new_turn = f"\n\n**❓ You:** {question}\n\n**🧠 Assistant:** {answer}\n"
        updated_history = (history or "") + new_turn

        return answer, updated_history, f"📄 Uploaded: `{filename}`"

    except Exception as e:
        return f"⚠️ Error: {str(e)}", history or "", f"📄 Error loading `{filename}`"


def clear_all():
    return (
        "💬 Ask me something about your research paper!",
        "",
        None,
        "",
        "No file uploaded.",
        "openai",
        ""
    )

def toggle_submit_btn(file, question):
    disabled = file is None or not question.strip()
    return gr.update(interactive=not disabled)

# ──────────────────────────────
# Gradio UI

demo = gr.Blocks(css="""
#layout {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    padding: 24px;
    gap: 16px;
    max-width: 1200px;
    margin: auto;
}
#left-col {
    width: 120px;
    flex-shrink: 0;
    display: flex;
    justify-content: center;
}
#avatar {
    width: 300px;
    height: 600px;
    border-radius: 12px;
    position: sticky;
    top: 10px;
}
#speech {
    background-color: #f0f4ff;
    padding: 20px 24px;
    border-radius: 16px;
    border: 1px solid #d6e0f5;
    font-size: 18px;
    font-weight: 600;
    line-height: 1.7;
    box-shadow: 2px 4px 10px rgba(0,0,0,0.05);
    font-family: 'Segoe UI', sans-serif;
    min-height: 100px;
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
#speech, #speech * {
    font-size: 18px !important;
    font-weight: 600 !important;
    font-family: 'Segoe UI', sans-serif !important;
    line-height: 1.7 !important;
}
#question-box textarea {
    height: 40px !important;
    font-size: 15px;
    padding: 8px 10px;
}
#input-row {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-top: 12px;
}
#upload-btn .gr-file {
    height: 40px !important;
    width: 130px !important;
    font-size: 13px;
    padding: 6px 10px !important;
    background-color: #e0e0e0;
    border-radius: 8px;
    border: 1px solid #ccc;
}
#question-box textarea {
    height: 40px !important;
    font-size: 15px;
    padding: 8px 12px;
    border-radius: 8px;
    flex: 1;
}
#submit-btn, #clear-btn {
    height: 40px;
    padding: 0 14px;
    font-size: 14px;
    font-weight: 600;
    border-radius: 8px;
}
#submit-btn {
    background-color: #4a90e2;
    color: white;
}
#clear-btn {
    background-color: #f5f5f5;
    color: #555;
}
#chat-thread {
    max-height: 400px;
    overflow-y: auto;
    padding: 16px;
    font-size: 14px;
    background-color: #fafafa;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    white-space: pre-wrap;
}
/* User messages */
.message.user {
    align-self: flex-end;
    background-color: #e6f0ff;
    color: #003366;
    padding: 10px 14px;
    border-radius: 16px 16px 4px 16px;
    max-width: 75%;
    font-weight: 500;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    margin-bottom: 4px;
}
/* Assistant messages */
.message.assistant {
    align-self: flex-start;
    background-color: #f2f2f2;
    color: #333;
    padding: 10px 14px;
    border-radius: 16px 16px 16px 4px;
    max-width: 75%;
    font-weight: 500;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    margin-bottom: 12px;
}
""")


with demo:
    with gr.Row(elem_id="layout"):
        with gr.Column(elem_id="left-col", scale=2):
            gr.Image("static/avatar.png", elem_id="avatar", show_label=False)

        with gr.Column(elem_id="right-col", scale=4):
            answer_output = gr.Markdown("💬 Ask me something about your research paper!", elem_id="speech")
            chat_history = gr.HTML(value="", elem_id="chat-thread")

            with gr.Row(elem_id="input-row"):
                pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"], elem_id="upload-btn")
                file_status = gr.Markdown("No file uploaded.", elem_id="file-status")

            with gr.Row(elem_id="input-row"):
                question_input = gr.Textbox(label="", placeholder="Ask a question...", lines=1, elem_id="question-box")

            with gr.Row(elem_id="input-row"):
                model_selector = gr.Dropdown(
                    label="Select Model",
                    choices=["openai", "huggingface"],
                    value="openai",
                    interactive=True,
                )
                password_box = gr.Textbox(
                    label="Password (for GPT)",
                    type="password",
                    placeholder="Enter password if using GPT",
                    visible=True,
                )

            with gr.Row(elem_id="input-row"):
                dev_toggle = gr.Checkbox(label="🧪 Dev Mode", value=False)
                submit_btn = gr.Button("Get Answer", interactive=False, elem_id="submit-btn")
                clear_btn = gr.Button("🧹 Clear All", variant="secondary", elem_id="clear-btn")

        # Pre-submit loading state
        def before_submit(question, history):
            return f"⏳ Thinking about: *{question}*", history, "💭 Thinking..."

        pdf_input.change(toggle_submit_btn, [pdf_input, question_input], [submit_btn])
        question_input.change(toggle_submit_btn, [pdf_input, question_input], [submit_btn])

        submit_btn.click(
            before_submit,
            inputs=[question_input, chat_history],
            outputs=[answer_output, chat_history, file_status]
        ).then(
            ask_rag_assistant,
            inputs=[pdf_input, question_input, chat_history, dev_toggle, model_selector, password_box],
            outputs=[answer_output, chat_history, file_status],
            show_progress=True
        )

        clear_btn.click(
            clear_all,
            inputs=[],
            outputs=[
                answer_output, chat_history, pdf_input, question_input,
                file_status, model_selector, password_box
            ]
        )

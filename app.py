import gradio as gr
import requests
from fastapi import FastAPI
import uvicorn
import threading

from app import app  # your FastAPI app


# 🔥 Run FastAPI in background
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)


threading.Thread(target=run_fastapi, daemon=True).start()


def run(pr_url):
    try:
        res = requests.get(
            "http://127.0.0.1:8000/review",
            params={"pr_url": pr_url},
            timeout=60
        )
        return res.json()["review"]
    except Exception as e:
        return f"❌ Error: {str(e)}"


custom_css = """
#app-container {
    max-width: 980px;
    margin: 0 auto;
    padding-top: 14px;
    padding-bottom: 22px;
}

#tool-subtitle {
    margin-top: -6px;
    margin-bottom: 10px;
    color: #52606d;
    font-size: 0.96rem;
}

#input-row {
    margin-top: 8px;
    margin-bottom: 12px;
    align-items: end;
}

#output-title {
    margin-top: 4px;
    margin-bottom: 8px;
}

#output-panel {
    min-height: 500px;
    border: 1px solid #d4dbe4;
    border-radius: 10px;
    padding: 18px;
    background: #f9fbfd;
    color: #1f2937;
    line-height: 1.55;
}

#output-panel, #output-panel * {
    color: #1f2937 !important;
}

#output-panel h1,
#output-panel h2,
#output-panel h3,
#output-panel h4 {
    color: #0f172a !important;
}

#output-panel pre {
    background: #eef2f7 !important;
    border: 1px solid #d8e0ea;
    border-radius: 8px;
    padding: 12px;
    overflow-x: auto;
}

#output-panel code {
    background: #edf2f7;
    color: #0f172a !important;
    border-radius: 4px;
    padding: 0.12rem 0.34rem;
}

#output-panel pre code {
    background: transparent;
    padding: 0;
}
"""


with gr.Blocks(title="Context-Aware PR Analyzer") as demo:

    with gr.Column(elem_id="app-container"):
        gr.Markdown("# Context-Aware PR Analyzer")

        gr.Markdown(
            "Analyze pull requests with focused checks for security, performance, and code quality. 🧭",
            elem_id="tool-subtitle",
        )

        with gr.Row(elem_id="input-row"):
            pr_url_input = gr.Textbox(
                label="GitHub PR URL",
                placeholder="https://github.com/org/repo/pull/123",
                scale=1,
            )
            analyze_button = gr.Button(
                "Analyze PR",
                variant="primary",
                min_width=150,
            )

        gr.Markdown("### Review Output", elem_id="output-title")

        review_output = gr.Markdown(
            value="Submit a pull request URL to generate a contextual review report.",
            elem_id="output-panel",
        )

        analyze_button.click(
            fn=run,
            inputs=pr_url_input,
            outputs=review_output,
            show_progress="full",
        )

        pr_url_input.submit(
            fn=run,
            inputs=pr_url_input,
            outputs=review_output,
            show_progress="full",
        )


demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    theme=gr.themes.Soft(),
    css=custom_css
)
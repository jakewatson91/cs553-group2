import gradio as gr
from huggingface_hub import InferenceClient
import torch
from transformers import pipeline

# Inference client setup
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")
pipe = pipeline("text-generation", "microsoft/Phi-3-mini-4k-instruct", torch_dtype=torch.bfloat16, device_map="auto")

# Global flag to handle cancellation
stop_inference = False

# Default system message
DEFAULT_SYSTEM_MESSAGE = (
    "You are a helpful chatbot who answers questions according to Occam's razor, "
    "which suggests that the simplest explanation is usually the best one. Answer as concisely as possible. "
    "DO NOT explain everything in 3-5 paragraphs. Only provide the single simplest possible answer or solution. "
    "Ensure that the answer is still clearly explained to a user who does not understand, "
    "but avoid long and drawn out answers to simple questions. Prioritize speed of answering."
)

def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens=512,
    temperature=0.7,
    top_p=0.95,
    use_local_model=False,
):
    global stop_inference
    stop_inference = False  # Reset cancellation flag

    # Initialize history if it's None
    if history is None:
        history = []

    # Use `system_message` from the state
    if use_local_model:
        # Local inference 
        messages = [{"role": "system", "content": system_message}]
        for val in history:
            if val[0]:
                messages.append({"role": "user", "content": val[0]})
            if val[1]:
                messages.append({"role": "assistant", "content": val[1]})
        messages.append({"role": "user", "content": message})

        response = ""
        for output in pipe(
            messages,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True,
            top_p=top_p,
        ):
            if stop_inference:
                response = "Inference cancelled."
                yield history + [(message, response)]
                return
            token = output['generated_text'][-1]['content']
            response += token
            yield history + [(message, response)]  # Yield history + new response

    else:
        # API-based inference 
        messages = [{"role": "system", "content": system_message}]
        for val in history:
            if val[0]:
                messages.append({"role": "user", "content": val[0]})
            if val[1]:
                messages.append({"role": "assistant", "content": val[1]})
        messages.append({"role": "user", "content": message})

        response = ""
        for message_chunk in client.chat_completion(
            messages,
            max_tokens=max_tokens,
            stream=True,
            temperature=temperature,
            top_p=top_p,
        ):
            if stop_inference:
                response = "Inference cancelled."
                yield history + [(message, response)]
                return
            token = message_chunk.choices[0].delta.content
            response += token
            yield history + [(message, response)]  # Yield history + new response


def cancel_inference():
    global stop_inference
    stop_inference = True

# Custom CSS for a fancy look
custom_css = """
#main-container {
    background-color: #f0f0f0;
    font-family: 'Arial', sans-serif;
}
.gradio-container {
    max-width: 700px;
    margin: 0 auto;
    padding: 20px;
    background: white;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
}
.gr-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.gr-button:hover {
    background-color: #45a049;
}
.gr-slider input {
    color: #4CAF50;
}
.gr-chat {
    font-size: 16px;
}
#title {
    text-align: center;
    font-size: 2em;
    margin-bottom: 20px;
    color: #333;
}
"""

# Define the interface
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("<h1 style='text-align: center;'>🪒 Occam's Chatbot 🪒</h1>")
    gr.Markdown("Occam's Razor is the problem-solving principle that recommends searching for explanations constructed with the smallest possible set of elements.")

    # Define a persistent state for the system message
    system_message_state = gr.State(value=DEFAULT_SYSTEM_MESSAGE)
    
    # Checkbox to toggle local model usage
    use_local_model = gr.Checkbox(label="Use Local Model", value=False)

    # Parameters for model control
    max_tokens = gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens")
    temperature = gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature")
    top_p = gr.Slider(minimum=0.1, maximum=1.0, value=0.95, step=0.05, label="Top-p (nucleus sampling)")

    # Chat components
    chat_history = gr.Chatbot(label="Chat")
    user_input = gr.Textbox(show_label=False, placeholder="The simplest solution is often the best...")
    cancel_button = gr.Button("Cancel Inference", variant="danger")

    # Pass the `system_message_state` to the `respond` function
    user_input.submit(respond, [user_input, chat_history, system_message_state, max_tokens, temperature, top_p, use_local_model], chat_history)

    cancel_button.click(cancel_inference)

if __name__ == "__main__":
    demo.launch(share=False)  # Remove share=True because it's not supported on HF Spaces

import gradio as gr
from huggingface_hub import InferenceClient
import torch
from transformers import pipeline

# Set up the local model (Phi-3-mini-4k-instruct) for text generation
local_pipe = pipeline("text-generation", model="microsoft/Phi-3-mini-4k-instruct", torch_dtype=torch.bfloat16, device_map="auto")

# Set up the Inference client for API-based inference (Zephyr 7B model)
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")

# Global flag for stopping inference (if needed)
stop_inference = False

# Occam's Razor-themed system message
DEFAULT_SYSTEM_MESSAGE = (
    "You are a helpful chatbot who answers questions according to Occam's Razor, "
    "which suggests that the simplest explanation is usually the best one. Answer as concisely as possible. "
    "DO NOT explain everything in 3-5 paragraphs. Only provide the single simplest possible answer or solution. "
    "Ensure that the answer is still clearly explained to a user who does not understand, "
    "but avoid long and drawn-out answers to simple questions. Prioritize speed of answering."
)

# Function to generate responses
def respond(
    message,
    history,
    system_message=DEFAULT_SYSTEM_MESSAGE,
    max_tokens=256,
    temperature=0.7,
    top_p=0.95,
    use_local_model=False,
):
    global stop_inference
    stop_inference = False  # Reset cancellation flag

    # Initialize history if it's None
    if history is None:
        history = []

    # Prepare the chat messages with the system message and conversation history
    messages = [{"role": "system", "content": system_message}]
    for user_input, bot_response in history:
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": bot_response})
    messages.append({"role": "user", "content": message})

    # Generate response based on the model selected
    if use_local_model:
        # Use local model (Phi-3-mini-4k-instruct)
        prompt = local_pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        output = local_pipe(
            prompt,
            do_sample=True
        )
        response_text = output[0]["generated_text"].split("<|assistant|>")[-1].strip()

    else:
        # Use API-based model (Zephyr 7B)
        response_text = ""
        try:
            response = client.chat_completion(
                messages=messages,
                stream=False
            )
            response_text = response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error in API response: {e}")
            response_text = "Error generating response"

    # Append the user message and model response to history
    history.append((message, response_text))
    return history

def cancel_inference():
    global stop_inference
    stop_inference = True

# Custom CSS for Gradio interface styling
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

# Define the Gradio interface
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("<h1 style='text-align: center;'>🪒 Occam's Chatbot 🪒</h1>")
    gr.Markdown("Explanations, simplified")

    # System message state
    system_message_state = gr.State(value=DEFAULT_SYSTEM_MESSAGE)
    
    # Toggle to use the local model or API
    use_local_model = gr.Checkbox(label="Use Local Model (Phi-3-mini-4k-instruct)", value=False)

    # Chat interface elements
    chat_history = gr.Chatbot(label="Chat")
    user_input = gr.Textbox(show_label=False, placeholder="The simplest solution is usually the best...")

    # Cancel button
    cancel_button = gr.Button("Cancel Inference", variant="danger")

    # Submit the input and generate response
    user_input.submit(respond, [user_input, chat_history, system_message_state, use_local_model], chat_history)

    # Cancel inference button
    cancel_button.click(cancel_inference)

if __name__ == "__main__":
    demo.launch(share=False)

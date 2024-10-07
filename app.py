import gradio as gr
from huggingface_hub import InferenceClient
import torch
from transformers import pipeline
import random

# Inference client setup
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")
pipe = pipeline("text-generation", "microsoft/Phi-3-mini-4k-instruct", torch_dtype=torch.bfloat16, device_map="auto")

# Global flag to handle cancellation
stop_inference = False

base_message = """You are a chatbot that responds with famous quotes from books, movies, philosophers, and business leaders.
Provide no advice, commentary, or additional context.
Your responses should be concise, no more than 3 quotes, and consist only of famous motivational quotes."""

def respond(
    message,
    history: list[tuple[str, str]],
    system_message_val,
    temperature=0.7,
    practicality=None,
    use_local_model=False,
    max_tokens=256,
):
    global stop_inference
    stop_inference = False  # Reset cancellation flag

    if practicality is None:
        practicality = round(random.uniform(0,1), 1)  # Initialize random practicality score
    if practicality > 0.5:
        append_message = "Provide actionable advice or direct instructions."
    else:
        append_message = "Provide theoretical concepts or abstract quotes."
    system_message_val = f"{base_message} {append_message}"

    # Initialize history if it's None
    if history is None:
        history = []

    if use_local_model:
        # Convert the conversation history and current message into a single string
        input_text = system_message_val + "\n"
        for val in history:
            if val[0]:
                input_text += f"User: {val[0]}\n"
            if val[1]:
                input_text += f"Assistant: {val[1]}\n"
        input_text += f"User: {message}\nAssistant:"

        # Generate response using the local model
        output = pipe(
            input_text,
            temperature=temperature,
            max_new_tokens=max_tokens,
            do_sample=True,
            num_return_sequences=1,
        )

        # Access the generated text
        generated_text = output[0]['generated_text']
        response = generated_text.split("Assistant:")[-1].strip()

        yield history + [(message, response)], system_message_val  # Yield history + new response

    else:
        # API-based inference
        messages = [{"role": "system", "content": system_message_val}]
        for val in history:
            if val[0]:
                messages.append({"role": "user", "content": val[0]})
            if val[1]:
                messages.append({"role": "assistant", "content": val[1]})
        messages.append({"role": "user", "content": message})

        response = ""
        for message_chunk in client.chat_completion(
            messages=messages,
            stream=True,
            temperature=temperature,
            max_tokens=max_tokens
        ):
            if stop_inference:
                response = "Inference cancelled."
                yield history + [(message, response)], system_message_val
                return

            # Store the chunk for debugging
            print(f"Raw payload: {message_chunk}")

            try:
                # Adjusted parsing logic
                delta = message_chunk.choices[0].delta
                token = getattr(delta, 'content', '')
                response += token
            except Exception as e:
                print("Error parsing message chunk:", e)
                continue  # Skip to the next message_chunk

            yield history + [(message, response)], system_message_val  # Yield history + new response

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
    gr.Markdown("<h1 style='text-align: center;'>💡 Ask the Greats 💡</h1>")
    gr.Markdown("Want to know the secret to life? Ask away!")

    with gr.Row():
        system_message_box = gr.Textbox(
            value=base_message,
            label="System message",
            visible=False
        )
        use_local_model = gr.Checkbox(label="Use Local Model", value=False)
        temperature = gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature")
        practicality = gr.Slider(minimum=0.1, maximum=1.0, value=0.5, step=0.05, label="Practicality")

    chat_history = gr.Chatbot(label="Chat")

    user_input = gr.Textbox(show_label=False, placeholder="What is the meaning of life?")

    cancel_button = gr.Button("Cancel Inference", variant="danger")
    # Adjusted to ensure history is maintained and passed correctly
    user_input.submit(
        respond, 
        inputs=[user_input, chat_history, system_message_box, temperature, practicality, use_local_model],
        outputs=[chat_history, system_message_box]
    )

    cancel_button.click(cancel_inference)

if __name__ == "__main__":
    demo.launch(share=True)

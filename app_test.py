from huggingface_hub import InferenceClient

client = InferenceClient(api_key="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")

for message in client.chat_completion(
	model="HuggingFaceH4/zephyr-7b-beta",
	messages=[{"role": "user", "content": "What is the capital of France?"}],
	max_tokens=500,
	stream=True,
):
    print(message.choices[0].delta.content, end="")
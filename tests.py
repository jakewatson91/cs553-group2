import time
from app import respond, cancel_inference  # assuming respond and cancel_inference are defined in app.py

def test_api():
    # Set up input parameters for API model
    message = "What is the meaning of life?"
    history = []
    system_message = "You are a helpful, concise chatbot."
    max_tokens = 256
    temperature = 0.7
    top_p = 0.95
    use_local_model = False  # Use API model

    start_time = time.time()

    # Call the respond function (generator)
    result_generator = respond(
        message=message,
        history=history,
        system_message=system_message,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        use_local_model=use_local_model
    )

    # Collect results
    final_history = None
    for result in result_generator:
        final_history = result

    end_time = time.time()
    runtime = end_time - start_time

    print("API Runtime:", runtime)
    print("API Final conversation history:", final_history)


def test_local():
    # Set up input parameters for local model
    message = "What is the meaning of life?"
    history = []
    system_message = "You are a helpful, concise chatbot."
    max_tokens = 256
    temperature = 0.7
    top_p = 0.95
    use_local_model = True  # Use local model

    start_time = time.time()

    # Call the respond function (generator)
    result_generator = respond(
        message=message,
        history=history,
        system_message=system_message,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        use_local_model=use_local_model
    )

    # Collect results
    final_history = None
    for result in result_generator:
        final_history = result

    end_time = time.time()
    runtime = end_time - start_time

    print("Local Runtime:", runtime)
    print("Local Final conversation history:", final_history)

# Run the tests
if __name__ == "__main__":
    test_api()
    test_local()

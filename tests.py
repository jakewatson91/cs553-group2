from app import respond, base_message
import time

def test_api():
    # Set up input parameters
    message = "What is the meaning of life?"
    history = []
    system_message_val = base_message
    temperature = 0.7
    practicality = 0.8  # This should modify the system message to provide actionable advice
    max_tokens = 256
    use_local_model = False  # Set to False to use the API-based model

    start_time = time.time()

    # Call the respond function (generator)
    result_generator = respond(
        message=message,
        history=history,
        system_message_val=system_message_val,
        temperature=temperature,
        practicality=practicality,
        use_local_model=use_local_model
    )

    # Iterate over the generator to get the final output
    final_history, final_system_message = None, None
    for result in result_generator:
        final_history, final_system_message = result

    end_time = time.time()
    runtime = end_time - start_time

    print("API Runtime: ", runtime)
    print("API Final conversation history:", final_history)
    print("API Final system message:", final_system_message)


def test_local():
    # Set up input parameters
    message = "What is the meaning of life?"
    history = []
    system_message_val = base_message
    temperature = 0.7
    practicality = 0.8  # This should modify the system message to provide actionable advice
    use_local_model = True  # Set to True to use the local model

    start_time = time.time()
    print("start time: ", start_time)

    # Call the respond function (generator)
    result_generator = respond(
        message=message,
        history=history,
        system_message_val=system_message_val,
        temperature=temperature,
        practicality=practicality,
        use_local_model=use_local_model,
        max_tokens=256
    )

    # Iterate over the generator to get the final output
    final_history, final_system_message = None, None
    print("Iterating over results...")
    for result in result_generator:
        print("Result: ", result)
        final_history, final_system_message = result

    end_time = time.time()
    runtime = end_time - start_time

    print("Local Runtime: ", runtime)
    print("Local Final conversation history:", final_history)
    print("Local Final system message:", final_system_message)

# Run the tests
if __name__ == "__main__":
    # test_api()
    test_local()

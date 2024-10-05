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

    # Call the respond function
    result_generator = respond(
        message=message,
        history=history,
        system_message_val=system_message_val,
        temperature=temperature,
        practicality=practicality,
        max_tokens=max_tokens,
        use_local_model=use_local_model
    )

    # Since respond is a generator, we need to iterate over it to get the final output
    for result in result_generator:
        final_history, final_system_message = result
        # Optionally, print intermediate results
        # print("Intermediate history:", final_history)

    end_time = time.time()
    runtime = end_time - start_time

    print("API Runtime: ", runtime)
    print("API Final conversation history:", final_history)
    print("API Final system message:", final_system_message)


def test_local():
    # Set up input parameters
    message = "What is the meaning of life"
    history = []
    system_message_val = base_message
    temperature = 0.7
    practicality = 0.8  # This should modify the system message to provide actionable advice
    max_tokens = 256
    use_local_model = True

    start_time = time.time()

    # Call the respond function
    result = list(respond(
        message=message,
        history=history,
        system_message_val=system_message_val,
        temperature=temperature,
        practicality=practicality,
        max_tokens=max_tokens,#test
        use_local_model=use_local_model
    ))

    end_time = time.time()
    runtime = end_time - start_time

    final_history, final_system_message = result[-1]
    print("Local Runtime: ", runtime)
    print("Local Final conversation history:", final_history)
    print("Local Final system message:", final_system_message)

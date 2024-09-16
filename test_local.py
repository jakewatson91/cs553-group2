from app import respond, base_message 
import time

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
        max_new_tokens=max_tokens,
        use_local_model=use_local_model
    ))

    end_time = time.time()
    runtime = end_time - start_time

    final_history, final_system_message = result[-1]
    print("Runtime: ", runtime)
    print("Final conversation history:", final_history)
    print("Final system message:", final_system_message)


        
import unittest
from unittest.mock import patch, MagicMock
from app import respond

class TestRespondFunction(unittest.TestCase):

    @patch('app/respond.pipe')  # Mocking the local model inference pipeline
    def test_respond_with_local_model(self, mock_pipe):
        # Mocking the pipeline's output
        mock_pipe.return_value = iter([{'generated_text': [{'content': 'Hello!'}]}])

        # Input parameters for the respond function
        message = "Hello"
        history = [("Hi", "Hello there")]
        system_message = "You are a friendly Chatbot."
        max_tokens = 10
        temperature = 0.7
        top_p = 0.95
        use_local_model = True

        # Call the respond function and convert the generator to a list
        result = list(respond(message, history, system_message, max_tokens, temperature, top_p, use_local_model))

        # Check that the response is as expected
        self.assertEqual(result[-1], history + [(message, "Hello!")])

if __name__ == '__main__':
    unittest.main()

import requests
import json
import gradio as gr

# 65 seg
URL = "http://localhost:11434/api/generate"
HEADERS = {
    'Content-Type': 'application/json',
}

CONVERSATION_HISTORY = []

def generate_response(user_input):
    try:
        # Read the content of the leeme.txt file
        with open("leeme.txt", "r") as f:
            leeme_text = f.read()

        # Append the leeme.txt content to the prompt
        full_prompt = "\n".join(CONVERSATION_HISTORY) + leeme_text + "\n" + user_input

        # Construct the request data
        data = {
            "model": "netrunner:latest",
            "stream": False,
            "prompt": """ Eres Mario Bros, responde en castellano """ + full_prompt,
        }

        # Send the POST request to the API
        response = requests.post(URL, headers=HEADERS, data=json.dumps(data))

        # Check the response status code
        if response.status_code == 200:
            # Process the response data
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data["response"]

            # Update the conversation history and return the response
            CONVERSATION_HISTORY.append(actual_response)
            print("info:", response.status_code, response.text)
            return actual_response
        else:
            # Handle error response
            print("Error:", response.status_code, response.text)
            return None

    except Exception as e:
        # Handle general exceptions
        print("An error occurred:", e)
        return None

iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs="text"
)

iface.launch(share=True)

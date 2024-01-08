import requests
import json
import gradio as gr

URL = "http://localhost:11434/api/generate"
HEADERS = {
    'Content-Type': 'application/json',
}

CONVERSATION_HISTORY = []

def generate_response(prompt):
    try:
        CONVERSATION_HISTORY.append(prompt)
        full_prompt = "\n".join(CONVERSATION_HISTORY)
        data = {
            "model": "mistral",
            "stream": False,
            "prompt": full_prompt,
        }

        response = requests.post(URL, headers=HEADERS, data=json.dumps(data))

        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data["response"]
            CONVERSATION_HISTORY.append(actual_response)
            return actual_response
        else:
            print("Error:", response.status_code, response.text)
            return None

    except Exception as e:
        print("An error occurred:", e)
        return None

iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),  # Cambio en la sintaxis
    outputs="text"
)

iface.launch()

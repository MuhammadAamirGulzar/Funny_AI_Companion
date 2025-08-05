from flask import Flask, render_template, request, jsonify
import requests
from pydantic import BaseModel
from typing import Any
import json

app = Flask(__name__)

# Example JSON output from the `curlOut` command
curlOut = '''
{
  "tunnels": [
    {
      "public_url": "https://44b8-35-187-230-202.ngrok-free.app"
    }
  ]
}
'''

# Parse the JSON string to get the public URL
parsed_json = json.loads(curlOut)
ngrokURL = parsed_json['tunnels'][0]['public_url']

# Pydantic model to validate the input to the API
class TextInput(BaseModel):
    inputs: str
    parameters: dict[str, Any] | None

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    response = get_Chat_response(msg)
    return jsonify({"response": response})

def get_Chat_response(text):
    # Data to send in the POST request
    data = {
        "inputs": text,
        "parameters": {"max_length": 200}
    }

    # Convert data to TextInput instance
    text_input = TextInput(**data)

    # Serialize TextInput to dictionary and then to JSON
    text_input_dict = text_input.dict()

    # Send the POST request to the API
    response = requests.post(ngrokURL + "/generate/", json=text_input_dict)

    # Check the response
    if response.status_code == 200:
        result = response.json()
        return result.get("generated_text", "Error: No generated text found.").strip()
    else:
        return "Error: Unable to get response from the API."

if __name__ == '__main__':
    app.run(debug=True)

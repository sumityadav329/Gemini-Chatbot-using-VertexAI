from flask import Flask, render_template, request, jsonify
import os
from vertexai.preview.generative_models import GenerativeModel
from dotenv import load_dotenv
import vertexai

load_dotenv()

app = Flask(__name__)

project_id = os.getenv("project_id")
region = os.getenv("region")

# Authentication
vertexai.init(project=project_id, location=region)

model = GenerativeModel("gemini-1.0-pro")

@app.route("/")
def home(): 
    return render_template("index.html")

@app.route("/gemini", methods=["POST"])
def vertex_ai():
    userInput = request.form.get("userInput")
    
    responses = model.generate_content(userInput, stream=True)

    res = [response.candidates[0].content.parts[0].text for response in responses]
    final_res = "".join(res)
    
    return jsonify(content=final_res)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

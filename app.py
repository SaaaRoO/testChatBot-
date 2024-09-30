from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Set the folder for uploaded files

# Configure  API key here
genai.configure(api_key='AIzaSyDK4uGN2hWp6cdrug9t0IHXa0L6UB6DrBs')

# Define the generation config for the AI model
generation_config = {
    "temperature": 0.4,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",  # Specify the AI model to use
    generation_config=generation_config,
)

@app.route('/')
def index():
    # Render the index.html template for the main page
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Handle chat messages sent by the user
    data = request.get_json()  # Get JSON data from the request
    user_input = data.get('user_input')  # Extract user input from the data

    # Check if user input is provided
    if not user_input:
        return jsonify({"error": "No user input provided."}), 400

    # Start a chat session with an empty history
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_input)  # Send user input to the AI model

    # Return the AI's response as JSON
    return jsonify({"response": response.text})

@app.route('/upload', methods=['POST'])
def upload_file():
    # Handle file uploads from the user
    if 'file' not in request.files:  # Check if a file is part of the request
        return jsonify({"error": "No file part."}), 400

    file = request.files['file']  # Get the file from the request
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400  # Check if a file was selected

    # Save the uploaded file to the specified folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Return a success message with the filename
    return jsonify({"message": "File uploaded successfully!", "filename": file.filename})

if __name__ == '__main__':
    # Create the upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)  # Run the Flask app in debug mode

from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)
# Configure the folder where uploaded files will be stored
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Configure API key here
genai.configure(api_key='AIzaSyCrUBVHO0FVc8KBzJjuWow8uDay7iIwn-c') 

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",  # Specify the model to use
)

# Initialize an empty list to store the conversation history
conversation_history = []

@app.route('/')
def index():
    # Render the main chat interface
    return render_template('index.html', history=conversation_history)

@app.route('/chat', methods=['POST'])
def chat():
    # Handle incoming chat messages
    data = request.get_json()  # Parse the JSON data from the request
    user_input = data.get('user_input')  # Extract user input

    # Check if user input is provided
    if not user_input:
        return jsonify({"error": "No user input provided."}), 400

    # Create a context string from conversation history for better responses
    context = " ".join([f"User: {msg['user']}\nBot: {msg['bot']}" for msg in conversation_history])
    context += f"\nUser: {user_input}"  # Add the current user input to the context

    # Generate a response based on the full context
    response = model.generate_content([context])
    
    # Store the conversation history
    conversation_history.append({"user": user_input, "bot": response.text})  # Save the interaction

    # Return the generated response and updated history as JSON
    return jsonify({"response": response.text, "history": conversation_history})

@app.route('/upload', methods=['POST'])
def upload_file():
    # Handle file uploads
    if 'file' not in request.files:
        return jsonify({"error": "No file part."}), 400  # Error if no file part is found

    file = request.files['file']  # Get the uploaded file
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400  # Error if no file was selected

    # Save the uploaded file to the designated folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Generate content based on the uploaded image
    image_description = model.generate_content([file_path, "\n\n", "Please describe the content of this image."])
    
    # Store the conversation history with the uploaded image information
    conversation_history.append({"user": f"Uploaded: {file.filename}", "bot": image_description.text})

    # Return a success message with the image description and updated history
    return jsonify({"message": f"File '{file.filename}' uploaded successfully!", "description": image_description.text, "history": conversation_history})

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create the upload folder if it doesn't exist
    app.run(debug=True)  # Run the Flask app in debug mode

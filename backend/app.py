from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Define a folder to store uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def handle_file_upload():
    """Receives an uploaded file, saves it, and returns a success message."""
    file = request.files.get('file')

    if file and file.filename:
        filename = secure_filename(file.filename)  # Secure the filename to avoid file path traversal attacks
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        # Implement any processing you need on the file here

        return jsonify({'message': 'File uploaded successfully', 'filename': filename})
    
    return jsonify({'error': 'No file provided or file has no name'}), 400

if __name__ == "__main__":
    app.run(debug=True)

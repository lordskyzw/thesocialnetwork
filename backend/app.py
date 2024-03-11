from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
from werkzeug.utils import secure_filename
import os
import networkx as nx

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def handle_file_upload():
    """Receives an uploaded file, saves it, and returns a success message along with the filename of the network file"""
    file = request.files.get('file')
    if file and file.filename:
        filename = secure_filename(file.filename)  # Secure the filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename})
    else:
        return jsonify({'error': 'No file provided or file has no name'}), 400
 
@app.route("/show-analysis", methods=["POST"])
def show_analysis():
    """Expects a file name in the POST request and returns a network analysis of the file"""
    data = request.get_json()
    filename = data['filename']
    path = f'{UPLOAD_FOLDER}/{filename}'

    if os.path.exists(path=path):
        try:
            network = nx.read_edgelist(path=path)
        except Exception as e:
            return jsonify({'error': 'Error reading network file', 'details': str(e)}), 500
        info = nx.info(G=network)
        return jsonify({'network_info': info})
    else:
        return jsonify({'error': 'File does not exist'}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=True)

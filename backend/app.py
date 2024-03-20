from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import networkx as nx
import logging
from utils import get_hub, get_eigen_node, get_network_description, distance_calculator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.info(f"File {filename} uploaded successfully and saved to {save_path}")
        return jsonify({'message': 'File uploaded successfully', 'filename': filename})
    else:
        logging.error("No file provided or file has no name")
        return jsonify({'error': 'No file provided or file has no name'}), 400
 
@app.route("/show-analysis", methods=["POST"])
def show_analysis():
    """Expects a file name in the POST request and returns a network analysis of the file
        after processing a network file it caches it so that next time it first checks the cache"""
    data = request.get_json()
    filename = data['filename']
    path = f'{UPLOAD_FOLDER}/{filename}'

    if os.path.exists(path):
        logging.info(f"Processing network analysis for {filename}")
        try:
            network = nx.read_edgelist(path=path)
            logging.info("Network file read successfully")

            # Extract basic information
            num_nodes = len(network.nodes())
            logging.info("nodes calculated")
            num_edges = len(network.edges())
            logging.info("edges calculated")
            hub, hub_connections = get_hub(network)
            logging.info("calculated hub")
            clustering = nx.average_clustering(G=network)
            logging.info("calculated clustering")
            eigen_node = get_eigen_node(nx.eigenvector_centrality(G=network))
            logging.info("calculated eigen node")
            eigen_node, _ = next(iter(eigen_node.items()))

    

            info = {
                'nodes': num_nodes,
                'edges': num_edges,
                'hub': hub,
                'hub_connections': hub_connections,
                'average_clustering': clustering,
                'eigen_node': eigen_node,
            }
            try:
                description= get_network_description(network_facts=info)
                info['description']=description
            except Exception as e:
                logging.error(f"ERROR IN SENDING OVER THE NETWORK FACTS TO THE AI: {e}")

            logging.info("=====================================FULL NETWORK ANALYSIS COMPLETED===============================")
        except Exception as e:
            logging.error(f"Error reading network file: {e}")
            return jsonify({'error': 'Error reading network file', 'details': str(e)}), 500

        return jsonify({'network_info': info})
    else:
        logging.error(f"File {filename} does not exist")
        return jsonify({'error': 'File does not exist'}), 404

@app.route("/get-distance", methods=["POST"])
def get_distance():
    '''lets talk about what we actually want on our advanced analysis tab
    1.) distance calculator ~ this could be a form which sends over data to a dedicated endpoint (this endpoint) which calculates distances
    the form shall input source node, destination node and the network file path along with the method to be used from options provided
    WHAT THE ENDPOINT RETURNS:
        1.) short info about the nodes
        2.) distance, 
        3.) it should return info about the method used'''
    '''ok lets work on the current requirements'''
    data = request.get_json()
    source_node = data['sourceNode']
    destination_node = data['destinationNode']
    network_file_path = data['networkFilePath']
    distance = distance_calculator(graph_path=network_file_path, source_node=source_node, destination_node=destination_node)
    return jsonify({'distance': distance}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=True)

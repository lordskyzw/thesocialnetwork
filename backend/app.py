from flask import Flask
import networkx as nx

app = Flask(__name__)

@app.route("/show-analysis", methods=["POST"])
def show_analysis():
    '''this function performs an overview analysis on the network and returns a dictionary of the network description'''
    
    return
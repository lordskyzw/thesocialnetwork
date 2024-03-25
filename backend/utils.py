from openai import OpenAI
import os
import networkx as nx
import logging
import base64
import io
import matplotlib.pyplot as plt
import numpy as np
import time


client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key=os.environ.get("OPENROUTER_API_KEY")
)

def get_network_description(network_facts)-> str:
    '''this function sends over the network facts to an llm which then returns a short summary of the network'''
    completion = client.chat.completions.create(
    model="openchat/openchat-7b:free",
    messages=[
        {
        "role": "user",
        "content": f"given the following social network facts, give an overview summary and what might be interesting: SOCIAL NETWORK FACTS:{network_facts}",
        },
    ],
    )
    return completion.choices[0].message.content

def get_hub(network: nx.Graph):
    most_connected_node = max(network.degree, key=lambda pair: pair[1])
    return most_connected_node[0], most_connected_node[1]


def get_eigen_node(node_dict):
    my_dict = dict(node_dict)
    key_with_highest_value = max(my_dict, key=my_dict.get)
    highest_value_dict = {key_with_highest_value: my_dict[key_with_highest_value]}

    return(highest_value_dict)

def distance_calculator(graph_path, source_node, destination_node):
    '''if the nodes are invalid raise an error'''
    try:
        network = nx.read_edgelist(path=graph_path)
        distance = nx.shortest_path_length(G=network, source=source_node, target=destination_node)
    except Exception as e:
        logging.error(f"utils.py distance_calculator encountered an erro {e}")
        return e
    return int(distance)

def create_network_image(network_path):
    '''this function creates a network image and returns its base64 string'''
    try:
        network = nx.read_edgelist(path=network_path)
        logging.info("Calculating POS")
        start_time = time.perf_counter()
        pos = nx.spring_layout(network)
        time_taken = time.perf_counter() - start_time
        logging.info(f"Done calculating pos, time taken: {time_taken}")
        options = {
            "font_size": 6,
            "node_size": 3000,
            "node_color": "white",
            "edgecolors": "black",
            "linewidths":3,
            "width": 3,
        }
        nx.draw(network, pos, with_labels=True, **options)
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)

        # Encode the image in memory to base64
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        return img_base64
    except Exception as e:
        logging.error(f"Error creating network image: {e}")
        return e
            
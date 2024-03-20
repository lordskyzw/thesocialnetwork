from openai import OpenAI
import os
import networkx as nx
import logging

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
        distance = nx.shortest_path_length(graph=network, source=source_node, target=destination_node)
    except Exception as e:
        logging.error(f"utils.py distance_calculator encountered an erro {e}")
        return e
    return int(distance)
    
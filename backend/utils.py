from openai import OpenAI
import os

client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key=os.environ.get("OPENROUTER_API_KEY")
)

def get_network_description(network_facts)-> str:
    '''this function sends over the network facts to an llm which then returns a short summary of the network'''
    completion = client.chat.completions.create(
    model="mistralai/mistral-7b-instruct:free",
    messages=[
        {
        "role": "user",
        "content": f"given the following social network facts, give an overview summary and what might be interesting: SOCIAL NETWORK FACTS:{network_facts}",
        },
    ],
    )
    return completion.choices[0].message.content

def get_hub(node_dict):
    my_dict = dict(node_dict)

    # Find the key with the highest value
    key_with_highest_value = max(my_dict, key=my_dict.get)

    # Create a new dictionary with only the highest value
    highest_value_dict = {key_with_highest_value: my_dict[key_with_highest_value]}

    return(highest_value_dict)


def get_eigen_node(node_dict):
    my_dict = dict(node_dict)
    key_with_highest_value = max(my_dict, key=my_dict.get)
    highest_value_dict = {key_with_highest_value: my_dict[key_with_highest_value]}

    return(highest_value_dict)

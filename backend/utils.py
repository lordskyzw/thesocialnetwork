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

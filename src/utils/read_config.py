import yaml

def extract_config(CONFIG_PATH):
    """
    Extract settings from config file.

    Takes in:
        - A string specifying the path of the config file

    Returns
        - A dictionary with the contents of the config file
    """

    with open(CONFIG_PATH) as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)

    return settings


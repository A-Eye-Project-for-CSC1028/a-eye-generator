import os
import re
import sys

from typing import Any, Mapping, Sequence, Union


"""
Get data from different 'indexed' data structures.
"""


def get_value_at_index(obj: Union[Sequence, Mapping], index: int) -> Any:
    try:
        return obj[index]
    except KeyError:
        return obj['result'][index]


"""
Import 'nodes' module from the ComfyUI path for use in the generation script.
"""


def import_nodes_module(comfy_path: str) -> Any:
    nodes_path = os.path.join(comfy_path, 'nodes.py')

    if os.path.exists(nodes_path):
        sys.path.append(comfy_path)
        import nodes
        return nodes
    else:
        raise FileNotFoundError(f'nodes.py not found in "{comfy_path}"')


"""
Recursively find an import path based on its name and parent directory.
"""


def find_path(name: str, path: str = None) -> str:
    # If no path is given, use the current working directory.
    if path is None:
        path = os.getcwd()

    # Check if the current directory contains the name.
    if name in os.listdir(path):
        path_name = os.path.join(path, name)
        print(f'{name} found: {path_name}')
        return path_name

    # Get the parent directory.
    parent_directory = os.path.dirname(path)

    # If the parent directory is the same as the current directory, we've reached the root and stop the search.
    if parent_directory == path:
        return None

    # Recursively call the function with the parent directory.
    return find_path(name, parent_directory)


"""
Parse settings from .config, as follows:
- COMFY_DIRECTORY => A string that provides the path to the user's ComfyUI directory.
"""


def parse_config() -> dict:
    config = {}

    # Obtain preset settings from config.txt file...
    with open('.config', 'r') as file:
        # ...line-by-line!
        for line in file:
            # Find anything between double quotes in line.
            matches = re.findall(r'"([^"]+)"', line)

            if matches:
                for match in matches:
                    # Get name of setting in config.txt:
                    setting_name = line.split(r'="')[0]
                    config[setting_name] = match

        file.close()

    return config

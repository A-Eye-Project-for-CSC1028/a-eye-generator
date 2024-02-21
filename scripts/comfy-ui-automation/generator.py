import os
import random
import re
import sys
from typing import Any, Mapping, Sequence, Union

import torch


gen_params = {
    "image": "scene.png",
    "positive_prompt": "",
    "negative_prompt": "",
    "steps": 35,
    "cfg": 7,
    "sampler": "dpmpp_3m_sde_gpu",
    "scheduler": "exponential",
    "denoise": 1,
    "dimensions": (1024, 1024),
    "iterations": 10,
    "file_prefix": "ComfyUI"
}


"""
Parse settings from config.txt, as follows:
- COMFY_DIRECTORY => A string that provides the path to the user's ComfyUI directory.
"""


def parse_config() -> dict:
    config = {}

    # Obtain preset settings from config.txt file...
    with open(".config", "r") as file:
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


# Get config details, such as where ComfyUI is located at on the user's computer.
config = parse_config()
comfy_path = config.get("COMFY_DIRECTORY")

"""
Locate the nodes.py file in the ComfyUI directory, and then import it for later use.
"""


def import_nodes_module() -> Any:
    nodes_path = os.path.join(comfy_path, "nodes.py")

    if os.path.exists(nodes_path):
        sys.path.append(comfy_path)
        import nodes
        return nodes
    else:
        raise FileNotFoundError(f"nodes.py not found in '{comfy_path}'")


"""
Returns the value at the given index of a sequence or mapping.

If the object is a sequence (like list or string), returns the value at the given index.
If the object is a mapping (like a dictionary), returns the value at the index-th key.

Some return a dictionary, in these cases, we look for the 'results' key

Args:
    obj (Union[Sequence, Mapping]): The object to retrieve the value from.
    index (int): The index of the value to retrieve.

Returns:
    Any: The value at the given index.

Raises:
    IndexError: If the index is out of bounds for the object and the object is not a mapping.
"""


def get_value_at_index(obj: Union[Sequence, Mapping], index: int) -> Any:
    try:
        return obj[index]
    except KeyError:
        return obj["result"][index]


"""
Recursively looks at parent folders starting from the given path until it finds the given name.
Returns the path as a Path object if found, or None otherwise.
"""


def find_path(name: str, path: str = None) -> str:
    # If no path is given, use the current working directory.
    if path is None:
        path = os.getcwd()

    # Check if the current directory contains the name.
    if name in os.listdir(path):
        path_name = os.path.join(path, name)
        print(f"{name} found: {path_name}")
        return path_name

    # Get the parent directory.
    parent_directory = os.path.dirname(path)

    # If the parent directory is the same as the current directory, we've reached the root and stop the search.
    if parent_directory == path:
        return None

    # Recursively call the function with the parent directory.
    return find_path(name, parent_directory)


def add_comfy_directory_to_sys_path() -> None:
    if comfy_path is not None and os.path.isdir(comfy_path):
        sys.path.append(comfy_path)
        print(f"'{comfy_path}' added to sys.path")


def add_extra_model_paths() -> None:
    """
    Parse the optional extra_model_paths.yaml file and add the parsed paths to the sys.path.
    """
    from main import load_extra_path_config

    extra_model_paths = find_path("extra_model_paths.yaml")

    if extra_model_paths is not None:
        load_extra_path_config(extra_model_paths)
    else:
        print("Could not find the extra_model_paths config file.")


# Prepare script for main():
add_comfy_directory_to_sys_path()
add_extra_model_paths()
nodes = import_nodes_module()


def main():
    with torch.inference_mode():
        # Load image from path:
        image_loader = nodes.LoadImage()
        image = image_loader.load_image(image=gen_params["image"])

        # Load Stable Diffusion checkpoint (safetensors/ckpt):
        checkpoint_loader_simple = nodes.CheckpointLoaderSimple()
        checkpoint = checkpoint_loader_simple.load_checkpoint(
            ckpt_name="sd_xl_base_1.0.safetensors"
        )

        # Load appropriate ControlNet checkpoint (safetensors/ckpt):
        controlnet_loader = nodes.ControlNetLoader()
        controlnet = controlnet_loader.load_controlnet(
            control_net_name="control-lora\control-LoRAs-rank256\control-lora-depth-rank256.safetensors"
        )

        clip_text_encode = nodes.CLIPTextEncode()

        # Encode positive prompt:
        positive_prompt_encode = clip_text_encode.encode(
            text=gen_params["positive_prompt"],
            clip=get_value_at_index(checkpoint, 1),
        )

        # Encode negative prompt:
        negative_prompt_encode = clip_text_encode.encode(
            text=gen_params["negative_prompt"],
            clip=get_value_at_index(checkpoint, 1),
        )

        # Define an empty latent image, and then size it appropriately.
        empty_latent_image = nodes.EmptyLatentImage()
        usable_latent_image = empty_latent_image.generate(
            width=gen_params["dimensions"][0],
            height=gen_params["dimensions"][1],
            batch_size=1,
        )

        # Prepare for image generation...
        controlnet_apply_advanced = nodes.ControlNetApplyAdvanced()
        k_sampler = nodes.KSampler()
        vae_decoder = nodes.VAEDecode()
        image_writer = nodes.SaveImage()

        # Generate as many images as in gen_params!
        for _ in range(gen_params["iterations"]):
            controlnet_applied = controlnet_apply_advanced.apply_controlnet(
                strength=1,
                start_percent=0,
                end_percent=1,
                positive=get_value_at_index(positive_prompt_encode, 0),
                negative=get_value_at_index(negative_prompt_encode, 0),
                control_net=get_value_at_index(controlnet, 0),
                image=get_value_at_index(image, 0),
            )

            sampled_image = k_sampler.sample(
                seed=random.randint(1, 2**64),
                steps=gen_params["steps"],
                cfg=gen_params["cfg"],
                sampler_name=gen_params["sampler"],
                scheduler=gen_params["scheduler"],
                denoise=gen_params["denoise"],  # 0-1
                model=get_value_at_index(checkpoint, 0),
                positive=get_value_at_index(controlnet_applied, 0),
                negative=get_value_at_index(controlnet_applied, 1),
                latent_image=get_value_at_index(usable_latent_image, 0),
            )

            decoded_image = vae_decoder.decode(
                samples=get_value_at_index(sampled_image, 0),
                vae=get_value_at_index(checkpoint, 2),
            )

            image_writer.save_images(
                filename_prefix=gen_params["file_prefix"], images=get_value_at_index(
                    decoded_image, 0)
            )


if __name__ == "__main__":
    main()

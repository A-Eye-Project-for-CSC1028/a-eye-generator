import os
import random
import sys

import torch

from .generation_parameters import GenerationParameters
from .utils import *

"""
A-Eye Image Generation Pipeline - Generates images based on a depth map and other parameters (see `GenerationParameters` class).
"""


def generate(parameters: GenerationParameters = GenerationParameters()):
    # Get config details, such as where ComfyUI is located at on the user's computer.
    config = parse_config()
    comfy_path = config.get("COMFY_DIRECTORY")

    # Add ComfyUI to sys.path...
    if comfy_path is not None and os.path.isdir(comfy_path):
        sys.path.append(comfy_path)

    # Import ComfyUI's nodes.py module:
    nodes = import_nodes_module(comfy_path)

    with torch.inference_mode():
        # Load image from path:
        image_loader = nodes.LoadImage()
        image = image_loader.load_image(image=parameters.image)

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
            text=parameters.positive_prompt,
            clip=get_value_at_index(checkpoint, 1),
        )

        # Encode negative prompt:
        negative_prompt_encode = clip_text_encode.encode(
            text=parameters.negative_prompt,
            clip=get_value_at_index(checkpoint, 1),
        )

        # Define an empty latent image, and then size it appropriately.
        empty_latent_image = nodes.EmptyLatentImage()
        usable_latent_image = empty_latent_image.generate(
            width=parameters.dimensions.x,
            height=parameters.dimensions.y,
            batch_size=1,
        )

        # Prepare for image generation...
        controlnet_apply_advanced = nodes.ControlNetApplyAdvanced()
        k_sampler = nodes.KSampler()
        vae_decoder = nodes.VAEDecode()
        image_writer = nodes.SaveImage()

        # Generate as many images as in parameters!
        for _ in range(parameters.iterations):
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
                steps=parameters.steps,
                cfg=parameters.cfg,
                sampler_name=parameters.sampler,
                scheduler=parameters.scheduler,
                denoise=parameters.denoise,
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
                images=get_value_at_index(decoded_image, 0))

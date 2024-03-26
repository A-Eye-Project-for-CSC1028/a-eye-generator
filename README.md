# A-Eye Generator

_Transforming depth maps into visually informative images for accessibility and understanding._

## Overview

The A-Eye Generator extends the functionality of the [public A-Eye web tool](https://a-eye-vision.tech/). This repository is the core engine for turning depth maps into images that aid in visual perception and interpretation.

## Key Features

- **Image Generation:** Effortlessly convert depth maps into visually-stimulating images. Provides a programmatic interface to interact with ComfyUI, making it automatable.
- **Object Bounding Box Drawer:** Highlight objects of interest within the generated images with outlined bounding boxes. Positioning data sourced from [web tool](https://a-eye-vision.tech/) at depth map render-time via the `Export JSON` button.

## Getting Started

### Prerequisites

- [Python 3.10.6](https://www.python.org/downloads/release/python-3106/): Any later version _should_ work, but is not expressly supported.
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI): Whatever the latest version is will do the trick!

### Installation

#### Part 1: a-eye-generator

- Firstly, clone this repository to your machine with:

```
git clone https://github.com/A-Eye-Project-for-CSC1028/a-eye-generator.git
```

- Once these items are completed, you should create a Python `venv` in the root of the newly-cloned repository:

```
python -m venv venv
```

- You'll need a customised version of PyTorch installed to your device, depending on its capabilities. To get the correct one, head over to their [`Get Started` section](https://pytorch.org/get-started/locally/) and configure your install.

[![](https://raw.githubusercontent.com/A-Eye-Project-for-CSC1028/a-eye-generator/master/assets/pytorch-get-started.png)](https://pytorch.org/get-started/locally/)

- Then, install all required dependencies from `requirements.txt`:

```
pip install -r requirements.txt
```

#### Part 2: ComfyUI

To actually generate the images, you'll need: ComfyUI, a pre-trained Stable Diffusion model, and a "Depth Control LoRA" model. Let's obtain these three things now...

- Download the latest release of ComfyUI from their official GitHub repository [here](https://github.com/comfyanonymous/ComfyUI/releases/tag/latest).

- Then, download any image-to-image `safetensors` model you desire - I've been using `sd_xl_base_1.0.safetensors` from StabilityAI on Hugging Face. It's available [here](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/sd_xl_base_1.0.safetensors).

- Once that download completes, move the `safetensors` file into the `ComfyUI/models/checkpoints` folder.

- Next, clone the following repository into the `ComfyUI/models/controlnet` folder:

```
git clone https://huggingface.co/stabilityai/control-lora
```

There's only one more thing to do in the name of setup - we need to tell `a-eye-generator` where ComfyUI is located...

### Pointing a-eye-generator to ComfyUI

If you look at this repository's file structure, you should see a `.config` file - it contains the location where ComfyUI is installed to on your device. The default is `COMFY_DIRECTORY="D:\Comfy for Stable Diffusion\User Interface\ComfyUI"`, as this is where I have my installation stored. For this repository to work, you need to update this with your ComfyUI folder.

To do this, navigate to the `ComfyUI` folder - please note, it's not the root folder with the `.bat` files; it's the `ComfyUI` folder within that directory that we need. See the below image highlighting this:

![](https://raw.githubusercontent.com/A-Eye-Project-for-CSC1028/a-eye-generator/master/assets/comfyui-directory.png)

Copy the file path of that folder, and paste it into the `.config` file.

Once that's completed, you should be set to work with A-Eye! See [usage](#usage) for more details.

### Usage

When using an image-to-image model, we need a source image to base all of our generated output on. We need to 'upload' this/these image(s) to ComfyUI.

To do this, navigate to `ComfyUI/input` and drop your image(s) there. You can call it/them whatever you like - just make sure to update the file name(s) in the generation script, too.

Now you're ready to start generating your very own 3D-model-based AI art!

**Contributing**

Contributions are most welcome! Please see below for more details:

- Open issues for bug reports or feature requests.
- Submit pull requests with code enhancements or new features.

**License**

This project is licensed under the [MIT license](https://github.com/A-Eye-Project-for-CSC1028/a-eye-generator/blob/master/LICENSE) - please see the linked document for more information.

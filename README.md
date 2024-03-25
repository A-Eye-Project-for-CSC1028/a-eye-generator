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

...

### Usage

...

**Contributing**

Contributions are most welcome! Please see below for more details:

- Open issues for bug reports or feature requests.
- Submit pull requests with code enhancements or new features.

**License**

This project is licensed under the [MIT license](https://github.com/A-Eye-Project-for-CSC1028/a-eye-generator/blob/master/LICENSE) - please see the linked document for more information.

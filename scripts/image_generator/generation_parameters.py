from typing import NamedTuple

"""
A named tuple used to represent a 2D vector (dimensions) - for readability.
"""


class Dimensions(NamedTuple):
    x: int
    y: int


"""
Allows the easier, safer definition of the parameters required to generate an image with Stable Diffusion.
"""


class GenerationParameters:
    def __init__(self, image: str = 'scene.png', positive_prompt: str = '', negative_prompt: str = '', steps: int = 35, cfg: float = 7.0, sampler: str = 'dpmpp_3m_sde_gpu', scheduler: str = 'exponential', denoise: float = 1.0, dimensions: Dimensions = Dimensions(1024, 1024), iterations: int = 35):
        self.image = image
        self.positive_prompt = positive_prompt
        self.negative_prompt = negative_prompt
        self.sampler = sampler
        self.scheduler = scheduler
        self.dimensions = dimensions
        self.set_denoise(denoise)
        self.set_steps(steps)
        self.set_cfg(cfg)
        self.set_iterations(iterations)

    def set_denoise(self, denoise: float):
        if not 0 <= denoise <= 1:
            raise ValueError('"denoise" must be between 0 and 1 (inclusive).')
        self.denoise = denoise

    def set_steps(self, steps: int):
        if steps <= 0:
            raise ValueError('"steps" must be 1 or above.')
        self.steps = steps

    def set_cfg(self, cfg: float):
        if cfg < 0:
            raise ValueError('"cfg" must be positive.')
        self.cfg = cfg

    def set_iterations(self, iterations: int):
        if iterations <= 0:
            raise ValueError('"iterations" must be 1 or above.')
        self.iterations = iterations

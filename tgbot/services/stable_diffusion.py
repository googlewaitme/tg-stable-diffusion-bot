import os

import replicate


class StableDiffusion:
    def __init__(self, replicate_token: str):
        os.environ['REPLICATE_API_TOKEN'] = replicate_token
        self.model = replicate.models.get("prompthero/openjourney")
        self.version = self.model.versions.get(
            "9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb")

        self.width = 768
        self.height = 768
        self.inputs = {
            'prompt': 'lion',
            'width': self.width,
            'height': self.height,
            # 'prompt_strength': 0.8,
            'num_outputs': 1,
            'num_inference_steps': 50,
            'guidance_scale': 6,
            # 'scheduler': "DPMSolverMultistep",
        }

    async def get_image_by_url(self, prompt: str) -> str:
        self.set_prompt(prompt)
        output = self.version.predict(**self.inputs)
        return output[0]

    def set_prompt(self, prompt: str):
        self.inputs['prompt'] = prompt

import os
from openai import OpenAI

_client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

def generate_image(prompt: str):
    """
    Generate an image using the Nebius API.
    :param prompt:
    :return:
    """
    response = _client.images.generate(
        model="black-forest-labs/flux-schnell",
        response_format="b64_json",
        extra_body={
            "response_extension": "png",
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 4,
            "negative_prompt": "",
            "seed": -1
        },
        prompt=prompt
    )
    return response

"""
Generate bizarre Italian-themed character names and prompts, and create images using the Nebius API.
"""
import os
import random
from openai import OpenAI

_client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

# 사물 리스트 (영어, 이탈리아어)
_objects = [
    {"english": "refrigerator", "italian": "Frigo"},
    {"english": "cappuccino cup", "italian": "Cappuccino"},
    {"english": "pizza slice", "italian": "Pizza"},
    {"english": "espresso machine", "italian": "Macchinetta"},
    {"english": "Vespa scooter", "italian": "Vespa"},
    {"english": "fork", "italian": "Forchetta"},
    {"english": "sofa", "italian": "Divano"},
    {"english": "chandelier", "italian": "Lampadario"},
    {"english": "Colosseum", "italian": "Colosseo"},
    {"english": "Leaning Tower of Pisa", "italian": "Torre"},
    {"english": "gondola", "italian": "Gondola"},
]

# 이름의 두 번째 부분(동물/역할)
_name_suffixes = [
    # 동물 (Animal)
    {"type": "animal", "english": "shark", "italian": "Squalo"},
    {"type": "animal", "english": "camel", "italian": "Cammello"},
    {"type": "animal", "english": "cat", "italian": "Gatto"},
    {"type": "animal", "english": "frog", "italian": "Rana"},
    {"type": "animal", "english": "bear", "italian": "Orso"},
    {"type": "animal", "english": "pigeon", "italian": "Piccione"},
    {"type": "animal", "english": "crocodile", "italian": "Coccodrillo"},
    {"type": "animal", "english": "octopus", "italian": "Polpo"},
    {"type": "animal", "english": "capybara", "italian": "Capibara"},
    # 역할 (Role)
    {"type": "role", "english": "assassin", "italian": "Assassino"},
    {"type": "role", "english": "doctor", "italian": "Dottore"},
    {"type": "role", "english": "ghost", "italian": "Fantasma"},
    {"type": "role", "english": "champion", "italian": "Campione"},
    {"type": "role", "english": "godfather", "italian": "Padrino"},
    {"type": "role", "english": "king", "italian": "Re"},
]

# --- 2. 프롬프트 구성을 위한 요소들 ---

# 행동 (Actions)
_actions = [
    "doing the griddy on a table",
    "aggressively making the 🤌 hand gesture at a pigeon",
    "trying to cook spaghetti in a coffee maker",
    "staring menacingly into the camera",
    "slipping on a banana peel in slow motion",
    "crying profusely, tears made of olive oil",
    "trying to fit into a tiny Fiat 500",
    "furiously playing an accordion",
    "looking lost in a supermarket",
]

# 장소 (Locations)
_locations = [
    "in a flooded St. Peter's Square",
    "on top of a giant, spinning wheel of parmesan cheese",
    "in a liminal, empty backroom of a pizzeria",
    "inside a low-poly Roman Colosseum",
    "on a Windows XP-style grassy hill under a blood moon",
    "in a Venetian canal filled with tomato sauce",
    "at a desolate gas station in the middle of the Tuscan countryside",
    "during a chaotic family dinner",
]

# 디테일/액세서리 (Details / Accessories)
_details = [
    "wearing oversized, knock-off Gucci sunglasses",
    "wearing bright blue sneakers",
    "with a tiny, crooked chef's hat",
    "covered in mysterious marinara sauce stains",
    "glowing with a faint, holy light",
    "glitching in and out of existence",
    "holding a single, perfect meatball",
    "all its fins are wearing tiny Nike sneakers",
]

# 시각 스타일 (Visual Styles)
_styles = [
    "italian brainrot style",
    "surrealism",
    "bizarre",
    "cursed image",
    "deep fried meme",
    "low-poly 3D render",
    "PS2 game graphics",
    "found footage from a 2004 camcorder",
    "glitch art",
    "shot on a nokia phone camera",
    "heavy chromatic aberration",
    "oversaturated colors",
    "weirdcore aesthetic",
]


def generate_italian_brainrot():
    """
    Generate a bizarre Italian-themed character name and prompt.
    :return: (name, prompt)
    """
    selected_object = random.choice(_objects)
    selected_suffix = random.choice(_name_suffixes)

    name = f"{selected_object['italian']} {selected_suffix['italian']}"
    if selected_suffix['type'] == 'animal':
        character_description = (
            f"a bizarre hybrid of a sentient {selected_object['english']} "
            f"and a {selected_suffix['english']}, a creature known as '{name}'"
        )
    else:  # type == 'role'
        character_description = (
            f"a living, anthropomorphic {selected_object['english']} "
            f"dressed as an Italian {selected_suffix['english']}, the infamous '{name}'"
        )

    action = random.choice(_actions)
    location = random.choice(_locations)

    detail_str = ""
    if random.random() < 0.8:
        detail_str = ", " + random.choice(_details)
    num_additional_styles = 2
    base_styles = ["italian brainrot style", "surrealism", "bizarre"]
    additional_styles = random.sample([s for s in _styles if s not in base_styles],
                                      num_additional_styles)
    style_str = ", ".join(base_styles + additional_styles)
    prompt = f"{character_description}, {action}{detail_str}, {location}, {style_str}"

    return name, prompt

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
            "num_inference_steps": 1,
            "negative_prompt": "",
            "seed": -1
        },
        prompt=prompt
    )
    return response

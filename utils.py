import os
import random

def ensure_output_dir(directory):
    os.makedirs(directory, exist_ok=True)
    return directory

def get_seed(seed_text):
    return int(seed_text) if seed_text else random.randint(0, 1000000)
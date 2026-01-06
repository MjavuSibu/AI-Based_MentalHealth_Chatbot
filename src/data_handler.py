import json
import pandas as pd

def load_intents(path="data/raw/intents.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = []
    labels = []
    responses = {}

    for item in data["intents"]:
        tag = item["tag"]
        responses[tag] = item["responses"]
        for pattern in item["patterns"]:
            if pattern.strip():
                texts.append(pattern.lower().strip())
                labels.append(tag)

    return texts, labels, responses
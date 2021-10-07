import json
from pathlib import Path
from typing import List
from model.card import Card


def parse_spec(path: Path):
    with path.open() as src:
        spec = json.load(src)
        cards: List[Card] = []
        for item in spec:

            cards.append(Card(item['id'], item['image']))

        return cards

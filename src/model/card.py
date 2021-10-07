from dataclasses import dataclass
from pathlib import Path


@dataclass
class Card:
    id: str
    image_source: Path

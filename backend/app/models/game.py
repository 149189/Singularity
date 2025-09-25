from pydantic import BaseModel
from typing import Dict, List, Optional  # Ensure imports are correct
from datetime import datetime

class PlayerAttributes(BaseModel):
    strength: int = 1
    agility: int = 1
    vitality: int = 1
    intelligence: int = 1
    available_points: int = 0

class LevelProgression(BaseModel):
    level: int = 1
    experience: int = 0
    experience_to_next_level: int = 100

class Quest(BaseModel):
    id: str
    title: str
    description: str
    quest_type: str  # "daily", "weekly", "story"
    requirements: Dict[str, int]  # {"pushups": 50, "squats": 30}
    rewards: Dict[str, int]  # {"exp": 100, "gold": 50}
    is_completed: bool = False

class Item(BaseModel):
    id: str
    name: str
    item_type: str  # "weapon", "armor", "potion"
    attributes: Dict[str, int]  # {"strength": 5}
    rarity: str  # "common", "rare", "epic"
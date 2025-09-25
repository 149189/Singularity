from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
from enum import Enum

class ExerciseType(str, Enum):
    STRENGTH = "strength"
    AGILITY = "agility" 
    VITALITY = "vitality"
    INTELLIGENCE = "intelligence"

class ExerciseBase(BaseModel):
    name: str
    exercise_type: ExerciseType
    base_exp: int
    description: str

class Exercise(ExerciseBase):
    id: str

class ExerciseCreate(BaseModel):
    exercise_id: str
    reps: Optional[int] = None
    sets: Optional[int] = None
    duration_minutes: Optional[int] = None
    weight_kg: Optional[float] = None

class ExerciseLog(ExerciseCreate):
    id: str
    user_id: str
    completed_at: datetime
    experience_gained: int
    attributes_gained: Dict[str, int] = {}
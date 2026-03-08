from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Mundial:
    año: int
    sede: str
    campeón: str
    subcampeón: str = ""

class MundialesData:
    def __init__(self):
        self.mundiales: List[Dict[str, Any]] = []
        self.partidos: List[Dict[str, Any]] = []

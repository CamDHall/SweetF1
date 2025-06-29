from dataclasses import dataclass
from fastf1.core import Telemetry

@dataclass
class DriverRaceData:
    name: str
    qual_session: Telemetry
    race_session: Telemetry
    practice_session_1: Telemetry | None = None
    practice_session_2: Telemetry | None = None
    practice_session_3: Telemetry | None = None

    def __init__(self, name, p1, p2, p3, q, r):
        self.name = name
        self.practice_session_1 = p1
        self.practice_session_2 = p2
        self.practice_session_3 = p3
        self.qual_session = q
        self.race_session = r
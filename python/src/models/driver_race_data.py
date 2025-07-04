from dataclasses import dataclass
from fastf1.core import Telemetry

from models.session_telemetry_data import SessionTelemetryData

@dataclass
class DriverRaceData:
    name: str
    qual_session: SessionTelemetryData
    race_session: SessionTelemetryData
    practice_session_1: SessionTelemetryData | None = None
    practice_session_2: SessionTelemetryData | None = None
    practice_session_3: SessionTelemetryData | None = None

    def __init__(self, name, p1, p2, p3, q, r):
        self.name = name
        self.practice_session_1 = p1
        self.practice_session_2 = p2
        self.practice_session_3 = p3
        self.qual_session = q
        self.race_session = r
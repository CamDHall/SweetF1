from dataclasses import dataclass
from enum import Enum

from models.session_telemetry_data import SessionTelemetryData

class SessionName(Enum):
    P_1 = "practice_1"
    P_2 = "practice_2"
    P_3 = "practice_3"
    Q = "qualifying"
    R = "race"

@dataclass
class DriverRaceData:
    name: str
    session_name: SessionName
    session: SessionTelemetryData

    def __init__(self, name, session_name, session):
        self.name = name
        self.session_name = session_name
        self.session = session
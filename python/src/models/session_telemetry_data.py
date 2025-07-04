from dataclasses import dataclass
from fastf1.core import Telemetry

@dataclass
class RacePositionData:
    date: str
    time: str
    x: float
    y: float
    z: float

@dataclass
class SessionTelemetryData:
    position: RacePositionData
    speed: float
    rpm: float
    gear: int
    brake: float
    throttle: float
    drs: bool

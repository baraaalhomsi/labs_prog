from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Hit:
    damage: int
    critical: bool = False


class Side(Enum):
    HERO = "hero"
    ENEMY = "enemy"


class EventType(Enum):
    HIT = "hit"
    CRITICAL_HIT = "critical_hit"
    DEATH = "death"


class Outcome(Enum):
    VICTORY = "victory"
    DEFEAT = "defeat"


@dataclass(frozen=True)
class BattleEvent:
    round: int
    type: EventType
    source: Side
    target: Side
    amount: int
    target_health_after: int


@dataclass(frozen=True)
class Participant:
    code: str
    name: str
    max_health: int

    @staticmethod
    def of(combatant):
        return Participant(combatant.code, combatant.name, combatant.max_health)


@dataclass(frozen=True)
class BattleReport:
    hero: Participant
    enemy: Participant
    outcome: Outcome
    events: tuple[BattleEvent, ...]

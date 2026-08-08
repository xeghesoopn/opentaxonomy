from typing import Optional
from pydantic import BaseModel

class EdgeCase(BaseModel):
    term: str
    resolution: str
    decided: bool

class NodeCriteria(BaseModel):
    includes: list[str] = []
    excludes: list[str] = []

class DecisionRecord(BaseModel):
    criterion_chosen: str
    alternatives_considered: list[str]
    reason: str

class Node(BaseModel):
    node: str
    canonical_id: str
    criteria: NodeCriteria
    parent: Optional[str]
    question: str = ""
    children: list[str] = []
    edge_cases: list[EdgeCase] = []
    decision_record: Optional[DecisionRecord] = None

class PlacementEntity(BaseModel):
    normalized: str
    definition: Optional[str]
    raw_samples: list[str] = []

class Placement(BaseModel):
    canonical_id: str
    entities: list[PlacementEntity]

class UnresolvedValue(BaseModel):
    raw: str
    reason: str

class PlacementMap(BaseModel):
    seed_id: str
    seed_version: str
    generated: str
    placements: list[Placement]
    unresolved: list[UnresolvedValue] = []

class SeedContext(BaseModel):
    Q0_answer: str
    Q0b_answer: str

class SeedLevel(BaseModel):
    dimension: str
    question: str
    branches: list[str]

class Seed(BaseModel):
    seed_id: str
    description: str
    context: SeedContext
    normalization_rules: dict[str, bool]
    levels: dict[str, SeedLevel] = []
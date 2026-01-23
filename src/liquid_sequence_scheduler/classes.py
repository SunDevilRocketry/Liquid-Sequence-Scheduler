from dataclasses import dataclass

@dataclass
class Hardware:
    name: str

    def __hash__(self):
        return hash(self.name)

@dataclass
class Command:
    name: str

    def __hash__(self):
        return hash(self.name)

@dataclass
class SequenceLine:
    line: int
    time: float
    parameter: str
    switch: str

@dataclass
class SequenceNode:
    num: int
    time: float
    parameter: Command | Hardware
    switch: bool

@dataclass
class SyntaxCheck:
    result: bool
    line: int
    message: str
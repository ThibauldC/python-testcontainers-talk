from dataclasses import dataclass


@dataclass
class Book:
    id: int
    title: str
    score: int

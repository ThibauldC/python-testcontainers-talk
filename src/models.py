from dataclasses import dataclass


@dataclass
class Book:
    id: int
    title: str
    rating: int

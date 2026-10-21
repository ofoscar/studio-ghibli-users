from enum import Enum


class GhibliResource(str, Enum):
    films = "films"
    people = "people"
    locations = "locations"
    species = "species"
    vehicles = "vehicles"
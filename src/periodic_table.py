from json import load
from pathlib import Path

# References:
# Atomic radii: 10.1063/1.1725697
# Color: CPK variant jmol


class PeriodicTable:
    def __init__(self):
        self.elements = {}

    def __getitem__(self, symbol):
        if symbol not in self.elements:
            self.elements.update({symbol: Element(symbol)})

        return self.elements[symbol]


class Element:
    def __init__(self, symbol):
        self.parse(self.load(symbol))

    def load(self, symbol):
        with open(Path(__file__).parent / "resources" / "elements.json") as file:
            data = load(file)

        for element in data:
            if element["symbol"] == symbol:
                return element

        raise KeyError("Element not defined.")

    def parse(self, data):
        self.name = data["name"]
        self.symbol = data["symbol"]
        self.radius = data["radius"]
        self.covalent_radius = data["covalent radius"]


PeriodicTable = PeriodicTable()

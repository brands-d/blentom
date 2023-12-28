# References:
# Atomic radii: 10.1063/1.1725697
# Color: CPK variant jmol

from dataclasses import dataclass
from json import load
from blentom.material import Material

# elements = {
#     "H": {"radius": 0.25, "color": "#FFFFFF"},
#     "C": {"radius": 0.70, "color": "#909090"},
#     "N": {"radius": 0.65, "color": "#3750EF"},
#     "Ni": {"radius": 1.35, "color": "#75CD61"},
# }


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
        with open("elements.json") as file:
            data = load(file)

        for element in data:
            if element["symbol"] == symbol:
                return element

        raise KeyError("Element not defined.")

    def parse(self, data):
        self.symbol = data["symbol"]
        self.radius = data["radius"]
        self.covalent_radius = data["covalent radius"]
        self.material = Material.pre_defined(self.symbol)


PeriodicTable = PeriodicTable()

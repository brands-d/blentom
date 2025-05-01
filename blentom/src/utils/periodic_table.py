from json import load
from shutil import copy
from os.path import exists

from .. import __default_directory__, __user_directory__


class PeriodicTable:
    """
    A class representing the periodic table. Mainly for internal use to avoid reloading elements over and over again.
    """

    elements = {}

    @classmethod
    def get(cls, symbol, load=False):
        """
        Retrieves an element from the periodic table by its symbol.

        Args:
            symbol (str): The symbol of the element.
            load (bool): Force updating existing elements.

        Returns:
            Element: The element object corresponding to the symbol.
        """
        if load or symbol not in cls.elements:
            cls.elements.update({symbol: Element(symbol)})

        return cls.elements[symbol]

    @classmethod
    def reload(cls):
        """
        Reloads the periodic table by clearing the existing elements.
        """
        cls.elements = {}


class Element:
    """
    A class representing an element in the periodic table.

    Attributes:
        name (str): The name of the element (i.e. Hydrogen).
        symbol (str): The symbol of the element (i.e. H).
        radius (float): The radius of the element in Angstrom. Default is half of the covalent radius.
        covalent_radius (float): The covalent radius of the element in Angstrom. Source: https://en.wikipedia.org/wiki/Covalent_radius.
    """

    elements_default_file = __default_directory__ / "elements.json"
    elements_user_file = __user_directory__ / "elements_user.json"

    def __init__(self, symbol):
        """
        Initializes an instance of the Element class.

        Args:
            symbol (str): The symbol of the element.
        """
        self.parse(self.load(symbol))

    def load(self, symbol):
        """
        Loads the element data from the JSON file(s). User file is preferred.

        Note:
            If unknown element is loaded, it will default to the element with dummy element called Veritasium with the symbol "X".

        Args:
            symbol (str): The symbol of the element.

        Returns:
            dict: The element data as a dictionary.
        """
        try:
            element = self._read(symbol, user=True)
        except KeyError:
            element = self._read(symbol, user=False)

        return element

    def _read(self, symbol, user=True):
        """
        Reads element data from a elements file based on the given chemical symbol.
        Args:
            symbol (str): The chemical symbol of the element to look up.
            user (bool, optional): If True, reads from the user-defined elements file.
                If False, reads from the default elements file. Defaults to True.
        Returns:
            dict: A dictionary containing the data of the element with the specified symbol.
        Raises:
            KeyError: If the element with the specified symbol is not found in the file.
        """
        if user:
            Element.ensure_user_file()
            path = Element.elements_user_file
        else:
            Element.elements_default_file

        with open(path) as file:
            data = load(file)

        for element in data:
            if element["symbol"] == symbol:
                return element

        raise KeyError

    def parse(self, data):
        """
        Parses the element data and assigns the attributes.

        Args:
            data (dict): The element data as a dictionary.
        """
        self.name = data["name"]
        self.symbol = data["symbol"]
        self.radius = data["radius"]
        self.covalent_radius = data["covalent radius"]

    @classmethod
    def _check_user_file_exists(cls):
        """
        Checks if the user-defined elements file exists.

        Returns:
            bool: True if the user-defined elements file exists, False otherwise.
        """
        return exists(cls.elements_user_file)

    @classmethod
    def ensure_user_file(cls):
        """
        Ensures the existence of the user-specific elements file.

        This method checks if the user-specific elements file exists. If it does not,
        it creates the file by copying the default elements file to the user-specific
        location.
        """
        if not cls._check_user_file_exists():
            copy(cls.elements_default_file, cls.elements_user_file)

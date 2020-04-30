from inventory import Inventory


class Room(object):
    """
    Representation of a room in Adventure
    """

    def __init__(self, id, name, description):
        """
        Initialize a Room
        give it an id, name and description
        """
        self.id = id
        self.name = name
        self.description = description
        self.connection = {}
        self.inventory = Inventory()

    def __str__(self):
        return (f"{self.id} {self.name} {self.description}")

    def isvalid(self, direction):
        """
        Check if command is a valid direction
        """
        if direction in self.connection:
            return True
        else:
            return False
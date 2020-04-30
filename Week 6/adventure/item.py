class Item(object):
    """
    Representation of an item in Adventure
    """

    def __init__(self, name, description, initial_room_id):
        """
        Initialize an Item
        give it a name, description and initial location
        """
        self.name = name
        self.description = description
        self.initial_room_id = initial_room_id

    def __str__(self):
        return (f"{self.name} {self.description} {self.initial_room_id}")
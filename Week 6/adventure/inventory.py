class Inventory(object):
    """
    Representation of the inventory in Adventure
    """

    def __init__(self):
        """
        Initialize the inventory
        give it the items
        """
        self.itemlist = []

    def add(self, item):
        """
        Add item to inventory
        """
        self.itemlist.append(item)

    def remove(self, item_name):
        """
        Remove item from inventory
        """
        item = None

        # Get full item from itemname
        for items in self.itemlist:
            if item_name == items.name:
                item = items

        # Remove item if possible
        if item is not None:
            self.itemlist.remove(item)
            return item
        else:
            return None

    def __str__(self):
        return (f"{self.itemlist}")

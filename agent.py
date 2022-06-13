from collections    import Counter
from random         import randint
class Agent:
    """ constructor ::
            <String>    -> agent id
            <Integer>   -> agent inventory size
        description ::
            base agent class, hold essential game interaction functions
    """
    def __init__(self, agent_id, initial_inventory_size):
        self.agent_id   = agent_id

        self.inventory      = []
        self.inventory_size = initial_inventory_size
    
    def __str__(self):
        return "AGENT{}".format(self.agent_id)

    def roll(self, inventory_type):
        """ input ::
                <List>      -> items to count in inventory
            output ::
                <Integer>   -> total items matched in inventory
            description ::
                agent counts all items in inventory and returns count
        """
        self.inventory.clear()

        self.inventory  = [randint(1,inventory_type) for item in range(self.inventory_size)] 

    def count(self, items):
        """ input ::
                <List>      -> items to count in inventory
            output ::
                <Integer>   -> total items matched in inventory
            description ::
                agent counts all items in inventory and returns count
        """
        ans = 0

        try:
            for item in self.inventory:
                if item in items:
                    ans += 1

        
        except TypeError:
            for item in self.inventory:
                if item == items:
                    ans += 1

        return ans

    def lose(self):
        """ input ::
                none
            output ::
                <Boolean>   -> true if agent has lost
            description ::
                agent loses a item, then returns true if agent has no inventory
        """
        self.inventory_size = self.inventory_size - 1

        return self.inventory_size < 1
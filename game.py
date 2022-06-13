from random import randint
from random import shuffle
class Game:
    """ constructor ::
            <List>      -> list of initial agents
            <Integer>   -> dice type for game (i.e. 6 = six-sided)
            <List>      -> dice values considered 'wildcards'
        description ::
            simulates the game of 'Liar's Dice' with given agents and dice type, game.play() to start
    """
    def __init__(self, initial_agents, inventory_type, wildcard_type):
        self.agents = initial_agents
        shuffle(self.agents)

        self.inventory_size = sum([agent.inventory_size for agent in self.agents])
        self.inventory_type = inventory_type

        self.bid        = None
        self.bid_log    = []

        self.wildcard_type  = [wild for wild in wildcard_type]

    def __str__(self):
        s   =   "This game has {} many agents\n".format(len(self.agents)) + "{}\n".format([str(agent) for agent in self.agents])
        s   +=  "The inventory settings are...\n" + "{} inventory size and inventory type {}\n".format(self.inventory_size, self.inventory_type)
        s   +=  "The wildcard settings are...\n" + "{} as wildcard types\n".format(self.wildcard_type)
        
        return s

    def play(self):
        """ input ::
                none
            output ::
                <Agent>     -> agent in game 
            description ::
                turn by turn game simulation, returns winning agent
        """
        self.reset()

        gameState   = GameState(self)
        curr_turn   = randint(0, len(self.agents)-1)
        while (len(self.agents)) > 1:
            # print(gameState)
            
            curr_agent  = self.agents[curr_turn]

            # print("current turn = ", str(curr_agent))
            # input("...")

            if (curr_agent.call(gameState)) == False:
                curr_bid    = curr_agent.bid(gameState)

                self.setBid(curr_bid)
                curr_turn   = (curr_turn + 1) % len(self.agents)
            
            else:
                # print(str(curr_agent), " is calling")
                # input("...")
                if self.checkBid() is True:
                    # print(str(curr_agent), " was incorrect")

                    if curr_agent.lose():
                        # print(str(curr_agent), " has lost")

                        self.agents.remove(curr_agent)
                        curr_turn   = (curr_turn - 1) % len(self.agents)
                    else:
                        curr_turn   = curr_turn

                else:
                    # print(str(curr_agent), " was correct")

                    prev_turn   = (curr_turn - 1) % len(self.agents)
                    prev_agent  = self.agents[prev_turn]

                    if prev_agent.lose():
                        # print(str(prev_agent), " has lost")

                        self.agents.remove(prev_agent)
                        curr_turn   = (prev_turn - 1) % len(self.agents)
                        # input("...")
                    else:
                        curr_turn   = prev_turn

                # input("...")
                self.inventory_size = self.inventory_size - 1
                self.reset()

            gameState.update(self)

        return self.agents[0]

    def reset(self):
        """ input ::
                none
            output ::
                none
            description ::
                resets current game bid and rerolls inventory for each agent in game
        """
        self.bid        = None
        self.bid_log    = []
        
        for agent in self.agents:
            agent.roll(self.inventory_type)

    def setBid(self, curr_bid):
        """ input ::
                none
            output ::
                none
            description ::
                sets game bid to given current bid
        """
        if GameState.isBidLegal(GameState(self), curr_bid) is False:
            raise Exception(">> ERROR: Illegal bid has been passed to game")

        self.bid    = curr_bid

        self.bid_log.append(curr_bid)

    def checkBid(self):
        """ input ::
                none
            output ::
                <Boolean>   -> true if current game bid is valid
            description ::
                determines if current game bid is true
        """
        type_s  = [wild for wild in self.wildcard_type]
        type_s.append(self.bid[1])

        return sum([agent.count(type_s) for agent in self.agents]) >= self.bid[0]

class GameState:
    """ constructor ::
            <List>      -> list of initial agents
            <Integer>   -> dice type for game (i.e. 6 = six-sided)
            <List>      -> dice values considered 'wildcards'
        description ::
            simulates the game of 'Liar's Dice' with given agents and dice type, game.play() to start
    """
    def __init__(self, game):
        self.inventory_size = game.inventory_size
        self.inventory_type = game.inventory_type
        
        self.curr_bid   = game.bid
        self.bid_log    = game.bid_log

        self.wildcard_type  = game.wildcard_type

        self.type_s = [wild for wild in game.wildcard_type]

    def __str__(self):
        s   =   "Current game state...\n"
        s   +=  "inventory size = {}\n".format(self.inventory_size)
        s   +=  "current bid = {}\n".format(self.curr_bid)

        return s

    def update(self, game):
        """ input ::
                <GameState> -> current game state
            output ::
                none
            description ::
                updates current game state variables to match game
        """
        self.inventory_size = game.inventory_size

        self.curr_bid   = game.bid
        self.bid_log    = game.bid_log


        self.type_s = [wild for wild in game.wildcard_type]
        if self.curr_bid is not None:
            self.type_s.append(self.curr_bid[1])

    def mininumBid(self):
        """ input ::
                none
            output ::
                <Tuple>     -> bid
            description ::
                returns the smallest possible bid an agent must make
        """
        min_type    = min(set([i for i in range(1, self.inventory_type+1)]) - set(self.wildcard_type))

        if self.curr_bid is None:
            return (1,min_type)

        if self.curr_bid[1] == self.inventory_type:
            return (self.curr_bid[0] + 1, min_type)
        
        return (self.curr_bid[0], self.curr_bid[1]+1)

    def bidsInRange(self, bid_index_1, bid_index_2):
        """ input ::
                <Tuple>     -> bid index 1 (starting index)
                <Tuple>     -> bid index 2 (ending index)
            output ::
                <List>      -> bids within range
            description ::
                returns list of valid bids within a range of two bids
        """
        bids_in_range = []

        bid_size, bid_type = bid_index_1[0], bid_index_1[1]

        while (bid_size, bid_type) != bid_index_2:
            bid = (bid_size, bid_type)

            if self.isBidLegal(bid):
                bids_in_range.append(bid)

            if bid_type == self.inventory_type:
                if (bid_size, bid_type) == bid_index_2:
                    break
                
                bid_size += 1
                bid_type = 1
            else:
                bid_type += 1

        return bids_in_range

    def isBidPossible(self, bid):
        """ input ::
                none
            output ::
                <Boolean>   -> true if bid is possible
            description ::
                determines if current game bid is possible
        """
        if self.curr_bid is None and bid is None:
            return True
        return bid[0] <= self.inventory_size
        
    def isBidLegal(self, bid):
        """ input ::
                none
            output ::
                <Boolean>   -> true if bid is legal
            description ::
                determines if potential game bid is legal
        """
        min_type    = min(set([i for i in range(1, self.inventory_type+1)]) - set(self.wildcard_type))

        if bid[1] < min_type or bid[1] > self.inventory_type:
            return False

        if bid[0] < 1:
            return False
        
        if self.curr_bid is not None:
            if bid[1] in self.wildcard_type or bid[1] == self.curr_bid[1]:
                return False
            
            if bid[0] < 1 or bid[0] < self.curr_bid[0]:
                return False

            if bid[0] == self.curr_bid[0] and bid[1] < self.curr_bid[1]:
                return False

        return True
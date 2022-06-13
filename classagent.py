from agent  import Agent

class DefaultAgent(Agent):
    """ constructor ::
            <String>    -> agent id
            <Integer>   -> agent inventory size
        description ::
            agent has simple increment bid and fail-proof call methods
    """
    def __init__(self, agent_id, initial_inventory_size):
        Agent.__init__(self, agent_id, initial_inventory_size)

    def __str__(self):
        return "DEFAULT{}".format(self.agent_id)

    def bid(self, gameState):
        """ input ::
                <GameState> -> current game state
            output ::
                <Tuple>     -> bid from agent
            description ::
                agent returns current game bid, incremented by +(0,1)
        """
        return gameState.mininumBid()

    def call(self, gameState):
        """ input ::
                <GameState> -> current game state
            output ::
                <Boolean>   -> true if agent will call
            description ::
                agent will call if bid is impossible
        """
        return gameState.isBidPossible(gameState.curr_bid) is False
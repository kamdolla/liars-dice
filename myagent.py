from agent  import Agent
from util   import binomial_dist

class ProbabilityAgent(Agent):
    """ constructor ::
            <String>    -> agent id
            <Integer>   -> agent inventory size
            <Float>     -> probability bound for agent call method
            <Float>     -> probability bound for agent bid method
        description ::
            agent utilizes binomial distribution to calculate probabiltiy of a given bid, then determines bid or call based on inputted probability bounds
    """
    def __init__(self, agent_id, initial_inventory_size, prob_to_bid, prob_to_call):
        Agent.__init__(self, agent_id, initial_inventory_size)

        self.prob_to_bid    = prob_to_bid
        self.prob_to_call   = prob_to_call

    def __str__(self):
        return "PROB{}".format(self.agent_id)

    def bid(self, gameState):
        """ input ::
                <GameState> -> current game state
            output ::
                <Tuple>     -> bid from agent
            description ::
                agent calculates highest probability and sized bid using binomial distribution
        """
        return gameState.mininumBid()

    def call(self, gameState):
        """ input ::
                <GameState> -> current game state
            output ::
                <Boolean>   -> true if agent will call
            description ::
                agent uses binomial distribution to calculate probability of current game bid, returns true if probability falls below inputted probability to call bound
        """
        if gameState.curr_bid is None:
            return False
        
        return self.bidProbability(gameState, gameState.curr_bid) < self.prob_to_call

    def bidProbability(self, gameState, bid):
        """ input ::
                <GameState> -> current game state
                <Tuple>     -> bid from agent
            output ::
                <Float>     -> probability of bid
            description ::
                determines probability of given bid from agent in current game state
        """
        type_s      = [wild for wild in gameState.wildcard_type]
        type_s.append(bid[1])

        known_s     = self.count(type_s)
        desired_s   = bid[0]
        
        trials          = gameState.inventory_size
        probability_s   = 1/gameState.inventory_type

        return binomial_dist(known_s, desired_s, trials, probability_s, type_s)


class PickyBidder(ProbabilityAgent):
    """ constructor ::
            <String>    -> agent id
            <Integer>   -> agent inventory size
            <Float>     -> probability bound for agent call method
            <Float>     -> probability bound for agent bid method
        description ::
            agent utilizes binomial distribution to calculate probabiltiy of a given bid, then determines bid or call based on inputted probability bounds
                modified bid >> agent calculates smallest bid within probability bound, or smallest highest probability bid if none exists
    """
    def __str__(self):
        return "PICKY{}".format(self.agent_id)

    def bid(self, gameState):
        """ input ::
                <GameState> -> current game state
            output ::
                <Tuple>     -> bid from agent
            description ::
                agents chooses bid with highest probability in bounds, with the lowest bid size
        """
        mininum_bid = gameState.mininumBid()

        if gameState.curr_bid is None:
            return mininum_bid

        small_bid   = self.smallestProbableBid(gameState, mininum_bid, self.prob_to_bid)

        return small_bid

    def smallestProbableBid(self, gameState, bid_index_1, prob_to_bid):
        """ input ::
                <GameState> -> current game state
                <Tuple>     -> bid index 1 (starting index)
                <Float>     -> probability bound for agent bid method
            output ::
                <Tuple>     -> bid with smallest bid size such that probability > prob_to_bid, most probable bid if none exists
            description ::
                returns the bid with smallest bid size with probability > prob_to_bid, or most probable bid if none exists
        """
        bid_index_2 = (bid_index_1[0]+1, gameState.inventory_type)

        bids_in_range = gameState.bidsInRange(bid_index_1, bid_index_2)

        small_bid       = bid_index_1
        small_bid_prob  = self.bidProbability(gameState, small_bid)

        if small_bid_prob >= prob_to_bid:
            return small_bid

        for bid in bids_in_range:
            bid_prob = self.bidProbability(gameState, bid)

            if bid_prob > small_bid_prob:
                small_bid, small_bid_prob = bid, bid_prob

            if small_bid_prob > prob_to_bid:
                return small_bid

        return small_bid
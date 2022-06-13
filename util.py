from scipy.stats import binom

def binomial_dist(known_s, desired_s, trials, probability_s, type_s) -> float:
    """ input       ::
            Integer     -> number of known successes (i.e. known_s = agent.count(for type in type_s))
            Integer     -> number of desired successes (i.e. bid size)
            Integer     -> number of trials (i.e. total number of dice)
            Float       -> probability of ONE success type (i.e. 1/6 for a six-sided die, 1/4 for a four-sided die))
            List        -> list of valid success types (i.e. type_s = [bid_type + wildcard_type])

        output      ::
            Float       -> probability that at least desired_s successes of type_s exist within trials, given some known_s successes

        description ::
            uses binomial distribution to calculate: 
                probability that at least number_s successes of type_s exist within trials
            (useful for myagent.py class!)
    """
    return 1 - binom.cdf(k=(desired_s - known_s)-1, n=trials, p=(len(type_s)*probability_s))
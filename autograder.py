from game       import  Game
from agent      import  Agent
from classagent import  DefaultAgent as DAgent
from myagent    import  ProbabilityAgent as PAgent
from myagent    import  PickyBidder as PAgent_PB

agent_size      = 5

inventory_size  = 5
inventory_type  = 6
wildcard_type   = [1]

prob_to_bid     = 0.5
prob_to_call    = 0.5

tests           = 10
trials          = 100

def problem0():
    global agent_size
    global inventory_size, inventory_type, wildcard_type
    global prob_to_bid, prob_to_call

def problem1():
    student_agent_wins  = 0
    student_agent       = PAgent_PB(str(), inventory_size, prob_to_bid, prob_to_call)

    initial_agents  = [DAgent(str(i), inventory_size) for i in range(agent_size-1)]
    initial_agents.append(student_agent)

    scores  = {agent : 0 for agent in initial_agents}

    for test in range(tests):
        student_agent       = PAgent_PB(str(), inventory_size, prob_to_bid, prob_to_call)

        initial_agents.clear()
        initial_agents  = [DAgent(str(i), inventory_size) for i in range(agent_size-1)]
        initial_agents.append(student_agent)

        scores.clear()
        scores  = {str(agent) : 0 for agent in initial_agents}

        for trial in range(trials):
            initial_agents.clear()
            initial_agents  = [DAgent(str(i), inventory_size) for i in range(agent_size-1)]
            initial_agents.append(PAgent_PB(str(), inventory_size, prob_to_bid, prob_to_call))
            # input("...")

            game    = Game(initial_agents, inventory_type, wildcard_type)
            winner  = game.play()

            scores[str(winner)] += 1

        student_agent_wins += scores[str(student_agent)]
        print(scores)

    print("Student agent {} has a win percentage of {}".format(str(student_agent), student_agent_wins/(tests*trials)))

if __name__ == "__main__":
    problem0()
    problem1()
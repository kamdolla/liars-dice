# Advesarial Methods – Liar's Dice

Implementing advesarial learning agents to play in the game of *Liar's Dice*–– a dice rolling game involving bidding and bluffing.

Simulates the game of *Liar's Dice* with standard 5-player game rules. Can modify game rules in **autograder.py**.

Includes code for agent template and dummy agent, as well as model for agents utilizing binomial distribution to determine bid probability.

Final research project for *COSC-454 Seminar in Computer Science: Adversarial Methods* at Amherst College and self-designed course project for Artificial Intelligence class.

## Usage

Download the codebase, and run the **autograder.py** to see student agent performance against default agents.

Modify global variables in **autograder.py** to observer different game settings:

```
# number of agents in game instance
agent_size      = 5

# initial inventory size for agents, die type (i.e. 6 = six-sided die), and list of wildcard dice type
inventory_size  = 5
inventory_type  = 6
wildcard_type   = [1]

# for student agents, probability for agent to make a bid or call
prob_to_bid     = 0.5
prob_to_call    = 0.5
```

## Contents

Codebase is composed of several .py files–– which include game simulation, default agents, student agents, and helper functions.

**autograder.py**

As described above, run this file to initiate game simulation–– or edit global variables to observe different game settings.

Also will include grading options for student agents, determining how proficent a student-made agent performs.

**agent.py**

Class includes base object for all other agent objects to inherit. Methods here are neccesary for game function interactions:

```
def roll(inventory_type):
    # rerolls current inventory dice with desired inventory type

def count(items):
    # returns count of items in inventory

def lose():
    # agents loses 1 item, returns true if agent is eliminated
```

Student created agents should not use roll() or lose() functions, but may use count().

**game.py**

Class includes game simulation object, and game state object. Game state object keeps track of current game variables, like current bid and total inventory size in game, but also is used for privacy concerns (i.e. agents should not have direct access to game variables).

Game state object also contains useful functions that agents can utilize, like returning the mininum bid possible given current game state.

Game simulation object passes game state object to agents, agents are expected to utilize game state for any bidding and calling methodology.

**classagent.py**

Class includes any default agents designed for testing purposes or grading purposes.

Further detail of agent model in next description.

**agent.py**

Class includes any student designed agents that will be tested and graded for course project purposes.

In order to make your own agent, these methods must be included and design specifications must be followed:

```
def bid(gameState):
    # must return (int, int) tuple describing agent bid, given current game state

def call(gameState):
    # must return boolean describing if agent will call current bid, given current game state
```

All agents must be required to have bid() and call() functions, as game simulation interactions require these two methods.

**util.py**

Class includes helper functions, like calculating culmalative binomial distribution (look at *ProbabilityAgent* class in **myagent.py**).

## License

[MIT](https://choosealicense.com/licenses/mit/)

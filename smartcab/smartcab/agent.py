
import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env, discount_rate=0.1, epsilon=0.15, epsilon_decay=.99):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.actions = (None, 'forward', 'left', 'right')
        self.Q = {} #hashable Q-Table
        self.default_Q = 0
        self.epsilon = epsilon #controls frequency of random actions [note: not used when implementing epsilon decay]
        self.epsilon_decay = epsilon_decay #decay rate (multiplier) for GLIE
        self.alpha = 1  # learning rate [note: not used when updating/decaying alpha]
        self.initial_alpha = 1 #starting point for alpha-updating model
        self.discount_rate = discount_rate #controls extent to which we value future rewards


        # keep track of net reward, trial no., penalties
        self.net_reward = 0
        self.trial = 0

        self.success = 0
        self.net_penalty = 0
        self.penalty_tracker = []
        self.reward_tracker = []
        self.success_tracker = []
        self.trial_tracker = []

        #initialize Q-table with default values
        for light_state in ['green', 'red']:
            for oncoming_traffic_state in self.actions:
                for right_traffic_state in self.actions: 
                    for left_traffic_state in self.actions: 
                        for waypoint_state in self.actions[1:]: #ignore NONE - this is not a waypoint possibility
                            # record each state
                            state = (light_state, oncoming_traffic_state,
                                    right_traffic_state, left_traffic_state,
                                    waypoint_state)
                            self.Q[state] = {}
                            for action in self.actions:
                                self.Q[state][action] = self.default_Q
    

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.state = None
        self.trial += 1
        self.net_reward = 0
        self.net_penalty = 0

    #for the random agent
    def get_random_action(self, state):
        return random.choice(self.actions)

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (inputs['light'], inputs['oncoming'], inputs['left'],
                      inputs['right'], self.next_waypoint)

        # TODO: Select action according to your policy

        #random agent approach
        #best_action = self.get_random_action(self.state)

        #Q-learning approach
        if random.random() < self.epsilon:  # add randomness to the choice
            best_action = random.choice(self.actions)

        else:
            best_action = None
            max_Q = None
            #find action with best Q value
            for available_action in self.actions:
                if self.Q[self.state][available_action] > max_Q:
                    best_action = available_action
                    max_Q = self.Q[self.state][available_action]

        #EPSILON DECAY. COMMENT OUT FOR INITIAL PARAMETER TUNING 
        self.epsilon = 1 / (self.trial + self.epsilon_decay)

        # Execute action and get reward
        reward = self.env.act(self, best_action)
        self.net_reward += reward

        #successful if reward is large. count this and also store other stats from this trial.
        if reward > 8:
            self.success += 1

        if reward < 0:
            self.net_penalty += reward 

        #if done, update stats
        if self.env.done == True or deadline == 0:
            self.penalty_tracker.append(self.net_penalty)
            self.reward_tracker.append(self.net_reward)
            if deadline == 0:
                self.success_tracker.append(0)
            else:
                self.success_tracker.append(1)
            self.trial_tracker.append(40 - deadline)  #number of turns it took to reach the end

        #if all trials done, show progression of performance indicators over time 
        if self.trial == 100:
            print "net penalties over time: " + str(self.penalty_tracker)
            print "net rewards over time: " + str(self.reward_tracker)
            print "success pattern: " + str(self.success_tracker)
            print "trials required per round: " + str(self.trial_tracker)

        # TODO: Learn policy based on state, action, reward

        #get next state
        next_state = self.env.sense(self) 
        next_waypoint = self.planner.next_waypoint() 

        #re-represent this as a tuple since that's how the Q dict's keys are formatted
        next_state = (next_state['light'], next_state['oncoming'], next_state['left'], next_state['right'], next_waypoint)
        #add state to q dict if not already there
        if next_state not in self.Q:
            self.Q[next_state] = {}
            for next_action in self.actions:
                self.Q[next_state][next_action] = self.default_Q

        utility_of_next_state = None
        #search through available actions, find one with higest Q
        for next_action in self.Q[next_state]:
            if self.Q[next_state][next_action] > utility_of_next_state:
                utility_of_next_state = self.Q[next_state][next_action]

        #next get utility of state
        utility_of_state = reward + self.discount_rate * utility_of_next_state

        # update Q Table
        self.Q[self.state][best_action] = (1 - self.alpha) * \
            self.Q[self.state][best_action] + self.alpha * utility_of_state

        #alpha update. comment this out when testing other inputs in isolation.
        #decay needed to ensure Q convergence. source: http://dreuarchive.cra.org/2001/manfredi/weeklyJournal/pricebot/node10.html
        if self.trial != 0:
            #self.alpha = 1 / (self.trial + self.epsilon_decay)
            num_trials = 100 
            self.alpha = (self.initial_alpha * (num_trials / 10.0)) / ((num_trials / 10.0) + self.trial)

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}, successes = {}".format(deadline, inputs, best_action, reward, self.success)  # [debug]


def run(discount_rate=0.1, epsilon=0.15, epsilon_decay=.99):
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent, discount_rate, epsilon, epsilon_decay)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.000001)  # reduced the delay for a faster simulation
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()

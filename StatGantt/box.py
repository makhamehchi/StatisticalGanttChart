import numpy as np

class Outcome:
    #this class keeps the information of the outcome of a box.
    #It's composed of the probality, time, and money that takes to finish a box.
    def __init__(self, name = 'outcome x', probability=0.1, time=1, money=0):
        self.name = name
        self.probability = probability
        self.time = time #in units of days
        self.money = money #in units of USD - this is separate from workers time compensation.
        # any extra engineering cost will go to self.money here.
    def __str__(self):
        return str('Outcome obj: name=' + self.name + ' p=' + str(self.probability) + ' time=' + str(self.time) +
                   ' money=' + str(self.money))

class Box:
    def __init__(self, name = 'Box x', sufficient = False, outcomes = [], inputboxes = []):
        self.name = name
        self.input = False # this is the input of the box. it true it means that tast is started
        self.output = False # when output is true, it means that the task is done and next activity can start
        self.outcomes = outcomes # this is a list of outcomes
        self.outcome_picked = False #shows wheather an outcome is picked or not.
        self.renormalize_outcomes()
        self.counter_time = 0 # the time elapsed since stated
        self.time = 0 # time expected for the project to be finished
        self.money = 0
        self.sufficient = sufficient # if true, it will be enough to trigger the next item.
        self.input_boxes = inputboxes
        self.output_boxes = []

    def renormalize_outcomes(self):
        sum_probabilities = 0
        self.outcome_probabilities = []
        for outcome in self.outcomes:
            sum_probabilities += outcome.probability
        if sum_probabilities-1 > 1e-6:
            print("Sum of probabilities of ", outcome.name, " is more than 1. Renormalizing.")
        elif sum_probabilities-1 < -1e-6:
            print(sum_probabilities)
            print("Sum of probabilities of ", outcome.name, " is less than 1. Renormalizing.")
        for outcome in self.outcomes:
            outcome.probability = outcome.probability/sum_probabilities
            self.outcome_probabilities.append(outcome.probability)

    def pick_an_outcome(self):
        i = np.random.choice(len(self.outcomes), p=self.outcome_probabilities)
        self.the_outcome = self.outcomes[i]
        self.outcome_picked = True
        self.time = self.the_outcome.time
        #print(self.the_outcome)
        self.money = self.the_outcome.money
        return self.the_outcome

    def execute(self):
        intemp = True
        for input_box in self.input_boxes:
            if input_box.sufficient and input_box.output:
                intemp = True
                break
            if not input_box.output:
                intemp = False
        self.input = intemp

        if not self.input:
            return None
        if not self.outcome_picked:
            self.pick_an_outcome()

        if not self.output:
            if self.counter_time >= self.time:
                self.output = True
                #print('outcome is passed up here', self.the_outcome, self.time)
                return self.the_outcome
            else:
                self.counter_time += 1
                return None
        else:
            #print('outcome is passed down here', self.the_outcome, self.time)
            return self.the_outcome





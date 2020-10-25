import numpy as np
from collections import Counter
from itertools import combinations

class Scoring:
    def __init__(self):
        pass

    def fiveCardScore(self, hand, cut):
    # takes an array of tuple "hand" and single np array "cut"
        pairPoints = self.pairScore(hand, cut)
        flushPoints = self.flushScore(hand, cut)
        fifteenPoints = self.fifteenScore(hand, cut)
        runPoints = self.runScore(hand,cut)
        nobsPoints = self.nobsScore(hand,cut)
        pointSum = pairPoints + flushPoints + fifteenPoints + runPoints + nobsPoints
        return pointSum

    def pairScore(self, hand, cut):
        #add hand to cut 
        totalHand = np.concatenate((hand,cut), axis = 0)
        #count repeat cards in hand
        countDict = (Counter(totalHand[:,0]))
        #convert to numpy array
        values = np.array(list(countDict.values()))
        #calculate pair values
        total = sum(values*(values-1))
        return total

    def flushScore(self, hand, cut):
        #count repeat suits in hand
        countDict = (Counter(hand[:,1]))
        # find if there is only one suit
        if len(countDict) == 1:
            if cut[0,1] == hand[0,1]:
                return 5
            else:
                return 4
        else:
            return 0
    
    def fifteenScore(self, hand, cut):
        # add hand to cut 
        totalHand = np.concatenate((hand,cut), axis = 0) 
        # set all face cards to 10
        numbers = totalHand[:,0].astype(np.int)
        numbers[numbers>10] = 10
        # calculate score
        total = 0
        for count in range(2,6):
            # find all possible combinations of count number of cards
            combos= list(combinations(numbers, count))
            # adds two points if 15 found
            total += sum([2 for row in combos if sum(row) == 15])
        return total

    def runScore(self, hand, cut):
        # add hand to cut 
        totalHand = np.concatenate((hand,cut), axis = 0) 
        # set all face cards to 10
        numbers = totalHand[:,0].astype(np.int)
        total = 0
        for count in reversed(range(3,6)):
            # find all possible combinations of count number of cards
            combos= np.array(list(combinations(numbers, count)))
            # find pairs that are consecutive
            difference = sum([i for i in range(1,count)])
            total = sum([count for row in combos if row is list(range(min(row),max(row)))])
            if total > 0 :
                return total
        return total

    def nobsScore(self, hand, cut):
        # finds if jack in hand matches suit of cut card
        return ['11', cut[0,1]] in hand.tolist()

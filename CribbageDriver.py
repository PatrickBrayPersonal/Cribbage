import timeit
import numpy as np
from Scoring import Scoring
from Testing import Testing

class CribbageDriver:
    def main():
        scoring = Scoring()
        test = Testing()
        allHands, deck = test.deckMaker()
        sample_size = 100
        #average = test.sampleTester(1000, allHands, scoring, plot = False)


        #INSTATIATE CLASSES
        code  = 'average = test.sampleTester(sample_size, allHands, scoring, plot = False)'
        setup = '''from Scoring import Scoring
from Testing import Testing
scoring = Scoring()
test = Testing()
allHands, deck = test.deckMaker()
sample_size = {}'''.format(sample_size)
        #time = timeit.timeit(setup = setup, stmt = code, number = 1)
        #print('Sample Size: ', sample_size, '\nScored in: ', time, ' seconds\nFor ', sample_size/time, ' hands per second')
        #test.expectedValueSampleTester(1, deck, isOwnCrib = False, scoring = scoring, plot = False)
        #hand = ((, 'C'), (, 'S'), (, 'H'), (, 'D'), (, 'D'), (, 'D'))
        hand = ((1, 'H'), (4, 'H'), (6, 'H'), (10, 'S'), (1, 'D'), (5, 'D'))
        hand = ((4, 'C'), (8, 'H'), (13, 'C'), (9, 'H'), (2, 'H'), (6, 'H'))
        hand = ((6, 'C'), (13, 'S'), (5, 'H'), (9, 'H'), (6, 'H'), (3, 'D'))
        hand = ((10, 'C'), (13, 'S'), (6 ,'H'), (2, 'D'), (1, 'D'), (10, 'D'))
        hand = ((3, 'C'), (5, 'C'), (6, 'C'), (2, 'C'), (11, 'D'), (3, 'D'))
        hand = ((3, 'C'), (9, 'C'), (6, 'H'), (8, 'D'), (6, 'D'), (12, 'D'))
        hand = ((10, 'C'), (6, 'S'), (7, 'C'), (11, 'C'), (3, 'D'), (7, 'D'))
        hand = ((9, 'C'), (7, 'S'), (8, 'H'), (10, 'H'), (11, 'D'), (2, 'D'))
        hand = ((1, 'C'), (3, 'S'), (2, 'H'), (13, 'S'), (4, 'D'), (3, 'D'))
        hand = ((9, 'S'), (3, 'S'), (6, 'H'), (6, 'D'), (13, 'D'), (11, 'H'))
        test.keepCalculator(hand, deck, isOwnCrib = True, scoring = scoring, plot = False)

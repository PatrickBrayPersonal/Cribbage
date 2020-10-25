import numpy as np
import pandas as pd
import matplotlib .pyplot as plt
import random
from itertools import combinations

class Testing:
    
    def sampleTester(self, sample_size, allHands, scoring, plot):
        #SELECT MANAGEABLE SIZE
        sampleHands = random.sample(allHands, sample_size)
        scoreArr= [None] * sample_size
        count = 0
        for row in sampleHands:
            scoreArr[count] = scoring.fiveCardScore(np.array(row[0:4]), np.array([row[4]]))
            count += 1
        average_hand_value = sum(scoreArr)/len(scoreArr)
        print('Average Hand Value: ' , average_hand_value)
        print('Max Hand Value: ', max(scoreArr))
        print('Frequency of Max Hand: ', scoreArr.count(max(scoreArr)))
        if max(scoreArr) > 29:
            bad_hand = sampleHands[scoreArr.index(max(scoreArr))][:]
            print(bad_hand)
        if plot == True:
            plt.hist(scoreArr, 29)
            plt.show()
            plt.close()
        return average_hand_value


    def deckMaker(self):
        # CREATE DECK OF CARDS
        numbers = list(range(1,14))*4
        suits = ('C,'*13+'H,'*13+'S,'*13+'D,'*13).split(',')[0:52]
        deck = list(zip(numbers, suits))
        # CREATE ALL POSSIBLE HANDS
        allHands = list(combinations(deck, 5))
        return allHands, deck

    def scoreTester(self, scoring):
        # ASSIGN TEST DATA
        hand0 = np.array([(11,'S'),(5,'C'),(5,'D'),(5,'H')])
        cut0 = np.array([(5,'S')])
        hand1 = np.array([(1,'S'),(1,'C'),(2,'D'),(2,'H')])
        cut1 = np.array([(3,'S')])
        hand2 = np.array([(4,'H'),(4,'S'),(5,'H'),(5,'S')])
        cut2 = np.array([(6,'S')])
        hand3 = np.array([(6,'H'),(7,'H'),(8,'H'),(9,'H')])
        cut3 = np.array([(7,'S')])
        hand4 = np.array([[11,'H'],[1,'H'],[11,'D'],[3,'H']])
        cut4 = np.array([[2,'H']])
        testArr = np.array([[hand0, cut0, 29],[hand1, cut1, 16],[hand2, cut2, 24],[hand3,cut3, 20],[hand4,cut4,10]])          

        # PERFORM TESTS
        for row in testArr:
            print('Hand: \n', row[0], '\nCut:\n', row[1])
            print('Score Found: ', scoring.fiveCardScore(row[0],row[1]), 'Expected Score: ', row[2])

    # Calculates Expected Value of 4 Card Hand
    # Returns Array of Scores for all possible cut cards
    def expectedHandValueCalculator(self, hand, deck, scoring):
        # score 5 card hands for each 
        scoreArr= [None] * len(deck)
        for idx, cut_card in enumerate(deck):
            scoreArr[idx] = scoring.fiveCardScore(hand, np.array([cut_card]))
        return scoreArr

    # Calculates Expected Value of 2 Card Hand
    # Returns Array of Scores for all possible hands containing the two specified
    def expectedThrowValueCalculator(self, throw, deck, scoring):
        three_card_combos = np.array(list(combinations(deck, 3)))
        # score 5 card hands for each 
        scoreArr= [None] * len(three_card_combos)
        for idx, three_card_combo in enumerate(three_card_combos):
            sampleHand = np.concatenate((throw, three_card_combo))
            scoreArr[idx] = scoring.fiveCardScore(sampleHand[0:4], sampleHand[[4]])
        return scoreArr

    # Calculates Expected Values of 6 Card Hand
    # Returns Array of average expected Value for each 4 card choice
    def expectedValueOfHandFinder(self, hand, deck, isOwnCrib, scoring):
        hand = np.array(hand)
        deck = np.array(deck)
        # remove cards in hand from potential cut cards
        deck = self.removeCardsFromDeck(deck, hand)
        # create all 4 card combos from given hand
        allHands = np.array(list(combinations(hand, 4)))
        # holds average expected value for each 4 card combo
        expectedValueArr = [None]*len(allHands)
        expectedHandValueArr = [None]*len(allHands)
        expectedThrowValueArr = [None]*len(allHands)
        for idx, four_card_combo in enumerate(allHands):
            # determine what cards are going to the crib
            throw = self.removeCardsFromDeck(hand, four_card_combo)
            # calculate expected value of the cards kept
            handArr = self.expectedHandValueCalculator(four_card_combo, deck, scoring)
            # calculate expected value of cards to crib
            throwArr = self.expectedThrowValueCalculator(throw, deck, scoring)
            # Calculate average expected Value of hand and subtract or add the expected value of the 
            expectedHandValueArr[idx] = sum(handArr)/len(handArr)
            print(four_card_combo)
            print('Hand Value: ', expectedHandValueArr[idx])
            expectedThrowValueArr[idx] = sum(throwArr)/len(throwArr)
            print('Throw Value: ', expectedThrowValueArr[idx])
            if isOwnCrib == True:
                expectedValueArr[idx] = expectedHandValueArr[idx] + expectedThrowValueArr[idx]
            else:
                expectedValueArr[idx] = expectedHandValueArr[idx] - expectedThrowValueArr[idx]       
        return expectedValueArr, expectedHandValueArr, expectedThrowValueArr, allHands

    # Applies the expected Value calculation to a specified sample size of random hands
    def expectedValueSampleTester(self, sample_size, deck, isOwnCrib, scoring, plot):
        allHands = list(combinations(deck,6))
        sampleHands = random.sample(allHands, sample_size)
        for hand in sampleHands:
            print('Your hand is: \n' , hand)
            expectedValueArr, expectedHandValueArr, expectedThrowValueArr, evHands = self.expectedValueOfHandFinder(hand, deck, isOwnCrib, scoring)
            print(expectedValueArr)
            print(evHands)
            print('The best cards to keep are: \n' ,evHands[expectedValueArr.index(max(expectedValueArr))])
            print('With an expected value of : ' ,'%.3f'%(max(expectedValueArr)))

    # Removes cards indicated as "hand" from the known deck
    def removeCardsFromDeck(self, deck, hand):
        hand = np.array(hand)
        for idx, card in enumerate(hand):
            deck = deck[~((deck == hand[[idx]]).all(axis = 1))]
        return deck

    def removeCardsFromHand(self, hand, to_remove):
        concat_hand = [str(i[0]) + i[1] for i in hand]
        concat_to_remove = [str(i[0]) + i[1] for i in to_remove]
        hand = hand[concat_hand != concat_to_remove]
        print(hand)
        return hand

    def keepCalculator(self, hand, deck, isOwnCrib, scoring, plot):
        # finds the 4 cards in your hand that will produce the highest expected value
        expectedValueArr, expectedHandValueArr, expectedThrowValueArr, evHands = self.expectedValueOfHandFinder(hand, deck, isOwnCrib, scoring)
        print('The best cards to keep are: \n' ,evHands[expectedValueArr.index(max(expectedValueArr))])
        print('With an expected value of : ' ,'%.3f'%(max(expectedValueArr)))

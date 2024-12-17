#! problem3.py
"""Problem3.py: A program that allows a user to practice fraction operations
fraction composed of 2 attributes, a numerator and a denominator"""

__author__ = "Carter Harms"
__copyright__ = "Copyright, 2023"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "harmsc@uchicago.edu"

# imports
import random
from fractions import Fraction
import sys

class Game:

    # Initalize override to start the Game
    def __init__(self):
        print("Welcome to Action Fractions!\n")
        # create attributes for attempted/completed inputs
        self.attempted = 0
        self.completed = 0
    
    # Function to generate fractions with a maximum denominator of 5
    def create_fractions(self):
        self.fraction1_numerator = random.randint(1,5)
        self.fraction1_denominator = random.randint(1,5)
        self.fraction2_numerator = random.randint(1,5)
        self.fraction2_denominator = random.randint(1,5)
        # Converting the fractions into fraction format using the fractions module
        fraction1 = Fraction(self.fraction1_numerator, self.fraction1_denominator)
        fraction2 = Fraction(self.fraction2_numerator, self.fraction2_denominator)
        return fraction1, fraction2
    
    # Function to choose an operator at random
    def operator(self):
        operators = ['+', '-', '*', '/']
        operator = random.choice(operators)
        return operator
    
    # Function to structure the 4 types of equations depending on the random operator chosen
    def comp_answer(self, fraction1, fraction2, operator):
        if operator == "+":
            return fraction1 + fraction2
        elif operator == "-":
            return fraction1 - fraction2
        elif operator == "*":
            return fraction1 * fraction2
        elif operator == "/":
            return fraction1 / fraction2
        

    # Gameplay function
    def gameplay(self):

        # Random creation of the equation (composed of fractions and operator)
        fraction1, fraction2 = self.create_fractions()
        operator = self.operator()
        comp_ans = self.comp_answer(fraction1, fraction2, operator)
        # Asking for user input
        print(f"What is {fraction1} {operator} {fraction2}")
        answer = input("> ")
        # Converting user answer into fraction format
        answer = Fraction(answer)

        # Confirming user answer as correct or incorrect
        if comp_ans == answer:
            print("Correct!")
            # Adding tally to completed problems
            self.completed +=1
        else:
            print("Incorrect!")
        
        # Adding tally to attempted problems
        self.attempted += 1

        # Querying user if they want to play again
        play_again = input(f"Would you like another problem [y/n]\n> ").lower().strip()

        if play_again == "y":
            self.gameplay()
        elif play_again == "n":
            print(f'You answered {self.completed}/{self.attempted} problems correctly. Keep up the good work!')
        else:
            print("You did not enter a valid response.")
    

game = Game()
game.gameplay()


# References
# ref: https://codereview.stackexchange.com/questions/87287/guess-the-number-game-in-python
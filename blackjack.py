'''
Augusto Celis
7/11/19
Blackjack GUI using guizero
This is a simulator that lets you play Blackjack against a house bot.
Enjoy!
'''
from guizero import App, Text, Box, Picture, PushButton, yesno
import random
import sys

class Player:
    def __init__(self):
        self.cards = []
        self.playerScore = 0

    def add_card(self, card):
        cardString = card.split("of")

        value = cardString[0].replace(' ', '') #Value of card
        suit = cardString[1].replace(' ', '')  #Suit of card
        img_path = "images/" + suit + "/" + suit + "_" + value + ".png" #Image path used for card display

        #Display new card on screen
        globals()[card] = Picture(player_box, image=img_path, align="left")
        self.cards.append(card)

        #Add score to player total
        self.add_score(value)

    def add_score(self, points):
        if (points == "king" or points == "queen" or points == "jack"):
            self.playerScore += 10
        elif points == "ace":
            self.playerScore += 1
        else:
            self.playerScore += int(points)

        player_total.value = "Your score: " + str(self.playerScore)
        self.check_bust()

    def get_score(self):
        return self.playerScore

    def check_bust(self):
        # Check if player has gone over 21
        if self.get_score() > 21:
            retry = yesno("Over 21!", "You have exceeded 21. You have lost! Would you like to play again?")
            if retry == True:
                resetGame()
            else:
                sys.exit("Thank you for playing!")

    def reset(self):
        #Delete all global cards on GUI
        for i in range(len(self.cards)):
            globals()[self.cards[i]].destroy()
            del globals()[self.cards[i]]

        player_total.value = "Your score: 0"
        self.cards = []
        self.playerScore = 0

class Computer:
    def __init__(self):
        self.cards = []
        self.computerScore = 0

    def add_card(self, card):
        cardString = card.split("of")

        value = cardString[0].replace(' ', '') #Value of card
        suit = cardString[1].replace(' ', '')  #Suit of card
        img_path = "images/" + suit + "/" + suit + "_" + value + ".png" #Image path used for card display

        #Display new card on screen
        globals()[card] = Picture(house_box, image=img_path, align="left")
        self.cards.append(card)

        #Add score to house total
        self.add_score(value)

    def add_score(self, points):
        if (points == "king" or points == "queen" or points == "jack"):
            self.computerScore += 10
        elif points == "ace":
            self.computerScore += 1
        else:
            self.computerScore += int(points)

        house_total.value = "House score: " + str(self.computerScore)
        self.check_bust()

    def get_score(self):
        return self.computerScore

    def check_bust(self):
        global stop

        # Check if house has went over 21 or 17
        if self.get_score() > 21:
            stop = True
            retry = yesno("House has went over 21!", "House has exceeded 21. You won! Would you like to play again?")
            if retry == True:
                resetGame()
            else:
                sys.exit("Thank you for playing!")

        elif self.get_score() > 17:
            stop = True
            if player.get_score() == self.get_score():
                retry = yesno("Tie!", "You and house have the same score. It is a tie! Would you like to play again?")
                if retry == True:
                    resetGame()
                else:
                    sys.exit("Thank you for playing!")

            if player.get_score() > self.get_score():
                retry = yesno("You win!", "You have a higher score than house. You win! Would you like to play again?")
                if retry == True:
                    resetGame()
                else:
                    sys.exit("Thank you for playing!")

            else:
                retry = yesno("You lose!", "House has a higher score than you. You lose! Would you like to play again?")
                if retry == True:
                    resetGame()
                else:
                    sys.exit("Thank you for playing!")

    def reset(self):
        #Delete all global cards on GUI
        for i in range(len(self.cards)):
            globals()[self.cards[i]].destroy()
            del globals()[self.cards[i]]

        house_total.value = "House score: 0"
        self.cards = []
        self.computerScore = 0

class Deck:
    card_face = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
    card_suit = ['hearts', 'spades', 'clubs', 'diamonds']

    def __init__(self):
        self.cards = []
        self.reshuffle()

    def reshuffle(self):
        self.restart()
        self.shuffle()

    def restart(self):
        self.cards = []
        for i in range(len(self.card_face)):
            for j in range(len(self.card_suit)):
                self.cards.append(self.card_face[i] + " of " + self.card_suit[j])

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if not len(self.cards):
            self.reshuffle()

        return self.cards.pop()

deck = Deck()
player = Player()
computer = Computer()
stop = False
'''
Function: resetGame()
Global Variables: score, house_score, card, card_suit, card_number, user_turn

This function is used to reset the game when somebody would like to play again,
when they choose to rest the game. This will reset all the variables, reset all
the images, and the globals() variable.
'''
def resetGame():
    if computer.get_score():
        computer.reset()
    player.reset()

    start_button.enable()
    hit_button.disable()
    stay_button.disable()

'''
Function: hit()
Sub Functions: drawCard(), addScore()
Global Variables: player_cards, cards_drawn, card_suit, card

This function is used to draw another card for the user. This is if the user would like
to add another card to their score, and it will be updated dynamically as well.
'''
def hit():
    card = deck.draw_card()
    player.add_card(card)

'''
Function: stay()

This function is used to wait for the house to draw. Cards will be drawn for the house,
card pictures will be updated, and house score will be updated.
'''
def stay():
    global stop

    stop = False
    while not stop:
        card = deck.draw_card()
        computer.add_card(card)

'''
Function: startGame()

This will draw the first 2 cards for the player. This will also update the photos
shown on the screen to reflect the card that has been chosen. This will also update
each appropriate score for the user and the house.
'''
def startGame():
    start_button.disable()
    hit_button.enable()
    stay_button.enable()

    for i in range(2):
        card = deck.draw_card()
        player.add_card(card)

'''
This next section is setup for the GUI, as each element will be directly under each other
This also includes the appropriate boxes for the
'''
app = App(title="Blackjack 21", width=1000, height=1000)

# The welcoming message to the game
welcome_message = Text(app, "Welcome to Blackjack!", size=40, color="lightblue", font="Times New Roman")
rules = Text(app, "This is a game where you play the AI (house), and attempt to get as close to 21, without going over", size=18)
rules_2 = Text(app, "Each turn you can choose to hit (draw a card), or stay (keep your cards). If you stay, house will begin drawing.", size=18)
rules_3 = Text(app, "Hint - House must draw until they have over 17, so you have a chance of winning even if you have low values.",size=14, color="red")
start_text = Text(app, "Click 'start' to start the game")

# Where player cards and score is displayed
player_box = Box(app)
total = "Your score: 0"
player_total = Text(player_box, total, align="right")

# Simply holds the stack picture
stack_pic = Picture(app, image="images/stack_resized.png", align="top")

# Where house cards and score is displayed
house_box = Box(app)
total_2 = "House score: 0"
house_total = Text(house_box, total_2, align="right")

# Buttons to play the game
start_button = PushButton(app, command=startGame, text="Start!", width=30, pady=20)
hit_button = PushButton(app, command=hit, text="Hit!", width=30, pady=20, enabled=False)
stay_button = PushButton(app, command=stay, text="Stay!", width=30, pady=20, enabled=False)

# Start the game
app.display()

'''
Augusto Celis
7/11/19
Blackjack GUI using guizero
This is a simulator that lets you play Blackjack against a house bot.
Enjoy!
'''
from guizero import *
import random
import sys

player_cards = 0 #Determines how many cards the player has drawn
house_cards = 0 #Determines how many cards the house has drawn
player_lis = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"] #Variables for player cards
house_lis = ["hc1", "hc2", "hc3", "hc4", "hc5", "hc6", "hc7", "hc8", "hc9", "hc10", "hc11"] #Variables for house cards
score = 0 #Your score
house_score = 0 #House score
used = [] #Discard pile
suits = ["hearts", "spades", "clubs", "diamonds"] #Suits of cards
numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"] #Numbers of cards
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #Potential values for each card
cards_drawn = 0 #Number of cards drawn
card = "" #Present card drawn
card_suit = "" #Present card drawn suit
card_number = "" #Present card number drawn
user_turn = True #States that it is the user turn on start

'''
Function: resetGame()
Global Variables: score, house_score, card, card_suit, card_number, user_turn

This function is used to reset the game when somebody would like to play again,
when they choose to rest the game. This will reset all the variables, reset all
the images, and the globals() variable.
'''
def resetGame():
    global score, house_score, card, card_suit, card_number, user_turn

    score = 0
    house_score = 0
    card = ""
    card_suit = ""
    card_number = ""
    user_turn = True

    player_pic.image = "images/blank_resize.png"
    house_pic.image = "images/blank_resize.png"

    for x in range(1, player_cards):
        globals()[player_lis[x]].destroy()
        del globals()[player_lis[x]]

    if house_cards > 0:
        for x in range(1, house_cards):
            globals()[house_lis[x]].destroy()
            del globals()[house_lis[x]]


    player_total.value = "Your score: " + str(score)
    house_total.value = "House score: " + str(house_score)

    start_button.enable()
    hit_button.disable()
    stay_button.disable()

'''
Function: checkLoss()
Sub-Functions: resetGame()
Global Variables: score, house_score, user_turn

This function is used to check if the user has lost, or if the house
has lost. This function is called each time a value is added to see if
the user or house has broken above 21.

NOTE: A default rule of house is to continue drawing until they have at
least a value of 17. Then they stop drawing.
'''
def checkLoss():
    global user_turn, score, house_score

    #Check if player has gone over 21
    if score > 21:
        retry = yesno("Over 21!", "You have exceeded 21. You have lost! Would you like to play again?")
        if retry == True:
            resetGame()
        else:
            sys.exit("Thank you for playing!")

    #Check if house has went over 21 or 17
    if house_score > 21:
        user_turn = True
        retry = yesno("House has went over 21!", "House has exceeded 21. You won! Would you like to play again?")
        if retry == True:
            resetGame()
        else:
            sys.exit("Thank you for playing!")

    elif house_score >= 17:
        if score > house_score:
            retry = yesno("You win!", "You have a higher score than house. You win! Would you like to play again?")
            if retry == True:
                resetGame()
            else:
                sys.exit("Thank you for playing!")

        elif score == house_score:
            retry = yesno("Tie!", "You and house have the same score. It is a tie! Would you like to play again?")
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

'''
Function: addScore()
Sub Functions: checkLoss()
Global Variables: score, card, house_score, user_turn

Add value of the card to the appropriate users' score. This would
is seperated into if they have a face card, or they have a number.
At the end, the user/house score is updated on the screen.
'''
def addScore():
    global user_turn, card_number, score, house_score

    points = 0
    if "jack" in card or "queen" in card or "king" in card:
        points = 10
    elif "ace" in card:
        points = 1
    else:
        number = int(card_number)
        points = number

    if user_turn:
        score += points
        player_total.value = "Your score: " + str(score)
        checkLoss()

    else:
        house_score += points
        house_total.value = "House score: " + str(house_score)
        checkLoss()

'''
Function: drawCard()
Global Variables: cards_drawn, card, card_number, card_suit

Draws a card to give either to the player or the house. This
would be saved into our global vairables for further use, and would
only be drawn if they have a unique card.
'''
def drawCard():
    global card, card_suit, card_number, cards_drawn

    unique = False
    while not unique:
        card_suit = random.choice(suits)
        card_number = random.choice(numbers)
        card = card_suit + "_" + card_number
        if card not in used:
            unique = True

    used.append(card)

'''
Function: hit()
Sub Functions: drawCard(), addScore()
Global Variables: player_cards, cards_drawn, card_suit, card

This function is used to draw another card for the user. This is if the user would like
to add another card to their score, and it will be updated dynamically as well.
'''
def hit():
    global player_cards, cards_drawn, card_suit, card

    if cards_drawn >= 51:
        used.clear()
        cards_drawn = 0

    cards_drawn += 1
    drawCard()
    img_path = "images/" + card_suit + "/" + card + ".png"
    globals()[player_lis[player_cards]] = Picture(player_box, image = img_path, align = "left")
    player_cards += 1
    addScore()

'''
Function: stay()
Sub Functions: drawCard(), addScore()
Global Variables: house_cards, cards_drawn, user_turn, card_suit, card

This function is used to wait for the house to draw. Cards will be drawn for the house,
card pictures will be updated, and house score will be updated.
'''
def stay():
    global house_cards, cards_drawn, user_turn, card_suit, card

    if cards_drawn >= 48:
        used.clear()
        cards_drawn = 0

    cards_drawn += 1
    user_turn = False

    while not user_turn:
        drawCard()
        if house_cards == 0:
            img_path = "images/" + card_suit + "/" + card + ".png"
            house_pic.image = img_path
            house_cards += 1

        else:
            img_path = "images/" + card_suit + "/" + card + ".png"
            globals()[house_lis[house_cards]] = Picture(house_box, image = img_path, align = "left")
            house_cards += 1

        addScore()

'''
Function: startGame()
Sub Functions: drawCard(), addScore(0)
Global Variables: player_cards, house_cards, cards_drawn, card_suit, card

This will draw the first 2 cards for the player. This will also update the photos
shown on the screen to reflect the card that has been chosen. This will also update
each appropriate score for the user and the house.
'''
def startGame():
    global player_cards, house_cards, cards_drawn, card_suit, card

    player_cards = 0
    house_cards = 0

    start_button.disable()
    hit_button.enable()
    stay_button.enable()

    if cards_drawn >= 50:
        used.clear()
        cards_drawn = 0

    cards_drawn += 2

    #Draw first card for player
    drawCard()
    img_path = "images/" + card_suit + "/" + card + ".png"
    player_pic.image = img_path
    player_cards += 1
    addScore()

    #Draw second card for player
    drawCard()
    img_path = "images/" + card_suit + "/" + card + ".png"
    globals()[player_lis[player_cards]] = Picture(player_box, image = img_path, align = "left")
    player_cards += 1
    addScore()

'''
This next section is setup for the GUI, as each element will be directly under each other
This also includes the appropriate boxes for the
'''
app = App(title="Blackjack 21", width = 1000, height = 1000)

#The welcoming message to the game
welcome_message = Text(app, "Welcome to Blackjack!", size = 40, color = "lightblue", font = "Times New Roman")
rules = Text(app, "This is a game where you play the AI (house), and attempt to get as close to 21, without going over", size = 18)
rules_2 = Text(app, "Each turn you can choose to hit (draw a card), or stay (keep your cards). If you stay, house will begin drawing.", size = 18)
rules_3 = Text(app, "Hint - House must draw until they have over 17, so you have a chance of winning even if you have low values.", size = 14, color = "red")
start_text = Text(app, "Click 'start' to start the game")

#Where player cards and score is displayed
player_box = Box(app)
player_pic = Picture(player_box, image = "images/blank_resize.png", align = "left")
total = "Your score: " + str(score)
player_total = Text(player_box, total, align = "right")

#Simply holds the stack picture
stack_pic = Picture(app, image = "images/stack_resized.png", align = "top")

#Where house cards and score is displayed
house_box = Box(app)
house_pic = Picture(house_box, image = "images/blank_resize.png", align = "left")
total_2 = "House score: " + str(house_score)
house_total = Text(house_box, total_2, align = "right")

#Buttons to play the game
start_button = PushButton(app, command = startGame, text = "Start!", width = 30, pady = 20)
hit_button = PushButton(app, command = hit, text = "Hit!", width = 30, pady = 20, enabled = False)
stay_button = PushButton(app, command = stay, text = "Stay!", width = 30, pady = 20, enabled = False)

#Start the game
app.display()

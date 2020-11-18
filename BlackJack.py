import random

# SUITS
# There will be 13 cards of each suit within a deck
suits = ('Hearts','Diamonds','Clubs','Spades')

# RANKS
# There will be 4 of each rank within a deck, 1 in every suit.
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
         'Jack', 'Queen', 'King', 'Ace')
# GLOBAL DICTIONARY that will be used to give each card a value based on its rank.
# These values are what are compared to decided who wins each round.
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

# Boolean value to control the while loop that runs the game
playing = True

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    '''
    This will create all 52 card objects held as a list.
    Shuffle the deck through a method call. Random library shuffle() method.
    Deal out the cards to the players. Pop cards from the list.
    '''
    def __init__(self):
        # no user input because every new deck should be the same
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                # Create the card object
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)

    def shuffle_deck(self):
        random.shuffle(self.all_cards)

    # This will deal one card of the top of the deck
    def deal_one(self):
        return self.all_cards.pop()

# The hand class will be used to hold the card objects and to calculate the value of those cards
# This class will be used to adjust the value of an Ace between 11 and 1
class Hand:
    def __init__(self):
        self.cards = [] # empty list last will hold the card objects dealt to the player
        self.value = 0  # initial hand value of 0
        self.aces = 0   # Keep track of the aces in a player's hand

    def add_card(self, card):
        '''
        This method adds the cards to the player's hand from the Deck class deal_one
        method. Value is adjusted by the value of the card dealt to player.
        '''
        self.cards.append(card)
        self.value += values[card.rank]
        # Track the aces
        if card.rank == "Ace":
            self.aces +=1

    def adjust_for_ace(self):
        '''
        This method will determine whether or not an ace held in the player's cards list
        needs to be adjusted from 11 down to 1 if the player went over 21 while holding an
        ace.
        '''
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# CHIPS CLASS
# Keeps track of chip total and adjusts when a player wins or loses a bet.
class Chips:
    def __init__(self, total = 100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet*2

    def lose_bet(self):
        self.total -= self.bet

##  FUNCTIONS FOR GAMEPLAY  ##
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Sorry please provide an integer value.")
        else:
            if chips.bet > chips.total:
                print(f"Sorry you do not have the necessary funds. You have {chips.total}")
            else:
                print(f"The amount bet is {chips.bet}")
                break
def hit(deck,hand):
    hand.add_card(deck.deal_one())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing # used for while loop control

    while True:
        player_response = input("Hit or Stand? (h or s)\n").lower()

        if player_response[0] == 'h':
            hit(deck, hand)
        elif player_response[0] == 's':
            print("Player stands, Dealer's turn.")
            playing = False
        else:
            print("Sorry I don't understand please enter h or s")
            continue
        break

# These function's display the player's and the dealer's hands
def show_some(player, dealer):
    print(f"DEALER'S HAND: {dealer.cards[1]}\n\n")  # Only 1 card shown until player stands
    print("PLAYER'S HAND: ", *player.cards, sep='\n')
    print("Player's hand value: {}".format(player.value))

def show_all(player, dealer):
    print("DEALER'S HAND: ", *dealer.cards, sep='\n')
    print("PLAYER'S HAND: ", *player.cards, sep='\n')


# These functions will handle the situations in which the game will end.

def player_busts(player, dealer, chips):
    '''
    Player goes over 21 without an Ace in their hand.
    '''
    print("Player busts!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    '''
    Either the player's total hand value is higher than the dealer's after they both stand,
    the dealer busts, or the player achieved 21 with the first two cards they were dealt, 'Blackjack!'
    '''
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    '''
    Dealer's hand goes over 21 without and ace.
    '''
    print("Dealer busts! Player wins!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    '''
    Dealer's hand is of greater value than the player's hand after the player stands,
    the player busts, or the Dealer was dealt a 'Blackjack'
    '''
    print("Dealer wins!")
    chips.lose_bet()

def push(player, dealer):
    '''
    Player and Dealer achieve the same value after player stands and dealer is at or above 17
    and therefore doesn't take anymore cards.
    '''
    print("Push!")


##  GAME LOGIC  ##

player_chips = Chips()
while True:
    print ("Welcome to Blackjack!")
    #Create and shuffle deck
    deck = Deck()
    deck.shuffle_deck()

    #take player's bet before cards are dealt
    take_bet(player_chips)

    # Create players and deal 2 cards to each player
    dealer_hand = Hand()
    player_hand = Hand()
    player_hand.add_card(deck.deal_one())
    dealer_hand.add_card(deck.deal_one())
    player_hand.add_card(deck.deal_one())
    dealer_hand.add_card(deck.deal_one())


    # check for Blackjack where player automatically wins
    show_some(player_hand, dealer_hand)
    if player_hand.value == 21:
        player_wins(player_hand,dealer_hand,player_chips)
        print("\nPlayer has {} chips remaining".format(player_chips.total))
        new_game = input("Would you like to play another hand? y/n").lower()

        if new_game[0] == 'y':
            playing = True
        else:
            print("Thank you for playing!")
            break
    else:
        while playing:
            # prompt the player for whether they would like to hit or stand
            hit_or_stand(deck, player_hand)
            # show cards but keep one dealer card hidden, show_some
            show_some(player_hand, dealer_hand)
            # if player's hand exceeds 21, run player_busts and break out of the loop
            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand, player_chips)
                break

        # After player stands and hasn't busted, play dealer's hand until dealer reaches 17
        if player_hand.value <= 21:

            while dealer_hand.value < 17:
                hit(deck, dealer_hand)
            # show all cards
            show_all(player_hand, dealer_hand)
            # Run appropriate win scenario.
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)
            else:
                push(player_hand, dealer_hand)
        # Inform plaayer of their remaining chips
        print("\nPlayer has {} chips remaining".format(player_chips.total))
        # Prompt player to play another hand
        new_game = input("Would you like to play another hand? y/n").lower()

        if new_game[0] == 'y':
            playing = True
        else:
            print("Thank you for playing!")
            break

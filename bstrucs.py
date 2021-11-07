import globl
from random import shuffle

suits = ("hearts", "diamonds", "spades", "clubs")
ranks = ('two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace')  # noqa: E501
values = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'jack': 10, 'queen': 10, 'king': 10, 'ace': 11}  # noqa: E501

class Chips:
    def __init__(self, budget, bet):
        self.budget = budget
        self.bet = bet

    def take_bet(self):
        while True:
            try:
                self.bet = int(input(f"You currently have {self.budget} chips. How much do you want to bet on the bankroll?\n"))
            except ValueError:
                print("You are entering something different than a number. Try again!")
                continue
            else:
                if self.bet > self.budget:
                    print("Unfortunately, you don't have as much money available to you.")
                    continue
                elif self.bet <= 0:
                    print("You are trying to select an invalid amount of chips.")
                    continue
                print(f"If you win, you gain {self.bet*2} chips, however in case of a loss, you lose {self.bet} chips.\n--- --- ---")
                return self.bet


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Holder:
    def __init__(self):
        self.cards = []
        self.value = 0

    def __str__(self):
        return f"You currently have following cards on hand: {[str(card) for card in self.cards]} with a value of {self.value} points"

    def add_card(self, new_card):
        if new_card.rank == "ace":
            if self.value > 10:
                new_card.value = 1
        self.cards.append(new_card)
        self.value += new_card.value

    def show_all(self):
        print("Deck cards:", [str(card) for card in self.cards], f"Deck value: {self.value}")

    def show_but_one(self):
        print("Dealer cards: ? +", [str(card) for card in self.cards[1:]])


def hit(deck, holder):
    '''Adds a card from the global deck to a holder'''
    new_from_deck = deck.deal()
    holder.add_card(new_from_deck)


def hit_or_stand(deck, holder, money):
    '''Main playing loop asking the player to hit or stand'''
    while True:
        print(holder)
        if not bust_check(holder):
            state = input('Do you wish to hit or stand? Enter "hit" or "stand": ')
            if state.lower() == 'stand':
                break
            elif state.lower() == 'hit':
                hit(deck, holder)
            else:
                continue
        else:
            player_bust(holder, money)
            break


def bust_check(holder):
    return holder.value > 21

def player_bust(holder, money):
    money.budget -= money.bet
    print(f"With a value of {holder.value}, you have busted! The dealer wins and collects your money: you lose {money.bet}. Current budget: {money.budget}")
    globl.playing = False

def player_win(holder, money):
    money.budget += money.bet*2
    print(f"With a value of {holder.value}, you have won! The dealer lost, and you collect double your bet: you get {money.bet*2}. Current budget: {money.budget}")
    globl.playing = False
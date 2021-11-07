import bstrucs, globl

print("Welcome to blackjack!")
player_chips = bstrucs.Chips(100, 0)
while True:
    while globl.playing:
        gamedeck = bstrucs.Deck()
        gamedeck.shuffle()
        player_chips.take_bet()
        player = bstrucs.Holder()
        dealer = bstrucs.Holder()
        for x in range(2):
            player.add_card(gamedeck.deal())
            dealer.add_card(gamedeck.deal())
        player.show_all()
        dealer.show_but_one()
        print("--- --- ---")
        bstrucs.hit_or_stand(gamedeck, player, player_chips)
        if not bstrucs.bust_check(player):
            while not bstrucs.bust_check(dealer):
                if dealer.value > player.value:
                    bstrucs.player_bust(player, player_chips)
                    break
                elif dealer.value == player.value == 21:
                    print("It's a tie between the Dealer and the Player with both decks having a value of 21!")
                    globl.playing = False
                    break
                bstrucs.hit(gamedeck, dealer)
            else:
                bstrucs.player_win(player, player_chips)
        dealer.show_all()
    if player_chips.budget <= 0:
        print("As your budget reached zero, you can no longer play! We thank you for visiting our casino, come back again!")
        break
    else:
        rematch = input("Would you like to play another round? Type 'yes' or 'no': ")
        if rematch.lower() == 'yes':
            globl.playing = True
        elif rematch.lower() == 'no':
            print("We were glad to have you play with us today! See you again soon!")
            break
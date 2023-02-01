
import random

class Card():
    def __init__(self, type, number) -> None:
        self.type : str = type
        self.number : int = number

    def print_format(self) -> str:
        text = ""
        if self.type == 1:
            text += "♠"
        elif self.type == 2:
            text += "♥"
        elif self.type == 3:
            text += "♣"
        elif self.type == 4:
            text += "♦"
        else:
            text += "unknown"
            
        if self.number == 11:
            text += "B"
        elif self.number == 12:
            text += "Q"
        elif self.number == 13:
            text += "K"
        elif self.number == 14:
            text += "A"
        elif self.number == 15:
            text += "J"
        else:
            text += str(self.number)
        
        return text


            
class Game():
    def __init__(self) -> None:
        self.pot : Card = self.new_card()
        self.round_direction : int = -1
        self.current_pick_card : int = 0
        self.skips = 0

    def new_card(self) -> Card:
        type = random.randint(1,4)
        
        # if type == 1:
        #     type = "heart"
        # if type == 2:
        #     type = "diamond"
        # if type == 3:
        #     type = "club"
        # if type == 4:
        #     type = "spade"

        
        number = random.randint(1, 15)
        
        return Card(type, number)

class Player():
    def __init__(self, player_id, game: Game, type, manager) -> None:
        self.type = type
        self.id : int = player_id
        self.game : Game = game
        self.hand : list[Card] = []
        self.known_hands : dict[int: list[Card]] = {}
        self.manager = manager
    
    # just sorts the hands
    def sort_hand(self):
        self.hand = sorted(self.hand, key = lambda x: x.number)
        self.hand = sorted(self.hand, key=lambda x: x.type, reverse=True)
    
    # prints cards
    def print_cards(self):
        print('hand: ', [" (" + str(index + 1) + ") " + card.print_format() for index, card in enumerate(self.hand)])
    
    # adds cars to a players hand and lets the other players know
    def pick_card(self, amount : int = 1):
        for i in range(amount):
            self.hand.append(self.game.new_card())
            for player in self.manager.players:
                if player.id != self.id:
                    try:
                        player.known_hands[self.id].append(Card("?", -1))
                    except:
                        pass    
    
    # manages the forced card takes
    # checks if player can pick a card 
    # make player choose if he can
    # pick a card 
    def choose_card(self):        
        self.sort_hand()
        print("pot: ", self.game.pot.print_format())
        self.print_cards()
        if (self.game.current_pick_card != 0):
            if any([card.number in [2,15] for card in self.hand]):
                print("You take " + str(self.game.current_pick_card) + " cards unless you pick a 2 or a J")
            else:
                self.pick_card(self.game.current_pick_card)
                    
                print("You had to take " + str(self.game.current_pick_card) + " cards")
                self.game.current_pick_card = 0
                self.print_cards()

                
        chosen_card_value = -1
        if any([card.number == self.game.pot.number or card.type == self.game.pot.type for card in self.hand]):
            chosen_card_index = "-1"
            can_go_further = True
            while can_go_further:
                if self.type == "human":
                    chosen_card_index = input("what card do you want to choose: ")
                else:
                    pass
                
                try:
                    if (int(chosen_card_index) in range(1, len(self.hand) + 1) and (self.hand[int(chosen_card_index) - 1].number == self.game.pot.number or self.hand[int(chosen_card_index) - 1].type == self.game.pot.type)):
                        can_go_further = False
                except:
                    pass    
            chosen_card_value = self.hand[int(chosen_card_index) - 1]
            if self.game.current_pick_card != 0 and chosen_card_value.number in [2, 15]:
                self.game.current_pick_card += (2 if chosen_card_value.number == 2 else 5)
            self.play_card(chosen_card_value)
        else:
            new_card = self.game.new_card()
            self.hand.append(new_card)
            if new_card.number == self.game.pot.number or new_card.type == self.game.pot.type:
                self.play_card(new_card)


                
    def play_card(self, card: Card):
        if card in self.hand:
            self.hand.remove(card)
            
            for player in self.manager.players:
                if player.id != self.id:
                    try:
                        player.known_hands[self.id].remove(card)
                    except:
                        try:
                            player.known_hands[self.id].remove(Card("?", -1))
                        except:
                            pass
                         
            self.game.pot = card
            
            if card.number == 2:
                self.game.current_pick_card += 2
            
            if card.number == 7:
                self.choose_card()
                
            if card.number == 8:
                self.game.skips += 1
            
            if card.number == 10:
                print([' (' + str(player.id) + ') ' for player in self.manager.players if player.id != self.id])
                player_id = "-1"
                while not int(player_id) in [player.id for player in self.manager.players if player.id != self.id]:
                    if self.type == "human":
                        player_id = input("Note the id of the player of whom you want to see the card: ")
                    else:
                        pass
                    
                self.known_hands[int(player_id)] = self.manager.players[[player.id for player in self.manager.players].index(int(player_id))]
            
            if card.number == 11:
                print("(1)heart (2)diamond (3)club (4)spade")
                new_type = -1
                                    
                can_go_further = True
                while can_go_further:
                    if self.type == "human":
                        new_type = input("what color do you choose: ")
                    else:
                        pass
                    
                    try:
                        if int(new_type) in range(1,5):
                            can_go_further = False
                    except:
                        pass   
                
                # if int(new_type) == 1:
                #     new_type = "heart"
                # if int(new_type) == 2:
                #     new_type = "diamond"
                # if int(new_type) == 3:
                #     new_type = "club"
                # if int(new_type) == 4:
                #     new_type = "spade"


                self.game.pot = Card(int(new_type), self.game.pot.number)
            
            if card.number == 14:
                self.game.round_direction = -1 * self.game.round_direction
                
            if card.number == 15:
                self.game.current_pick_card += 5
            
            
    
                    

                

            

            
    
class GameManager():
    def __init__(self, player_amount: int, game : Game) -> None:
        self.game : Game = game
        self.players : list[Player] = [Player(player_id, self.game, "human", self) for player_id in range(1, player_amount + 1)]
        self.current_player = 0
        
        for i in range(7):
            for player in self.players:
                player.hand.append(self.game.new_card())
        
        for player in self.players:
            for dict_player in self.players:
                if player.id != dict_player.id:
                    player.known_hands[dict_player] = [-1 for i in range(7)]
        
        

        
    def play(self):
        while not any([len(player.hand) == 0 for player in self.players]):
            if self.game.skips == 0:
                print("Player ID: ", self.players[self.current_player].id)
                self.players[self.current_player].choose_card()
            else:
                self.game.skips = 0
            
            
            if self.current_player + self.game.round_direction > len(self.players) -1:
                self.current_player = 0
            elif self.current_player + self.game.round_direction < -1:
                self.current_player = len(self.players) -1
            # print(self.game.round_direction, self.current_player)
            self.current_player += self.game.round_direction

        print(list(filter(lambda x: len(x.hand) == 0,self.players))[0])
        
game = Game()
manager = GameManager(3, game)

manager.play()
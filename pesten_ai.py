
import random



class Card():
    def __init__(self, type = -1, number = -1) -> None:
        if type <= 1:
            self.type : int = random.randint(1,4)
        else:        
            self.type : int = type
            
        if number <= 1:
            self.number : int = random.randint(2,15)
        else:        
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

    def normalized_values(self) -> tuple[float, float]:
        return (self.type * (1/4), self.number * (1/15),)
         
class Game():
    def __init__(self, print_values=True) -> None:
        self.print_values = print_values
        self.pot : Card = Card()
        self.round_direction : int = -1
        self.current_pick_card : int = 0
        self.skips = 0

class Player():
    def __init__(self, player_id, game: Game, type, manager, genome = -1) -> None:
        self.type = type
        if type != "human":
            self.genome = genome
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
            self.hand.append(Card())
            for player in self.manager.players:
                if player.id != self.id:
                    try:
                        player.known_hands[self.id].append(Card("?", -1))
                    except:
                        pass    
    
    def get_normalized_game_state(self):
        normalized_game_state = []
        
        # pot
        pot = self.game.pot.normalized_values()
        normalized_game_state += [pot[0], pot[1]]
        
        for i in range(20):
            if i <= len(self.hand) - 1:
                card = self.hand[i].normalized_values()
                normalized_game_state += [card[0], card[1]]
            else:
                normalized_game_state += [0, 0]

        normalized_game_state += [1 / (1+self.game.current_pick_card)]

        
        return normalized_game_state
    
    # manages the forced card takes
    # checks if player can pick a card 
    # make player choose if he can
    # pick a card 
    def choose_card(self):        
        self.sort_hand()
        if self.game.print_values:
            print("pot: ", self.game.pot.print_format())
            self.print_cards()
        if (self.game.current_pick_card != 0):
            if any([card.number in [2,15] for card in self.hand]):
                if self.game.print_values:
                    print("You take " + str(self.game.current_pick_card) + " cards unless you pick a 2 or a J")
            else:
                self.pick_card(self.game.current_pick_card)
                if self.game.print_values:
                    print("You had to take " + str(self.game.current_pick_card) + " cards")
                    self.print_cards()
                self.game.current_pick_card = 0
                if self.game.pot.number == 15:
                    self.choose_color()

                
        chosen_card_value = -1
        if any([card.number == self.game.pot.number or card.type == self.game.pot.type for card in self.hand]):
            chosen_card_index = "-1"
            can_go_further = True
            while can_go_further:
                if self.type == "human":
                    chosen_card_index = input("what card do you want to choose: ")
                else:
                    genome_input = self.get_normalized_game_state()
                    genome_input += [1, 0, 0] #is choosing a hand card to play
                    
                    output = self.genome[1].activate(genome_input)
                    playable_cards = [(card, index) for index, card in enumerate(self.hand) if (card.number == self.game.pot.number or card.type == self.game.pot.type)]

                    # print(int(len(playable_cards) * output[0]))
                    chosen_card_index = playable_cards[int((len(playable_cards) - 1) * output[0])][1] + 1
                
                try:
                    if (int(chosen_card_index) in range(1, len(self.hand) + 1) and (self.hand[int(chosen_card_index) - 1].number == self.game.pot.number or self.hand[int(chosen_card_index) - 1].type == self.game.pot.type)):
                        can_go_further = False
                except:
                    pass    
            chosen_card_value = self.hand[int(chosen_card_index) - 1]
            if self.game.current_pick_card != 0 and chosen_card_value.number in [2, 15]:
                pass
                # self.game.current_pick_card += (2 if chosen_card_value.number == 2 else 5)
            else:
                self.pick_card(self.game.current_pick_card)
                self.game.current_pick_card = 0

            self.play_card(chosen_card_value)

        else:
            new_card = Card()
            self.hand.append(new_card)
            if new_card.number == self.game.pot.number or new_card.type == self.game.pot.type:
                self.play_card(new_card)

    def choose_color(self):
        if self.game.print_values:
            print("(1)heart (2)diamond (3)club (4)spade")
        new_type = -1
                            
        can_go_further = True
        while can_go_further:
            if self.type == "human":
                new_type = input("what color do you choose: ")
            else:
                genome_input = self.get_normalized_game_state()
                genome_input += [0, 1, 0] #is picking color
    
                output = self.genome[1].activate(genome_input)

                new_type = int(output[0] * 4) + 1
                
                
            
            try:
                if int(new_type) in range(1,5):
                    can_go_further = False
            except:
                pass   

        self.game.pot = Card(int(new_type), self.game.pot.number)
                
    def play_card(self, card: Card):
        if card in self.hand:
            self.hand.remove(card)
            if self.game.print_values:
                print("you played: " + card.print_format())
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
                if self.game.print_values:
                    print([' (' + str(player.id) + ') ' for player in self.manager.players if player.id != self.id])
                player_id = "-1"
                can_go_further = True
                while can_go_further:
                    if self.type == "human":
                        player_id = input("Note the id of the player of whom you want to see the card: ")
                    else:
                        genome_input = self.get_normalized_game_state()
                        genome_input += [0, 0, 1] #is choosing a hand card to play
                        
                        output = self.genome[1].activate(genome_input)
                        numbers_of_other_players = len(self.manager.players) - 2
                        available_ids = [player.id for player in self.manager.players if player.id != self.id]
                        # print(int(len(playable_cards) * output[0]))
                        player_id = available_ids[int(numbers_of_other_players * output[0]) + 1]
                    
                    if int(player_id) in [player.id for player in self.manager.players if player.id != self.id]:
                        can_go_further = False
                    
                self.known_hands[int(player_id)] = self.manager.players[[player.id for player in self.manager.players].index(int(player_id))]
            
            if card.number == 11:
                self.choose_color()
            
            if card.number == 14:
                self.game.round_direction = -1 * self.game.round_direction
                
            if card.number == 15:
                self.game.current_pick_card += 5
            
            
    
                    

                

            

            
    
class GameManager():
    def __init__(self, human_amount: int = 0, genomes = [], game = Game) -> None:
        self.game : Game = game
        self.players = []
        for i in range(1, human_amount + 1):
            self.players.append(Player(i, self.game, "human", self))
                
        for index, genome in enumerate(genomes):
            self.players.append(Player(human_amount + index + 1, self.game, "agent", self, genome))
        
        self.current_player = 0
        
        for i in range(7):
            for player in self.players:
                player.hand.append(Card())
        
        for player in self.players:
            for dict_player in self.players:
                if player.id != dict_player.id:
                    player.known_hands[dict_player] = [-1 for i in range(7)]
                
        

        
    def play(self) -> list[Player]:
        while not any([len(player.hand) == 0 for player in self.players]):
            if self.game.skips == 0:
                if self.game.print_values:
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
        if self.game.print_values:
    
            print(list(filter(lambda x: len(x.hand) == 0,self.players))[0])
        
        return sorted(self.players, key=lambda x: len(x.hand))

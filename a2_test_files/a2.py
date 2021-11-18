"""
CSSE1001 Assignment 2
Semester 2, 2020
"""
from a2_support import *

# Fill these in with your details
__author__ = "{{Tie Wang}} ({{s4621539}})"
__email__ = "tie.wang@uqconnect.edu.au"
__date__ = "2020/9/13"

# Write your code here

class Entity(object):
    """A generic Entity within the game."""
    def __init__(self):
        """Entity should be constructed with Entity(),no addtional argument required."""
        self._eid = 'Entity'
        self._collide = True
        #Set collide attribute to True for an Entity upon creation.
        self._name = 'Entity'
        #Name for printing
        
    def get_name(self):
        """(str)Returns a string that represents the Entity’s name for printing"""
        return self._name
    
    def get_id(self):
        """(str)Returns a string that represents the Entity’s ID"""
        return self._eid

    def set_collide(self, collidable:bool):
        """Set the collision state for the Entity.

        Parameters:
            collidable(bool): The collision state.
        """
        self._collide = collidable

    def can_collide(self):
        """(bool)Return the collision state for the Entity.
"""
        if self._collide == True:
            collidation = True
            #Returns True if the Entity can be collided with
        else:
            collidation = False
            #False otherwise
        return collidation

    def __str__(self):
        return f"{self._name}('{self._eid}')"

    def __repr__(self):
        return f"{self._name}('{self._eid}')"
        


class Wall(Entity):
    """A special type of Entity within the game."""
    def __init__(self):
        """Wall should be constructed with Wall(),no addtional argument required."""
        super().__init__()
        self._eid = '#'
        self._collide = False
        #Set collide attribute to False for a door upon creation.
        self._name = 'Wall'
    


class Player(Entity):
    """A special type of Entity within the game."""

    def __init__(self, move_count):
        """ Parameters:
                move_count (int): Number of moves a Player can have for the given dungeon they are in
        """
        super().__init__()
        self._eid = 'O'
        self._move_count = move_count
        self._position =() 
        self._inventory =[] 
        self._name = 'Player'

    def set_position(self, position: tuple):
        """Sets the position of the Player.

        Parameters:
            position(tuple): New position for the player
        """
        self._position = position

    def get_position(self):
        """(tuple) Returns the player's position."""
        if self._position != ():
            return self._position
        else:
            return None
            #If the Player’s position hasn’t been set yet then this method should return None.

    def change_move_count(self, number: int):
        """Change the move count of player.

        Parameters:
             number(int): Number to be added to the Player’s move count.
        """
        self._move_count += number

    def moves_remaining(self):
        """(int)Returns an int representing how many moves the Player has left."""
        return self._move_count
    
    def add_item(self, item: Entity):
        """Adds the item to the Player’s Inventory

        Parameters:
            item(Entity): Items to be added to the Player's Inventory
        """
        self._inventory.append(item)
    
    def get_inventory(self):
        """Returns a list that represents the Player's inventory.
"""
        return self._inventory
    
class GameLogic:
    """GameLogic contains all the game information and how the game should play out."""
    def __init__(self, dungeon_name="game1.txt"):
        """Constructor of the GameLogic class.

        Parameters:
            dungeon_name (str): The name of the level.
        """
        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)
        self._player = Player(GAME_LEVELS[dungeon_name])
        self._game_information = {}
        self._win = False 
        self.init_game_information()
        #Find the position of all entities within the current dungeon at the start of the game.

    def get_positions(self, entity):
        """ Returns a list of tuples containing all positions of a given Entity type.

        Parameters:
            entity (str): the id of an entity.

        Returns:
            (list<tuple<int, int>>): Returns a list of tuples representing the 
            positions of a given entity id.
        """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row,col))

        return positions
    
    def get_dungeon_size(self):
        """(int)Returns the width of the dungeon as an integer.
"""
        return self._dungeon_size
    
    def init_game_information(self):
        """(tuple)Return a dictionary containing the position and the corresponding Entity as the keys and values respectively."""
        for k in self.get_positions('K'):
            self._game_information[k] = Key()
        for d in self.get_positions('D'):
            self._game_information[d] = Door()
        for w in self.get_positions('#'):
            self._game_information[w] = Wall()
        for m in self.get_positions('M'):
            self._game_information[m] = MoveIncrease()
        self._player.set_position(self.get_positions('O')[0])
        #Set the Player’s position at the same time
        return self._game_information
    
    def get_game_information(self):
        """(dict)Returns a dictionary containing the position and the corresponding Entity for the current dungeon.
"""
        return self._game_information
    
    def get_player(self):
        """(Player)Returns the Player object within the game.
"""
        return self._player

    def get_entity(self, position: tuple):
        """ Returns an Entity in the given position in the dungeon.

        Parameters:
            position(tuple): Position of the entity.

        Returns:
            Entity: Returns an Entity in the given position.
        """
        if position in self.get_game_information():
            entity = self.get_game_information()[position] 
        else:
            entity = None
            #If there is no Entity in the given postion or if the postion is off map then this function should return None.
        return entity
    
    def get_entity_in_direction(self, direction: str):
        """ Returns an Entity in the given direction of the Player’s position.

        Parameters:
            direction(str): direction moving towards

        Returns:
            Entity: Returns an Entity in the given position.
        """
        original_position = self._player.get_position()
        direction = DIRECTIONS[direction]
        possible_position = (original_position[0]+direction[0],original_position[1]+direction[1])
        #generate the position after moving towards the direction
        if possible_position in self._game_information:
            possible_entity = self._game_information[possible_position] 
        else:
            possible_entity = None
            #If there is no Entity in the given direction or if the direction is off map then this function should return None.
        return possible_entity

    def collision_check(self, direction: str):
        """ Return the collision state of the item in given direction for the player.

        Parameters:
            direction(str): direction moving towards

        Returns:
            Boolean: Returns the collision state of the item in given direction for the player.
        """
        blockade = self.get_entity_in_direction(direction)
        if blockade != None:
            if blockade.can_collide() == False:
                result = True
                #Returns True if a player can't travel in the given direction as they will collide. False otherwise.
            else:
                result = False
        else:
            result = False
        return result

    def new_position(self, direction: str):
        """  Returns a tuple of integers that represents the new position of the player given the direction.

        Parameters:
            direction(str): direction moving towards

        Returns:
            tuple: New position given the direction.
        """
        direction = DIRECTIONS[direction]
        og_position = self._player.get_position()
        new_position = (og_position[0]+direction[0],og_position[1]+direction[1])
        return new_position
    
    def move_player(self, direction: str):
        """Update the Player’s position to place them one position in the given direction.

        Parameters:
            
direction(str): direction moving towards
        """
        self._player.set_position(self.new_position(direction))

    def check_game_over(self):
        """(bool)Return True if the game has been lost and False otherwise."""
        if self._player.moves_remaining() == 0:#First check if player runs out of move counts
            if Key() not in self._player.get_inventory():#Then check if she/he has the key
                loss = True
            else:
                if (self._player.get_position()).get_entity != Door():#At last check if he/she is at the door
                    loss = True
                else:
                    loss = False
        else:
            loss = False
        return loss

                   
    def set_win(self, win:bool):
        """Set the game’s win state to be True or False.

        Parameters:
            win(bool):Win state
        """
        self._win = win

    def won(self):
        """(bool)Return game’s win state."""
        return self._win
                    
    # Write your code here
    



class Item(Entity):
    """A special type of an Entity within the game. This is an abstract class."""
    def __init__(self):
        """Item should be constructed with Door()."""
        super().__init__()
        self._name = 'Item'
        
    def on_hit(self, game: GameLogic):
        """ This function should raise the NotImplementedError.
"""
        raise NotImplementedError()

    
class Key(Item):
    """A special type of Item within the game."""
    def __init__(self):
        """Key should be constructed with Key()"""
        super().__init__()
        self._eid = 'K'
        self._name = 'Key'
        
    def on_hit(self, game: GameLogic):
        """What happened when the key is taken.

        Parameters:
            game(GameLogic):Current running game.
        """
        game._player.add_item(game._game_information[list(game._game_information)[0]])
        #The Key should be added to the Player’s inventory. 
        game._game_information.pop(list(game._game_information)[0])
        #Removed the key from the dungeon. 
class MoveIncrease(Item):
    """A special type of Item within the game."""

    def __init__(self,moves=5):
        """
        Parameters:
            moves(int): Extra moves the Player will begranted. Default value = 5
        """
        super().__init__()
        self._eid = 'M'
        self._moves = moves
        self._name = 'MoveIncrease'

    def on_hit(self, game: GameLogic):
        """What happened when the MoveIncrease is taken.

        Parameters:
            game(GameLogic):Current running game.
        """
        game._player.change_move_count(self._moves)
        #Increase the number of move for the player
        game._game_information.pop(list(game._game_information)[-1])
        #Remove the MoveIncrease from the dungeon.

class Door(Entity):
    """A special type of Entity within the game."""

    def __init__(self):
        """Door should be constructed with Door()"""
        super().__init__()
        self._eid = 'D'
        self._name = 'Door'
        
    def on_hit(self, game: GameLogic):
        """What happened when player is at the door.

        Parameters:
            game(GameLogic):Current running game.
        """
        if game._player.get_inventory() != []:
            #Check if the player has the key
            game.set_win(True)
        else:
            print("You don't have the key!")
            
class GameApp(object):
    """GameApp acts as a communicator between the GameLogic and the Display"""
    def __init__(self):
        """GameApp should be constructed with GameApp()."""
        self._currentgame = GameLogic()  
            
    def draw(self):
        """ Displays the dungeon with all Entities in their positions. """
        display = Display(self._currentgame.get_game_information(),self._currentgame.get_dungeon_size())
        display.display_game(self._currentgame.get_player().get_position())
        display.display_moves(self._currentgame.get_player().moves_remaining())
        #Display the player’s remaining move count.
        
    def play(self):
        """play out the game"""
        while True:
            self.draw()
            action = input('Please input an action: ')
            if action.split(' ')[0] == 'I':
                if action.split(' ')[1] in DIRECTIONS:
                    #Investigate the direction
                    self._currentgame.get_player().change_move_count(-1)
                    result = self._currentgame.get_entity_in_direction(action.split(' ')[1])
                    print( '{0} is on the {1} side.'.format(result, action.split(' ')[1]))
                else:
                    print(INVALID)
                
            elif action == 'H':
                #Ask for help
                print(HELP_MESSAGE)
            elif action == 'Q':
                #Quit the game
                answer = input('Are you sure you want to quit? (y/n): ')
                if answer == 'y':
                    break
            elif action in DIRECTIONS:
                #Move the player
                self._currentgame.get_player().change_move_count(-1)
                possibility = self._currentgame.get_entity_in_direction(action)
                if possibility == None:
                    self._currentgame.move_player(action)
                elif isinstance(possibility,Key) == True:
                    Key().on_hit(self._currentgame)
                    self._currentgame.move_player(action)
                elif isinstance(possibility,MoveIncrease) == True:
                    MoveIncrease().on_hit(self._currentgame)
                    self._currentgame.move_player(action)
                elif isinstance(possibility,Door) == True:
                    Door().on_hit(self._currentgame)
                    self._currentgame.move_player(action)
                elif isinstance(possibility,Wall) == True:
                    print(INVALID)
            else:
                print(INVALID)

                
            if self._currentgame.won() == True:
                #check if the player has won
                print(WIN_TEXT)
                break
            if self._currentgame.check_game_over() == True:
                #check if the player has lost
                print(LOSE_TEST)
                break

            

       



def main():
    GameApp().play()


if __name__ == "__main__":
    main()


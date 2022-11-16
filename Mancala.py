# Author: Kevin Kuei
# GitHub ID: kckuei
# Course: CS-162
# Date: 2022-11-11, Fri., 7:58
# Description: Implements the cs-162 portfolio project for a console-based implementation of the Mancala board game.
# Uses a composition-ish based approach.
#
# The project solution implements the following classes:
#   Mancala - Mancala class representing the game as played.
#   Player - Player class representing each of the players.
#   Board - Board class representing the Mancala board.
#   Container - Container class representing seed pits/stores.
#
# The smallest abstraction is a Container class that is used to represent seed 'pits' and 'stores'. Containers can
# store seeds, and have attribute pointers to the next pits/store in line (similar to nodes in a tree). Containers can
# also have 'adjacent' attribute pointers (in the case that they are pits), to select opposing player pits. This is
# useful for implementing special game rules such as when a player lands on one of their empty pits with their last
# seed in a given turn.
#
# Pits and stores are strung together through their pointers to create a closed-circuit, which emulates the counter-
# clockwise navigation and traversal of the physical Mancala board.
#
# The Board class is subsequently represented as a collection of Container objects. Given any one of the pointers
# for a pit, the board can be traversed, and seeds distributed amongst them. The pointers for the pits/stores for
# each player are collected/grouped as an attribute in the Board class to create a common access interface. This makes
# manipulation of seed values, in conjunction with the pointers, trivial for tasks such as distributing and transfering
# seeds between other pits and stores.
#
# Players are presented by a trivial Player class with their names.
#
# The Mancala class representing the game as played, builds on the other class abstractions. Each Mancala object
# has two Players, and a Board.
#
# To play a game, simply call:
#       Mancala().new_game()


class Mancala:
    """Mancala class representing the game as played. The class contains information about
    each of the players, and the board.  Uses a composition-based approach.

    Attributes:
        _board      : Board object representing the Mancala board.
        _players    : dictionary of Player objects, where the keys are integers 1 or 2
                        corresponding to player 1 or 2.
        _current    : integer representing the current player 1 or 2 turn.
    """
    def __init__(self):
        """Initializes a Mancala game object."""
        self._board = Board(num_pits=6, num_seeds=4)
        self._players = {1: None, 2: None}
        self._current = 1

    def create_player(self, name):
        """Creates/adds a player to the game."""
        # If player 1 already added, add player 2.
        if self._players[1]:
            self._players[2] = Player(name)
        # Otherwise, add player 1.
        else:
            self._players[1] = Player(name)

    def print_board(self):
        """Prints the current board information PLAINLY, including the store, and pits
        consecutively from 1 to 6 for players 1 and 2, as specified in the README.md.
        Example:
            player1:
            store: 10
            [0, 0, 2, 7, 7, 6]
            player2:
            store: 2
            [5, 0, 1, 1, 0, 7]
            Game has not ended
        """
        self._board.print_board()

    def pretty_print_board(self):
        """Prints the current board information PRETTILY, including the store, and pits
        consecutively from 1 to 6 for players 1 and 2.
        Example:
            Player 2    6   5   4   3   2   1
            ╔═════════╦═══╦═══╦═══╦═══╦═══╦═══╦═════════╗
            ║ Store 2 ║ 5 ║ 5 ║ 0 ║ 4 ║ 4 ║ 5 ║ Store 1 ║
            ║    1    ╠═══╬═══╬═══╬═══╬═══╬═══╣    2    ║
            ║         ║ 5 ║ 4 ║ 0 ║ 1 ║ 6 ║ 6 ║         ║
            ╚═════════╩═══╩═══╩═══╩═══╩═══╩═══╩═════════╝
            Player 1    1   2   3   4   5   6
        """
        self._board.print_fancy_board()

    def return_winner(self):
        """If the game is ended, prints the winner in the following format, as specified
        in the README.md:
            "Winner is player 1 (or 2, based on the actual winner): player’s name"
            If the game is a tie, return "It's a tie";
            If the game is not ended yet, return "Game has not ended"
        """
        # Guard case for game not over.
        if not self._board.is_game_over():
            return "Game has not ended"

        # Otherwise report the winner, or tie scenario.
        winner = self._board.return_winner()
        if winner == 0:
            return "It's a tie"
        elif winner == 1:
            return f"Winner is player 1: {self._players[1].get_name()}"
        else:
            return f"Winner is player 2: {self._players[2].get_name()}"

    def play_game(self, player_idx, pit_idx):
        """Executes a single turn of a player according to the rules of the game, including
        special rules, and updating the seeds number in each pit including the store. It also
        checks the ending state of the game at the end of the play and updates the seed numbers
        in the pit and store for both players according to the rules of the game.

        In accordance with README.md, this method does not enforce turn-based called between players,
        and is implemented purely for grading/testing purposes.

        Call the .new_game method() instead to run a complete game in console with input soliciation.

        Parameters:
            player_idx  : integer representing the player index (1 or 2)
            pit_idx     : integer representing the pit index (1 or 2...or 6)
        Returns:
            If the pit index is not between 1 and 6, inclusive, returns the string "Invalid number for pit index"
            If the game is not over yet, return the string "Game is ended"
            Otherwise, returns a list of the current seed number in the following format:
                [player1 pit1, player1 pit2, player1 pit3, player1 pit4, player1 pit5, player1 pit6, player1 store,
                Player2 pit1, player2 pit2, player2 pit3, player2 pit4, player2 pit5, player2 pit6, player2 store,]

        """
        # Checks for invalid pit index.
        if pit_idx > 6 or pit_idx < 1:
            return "Invalid number for pit index"

        # Play a round of the game according to the rules.
        # The play_turn method on board will print "player <player_number> take another turn" if applicable.
        board = self._board
        board.play_turn(player_idx, pit_idx)

        # If the game is over, perform a final tally by moving any remaining
        # seeds in the pits to their respective player store.
        if self._board.is_game_over():
            self._board.final_tally()
            return "Game is ended"
        # Otherwise, form the return list of seed and store tallies.
        seeds = board.get_pit_seeds(1) + [board.get_store_seeds(1)]   # Player 1 pits + store
        seeds += board.get_pit_seeds(2) + [board.get_store_seeds(2)]  # Player 2 pits + store
        return seeds

    def print_title(self):
        title = ("\u001b[31m"
        "███╗   ███╗ █████╗ ███╗   ██╗ ██████╗ █████╗ ██╗      █████╗\n"
        "████╗ ████║██╔══██╗████╗  ██║██╔════╝██╔══██╗██║     ██╔══██╗\n"
        "██╔████╔██║███████║██╔██╗ ██║██║     ███████║██║     ███████║\n"
        "██║╚██╔╝██║██╔══██║██║╚██╗██║██║     ██╔══██║██║     ██╔══██║\n"
        "██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╗██║  ██║███████╗██║  ██║\n"
        "╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝\n"
        "\u001b[33mFall 2022, CS-162 Portfolio Project\n"
        "\u001b[33mBy Kevin Kuei\n\033[0m")
        print(title)

    def new_game(self):
        """Implements the logic for running a full Mancala game in console properly, with
        input solicitation from players.
        """
        # Print the game title.
        self.print_title()

        # Get the player names.
        player1 = input("Enter player 1 name: ")
        self.create_player(player1)
        player2 = input("Enter player 2 name: ")
        self.create_player(player2)

        # Print the initial board.
        print("\nInitial board:")
        self.pretty_print_board()

        # Enter the main game loop.
        while not self._board.is_game_over():
            # Get the current player's input (pit index).
            pit_idx = self.get_user_input()

            # Play the turn, and store the return skip flag value in skip.
            skip = self._board.play_turn(self._current, pit_idx)

            # Print the board.
            print()
            self.pretty_print_board()

            # Update current player (unless the player gets an extra turn).
            if not skip:
                self.next_player()

        # Perform final tally, and print the final board.
        self._board.final_tally()
        print()
        self.pretty_print_board()

        # Declare winner
        self.return_winner()

    def get_user_input(self, msg="Choose a pit (1-6): "):
        """Gets the user input (pit number), validates, and returns it as an integer.

        Parameters:
            msg : default input prompt."""
        print(f"Player {self._current} ({self._players[self._current].get_name()}) turn.")
        user_input = input(msg)
        while not self.is_valid_input(user_input):
            user_input = input(msg)
        return int(user_input)

    def is_valid_input(self, user_input):
        """Checks if supplied input is valid. The input is valid if it is numeric (i.e.
        can be cast from string to an integer, and is between 1-6, and the pit is not empty.

        Parameters:
            user_input : string representing user input.
        """
        # Checks that the input is numeric and between 1 and 6.
        if not user_input.isnumeric() or not self._board.is_valid_pit(int(user_input)):
            print("Value must be an integer between 1-6!")
            return False

        # Checks that the input is for a pit that is non-zero.
        pit_idx = int(user_input)
        board = self._board.get_board()
        if not board[self._current][pit_idx].get_seeds() > 0:
            print("Player must select a pit that is not empty!")
            return False
        return True

    def next_player(self):
        """Toggles current player turn."""
        if self._current == 1:
            self._current = 2
        else:
            self._current = 1


class Player:
    """Player class for representing a player.
    Attributes:
        _name : string representing the name of the player.
    """
    def __init__(self, name):
        """Initializes a player object."""
        self._name = name

    def get_name(self):
        """Returns the player name."""
        return self._name


class Board:
    """Board class representing the Mancala game board. Uses a composition-based approach.

    The board is represented by a collection of containers that represent the pits
    and stores for player 1 and 2. The containers are connected to form a closed-circuit
    representing the board. Given the location of any pit, we can traverse the board by
    moving in a counter-clockwise direction.

    A board is initialized with number of pits. The pits are initialized with an initial
    number of seeds.

    Board representation:
    | p2    | num_pits | .. | 2   | 1       | p1    |
    | Store | 1        | 2  | ... | num_pits| Store |

    Attributes:
        _num_pits   : integer representing the number of pits to setup the board with.
        _num_seeds  : integer representing the number of seeds to initially seed the pits with.
        _board      : object representing common access interface for the pits; represented by
                        a nested dictionary, where the first level is the player id (1 or 2),
                        and the second level is the Container class (pit/store) id value, either
                        an integer between 1 and num_pits, or 'store'.
    """
    def __init__(self, num_pits=6, num_seeds=4):
        """Initializes Board object."""
        self._num_pits = num_pits
        self._num_seeds = num_seeds
        self._board = None

        # Initializes the board access interface.
        self.setup_board()

    # Public getters
    def get_num_pits(self):
        """Returns the number of pits to setup the board with."""
        return self._num_pits

    def get_num_seeds(self):
        """Returns the number of seeds to seed the pits with."""
        return self._num_seeds

    def get_board(self):
        """Returns the board dictionary/ common access interface."""
        return self._board

    # Public methods
    def setup_board(self):
        """Sets up the Mancala board with appropriate number of seed pits and seeds.
        The board is represented by a chain/closed-circuit of containers representing
        either the seed 'pit' or 'store'.
        """
        # Create player 1 store and pits.
        p1_store = Container('store', 1, 'store')
        p1_pits = [Container(i, 1, 'pit') for i in range(1, self.get_num_pits()+1)]

        # Create player 2 store and pits.
        p2_store = Container('store', 2, 'store')
        p2_pits = [Container(i, 2, 'pit') for i in range(1, self.get_num_pits()+1)]

        # Next, create a closed-circuit for the game board by connecting the containers.
        # First, chain the pits together, consecutively, for player 1 and 2.
        for i in range(0, self.get_num_pits() - 1):
            p1_pits[i].set_next(p1_pits[i + 1])
            p2_pits[i].set_next(p2_pits[i + 1])

        # Next, chains the ends of the stores and pits for player 1 and 2.
        p1_pits[-1].set_next(p1_store)
        p1_store.set_next(p2_pits[0])
        p2_pits[-1].set_next(p2_store)
        p2_store.set_next(p1_pits[0])

        # Set the adjacent nodes, which will be opposing, i.e.
        #   p2: 6 5 4 3 2 1
        #   p1: 1 2 3 4 5 6
        for i in range(0, self.get_num_pits()):
            p1_pits[i].set_adjacent(p2_pits[self.get_num_pits()-1-i])
            p2_pits[i].set_adjacent(p1_pits[self.get_num_pits()-1-i])

        # Initialize all the pits with the specified number of seeds.
        [pit.set_seeds(self.get_num_seeds()) for pit in p1_pits + p2_pits]

        # Create a common access interface for the containers. Represent the board
        # with a nested dictionary, where the first level is player id (1 or 2), and
        # the second is the pit/store id.
        board = {1: {}, 2: {}}
        for pit in p1_pits:
            board[1][pit.get_id()] = pit
        for pit in p2_pits:
            board[2][pit.get_id()] = pit
        board[1]['store'] = p1_store
        board[2]['store'] = p2_store
        self._board = board

    def print_board(self):
        """Prints the current board state.
        Example:
            player1:
            store: 10
            [0, 0, 2, 7, 7, 6]
            player2:
            store: 2
            [5, 0, 1, 1, 0, 7]
            Game has not ended
        """
        print("player1:")
        print(f"store: {self.get_store_seeds(1)}")
        print(self.get_pit_seeds(1))

        print("player2:")
        print(f"store: {self.get_store_seeds(2)}")
        print(self.get_pit_seeds(2))

    def print_fancy_board(self):
        """Prints a fancier board representation.
        Example:
            Player 2    6   5   4   3   2   1
            ╔═════════╦═══╦═══╦═══╦═══╦═══╦═══╦═════════╗
            ║ Store 2 ║ 4 ║ 4 ║ 4 ║ 4 ║ 4 ║ 4 ║ Store 1 ║
            ║    0    ╠═══╬═══╬═══╬═══╬═══╬═══╣    0    ║
            ║         ║ 4 ║ 4 ║ 4 ║ 4 ║ 4 ║ 4 ║         ║
            ╚═════════╩═══╩═══╩═══╩═══╩═══╩═══╩═════════╝
            Player 1    1   2   3   4   5   6
        """
        p1_pits = self.get_pit_seeds(1)
        p2_pits = self.get_pit_seeds(2)
        p1_store = self.get_store_seeds(1)
        p2_store = self.get_store_seeds(2)
        self.get_num_pits()

        txt = "Player 2   " + " ".join([f"{p:^3}" for p in reversed(range(1, self.get_num_pits() + 1))]) + "\n"
        txt += "╔═════════╦" + "═══╦" * self.get_num_pits() + "═════════╗\n"
        txt += "║ Store 2 ║" + "║".join([f"{p:^3}" for p in reversed(p2_pits)]) + "║ Store 1 ║\n"
        txt += f"║ {p2_store:^8}╠" + "═══╬" * (self.get_num_pits()-1) + f"═══╣ {p1_store:^8}║\n"
        txt += "║         ║" + "║".join([f"{p:^3}" for p in p1_pits]) + "║         ║\n"
        txt += "╚═════════╩" + "═══╩" * self.get_num_pits() + "═════════╝\n"
        txt += "Player 1   " + " ".join([f"{p:^3}" for p in range(1, self.get_num_pits() + 1)]) + "\n"
        print(txt)

    def get_pits(self, player):
        """Given the player id, returns the pits in consecutive order.
        Parameters:
          player : integer representing the player id (1 or 2).
        """
        return [item for item in self._board[player].values() if item.get_type() == "pit"]

    def get_pit_seeds(self, player):
        """Given the player id, returns the number of seeds in each pit, as a list.
        Parameters:
          player : integer representing the player id (1 or 2).
        """
        return [pit.get_seeds() for pit in self.get_pits(player)]

    def get_store_seeds(self, player):
        """Given the player id, returns the number of seeds in their store.
        Parameters:
          player : integer representing the player id (1 or 2).
        """
        return self._board[player]['store'].get_seeds()

    def get_empty_pits(self, player):
        """Given the player id, returns a list of booleans representing if the pits are empty.
        Parameters:
          player : integer representing the player id (1 or 2).
        """
        return list(map(lambda x: True if x == 0 else False, self.get_pit_seeds(player)))

    def is_game_over(self):
        """Returns a boolean representing whether the game is over.  The game is over when
         a player has zero seeds left in their pits.
        """
        for player in [1, 2]:
            if all(self.get_empty_pits(player)):
                return True
        return False

    def return_winner(self):
        """Returns the winner (player id), and None if there is no winner.
        The remaining seeds on the player pits should be tallied with the seeds in the player
        stores. The player with the greatest total is the winner.
        Returns:
            Returns an integer (1 or 2) for the winner, 0 for a tie, and None if the game is not over.
        """
        # Guard against invalid winner states.
        if not self.is_game_over():
            return None

        # Get the seed totals for each player (remaining seeds in their pits + store).
        p1_total = sum(self.get_pit_seeds(1)) + self.get_store_seeds(1)
        p2_total = sum(self.get_pit_seeds(2)) + self.get_store_seeds(2)

        # Return the winner.
        # A tie.
        if p1_total == p2_total:
            return 0
        # Player 1 wins.
        elif p1_total > p2_total:
            return 1
        # Player 2 wins.
        else:
            return 2

    def final_tally(self):
        """Performs a final tally by moving any seeds remaining in the pits to their respective
        player store. Can prematurely end the game by removing all the seeds from the pits.
        """
        # Get the store accessors.
        p1_store = self._board[1]['store']
        p2_store = self._board[2]['store']

        # Add the remaining seeds in the pits to the stores.
        p1_store.add_seeds(sum(self.get_pit_seeds(1)))
        p2_store.add_seeds(sum(self.get_pit_seeds(2)))

        # Clear the seeds from the pits.
        [p.clear_seeds() for p in self.get_pits(1)+self.get_pits(2)]

    def play_turn(self, player_id, pit_number):
        """Executes a single player turn if valid. Given a player id and pit number,
        validates the request, then distributes the seeds counter-clockwise around the board.

        Special cases/scenarios:
            i.   Passing opposing player's store -- does not distribute a seed.
            ii.  Last seed lands on player's store -- player gets an additional turn (print this).
            iii. Last seed lands on an empty pit belonging to player -- the last seed and adjacent
                    (opposing player's seeds) get added to the player's store.

        Parameters:
            player_id : integer representing the player id (1 or 2)
            pit_number: integer representing the player pit number (must be between 1 and _num_pits).
        Returns:
            Returns None, except for the case where the player gets another turn--in that case, a
                string 'skip' is returned.
        """
        # Guard cases.
        # Must be valid player number.
        if player_id not in (1, 2):
            print("Invalid player selection. Pick 1 or 2.")
            return

        # Must be valid pit number.
        if not self.is_valid_pit(pit_number):
            print(f"Invalid pit number selection. Pick a number between 1 and {self.get_num_pits()}")
            return

        # Must select a non-empty pit.
        pit = self._board[player_id][pit_number]
        if pit.get_seeds() == 0:
            print("Invalid selection. Player must choose a non-empty pit.")
            return

        # Initialize traversal.
        seed_count = pit.get_seeds()
        pit.clear_seeds()
        current = pit

        # While we still have seeds to distribute.
        while seed_count > 0:

            # Gets the next seed.
            current = current.get_next()

            # If our last piece falls in an empty pit belonging to player, move the seed
            # and adjacent seeds to the player store.
            if seed_count == 1 and current.get_player() == player_id and current.get_type() == 'pit' \
                    and current.get_seeds() == 0:
                # Get the adjacent (opposing player's) pit.
                adjacent = current.get_adjacent()

                # Add the adjacent and current seed to the player store.
                store = self._board[player_id]['store']
                store.add_seeds(adjacent.get_seeds() + 1)

                # Clear the seeds from the adjacent pit.
                adjacent.clear_seeds()

                # Decrement the current seed count.
                seed_count -= 1

            # Otherwise, distribute the seed so long as it's not the opposing player's store.
            elif not (current.get_player() != player_id and current.get_type() == 'store'):
                # Increment the current container.
                current.increment_seeds()

                # Decrement the current seed count.
                seed_count -= 1

            # If our last piece falls in the player store, the player gets another turn, so
            # state that, and return a 'skip' flag.
            if seed_count == 0 and current.get_player() == player_id and current.get_type() == 'store':
                print(f"player {player_id} take another turn")
                return 'skip'

    def is_valid_pit(self, num):
        """Check if pit input number is valid."""
        if num < 1 or num > self._num_pits:
            return False
        return True


class Container:
    """Container Class that can be used to represent a 'pit' or a 'store' for a given player.

    We can chain several such containers to form a closed circuit to make a Mancala board,
    such that given any one of the containers forming the board, one can traverse the
    game board recursively.

    Each container has a player number/id, type (pit or store), number of seeds, and pointers
    to the next or adjacent containers (if pit) in the circuit.

    Collect the access pointers for the pits/stores in one place to provide easy access
    and updating.

    Attributes:
        _id         : integer/string representing unique container id.
        _player     : integer/string representing unique player id.
        _type       : string representing container type ('pit' or 'store').
        _seeds      : integer representing the number of seeds currently stored.
        _next       : Container object representing the next container moving counter-clockwise.
        _adjacent   : Container object representing adjacent (opposing players) pit.
    """
    def __init__(self, container_id, player_id, container_type):
        """Initializes a container."""
        self._id = container_id
        self._player = player_id
        self._type = container_type
        self._seeds = 0
        self._next = None
        self._adjacent = None

    # Public getters
    def get_id(self):
        """Returns the container id."""
        return self._id

    def get_player(self):
        """Returns the player id."""
        return self._player

    def get_type(self):
        """Returns the container type."""
        return self._type

    def get_seeds(self):
        """Returns the number of seeds."""
        return self._seeds

    def get_next(self):
        """Returns the next container."""
        return self._next

    def get_adjacent(self):
        """Returns the opposing (opponent) container."""
        return self._adjacent

    # Public setters
    def set_seeds(self, num):
        """Sets the number of seeds."""
        self._seeds = num

    def add_seeds(self, num):
        """Adds the number of seeds to existing."""
        self._seeds = self._seeds + num

    def set_next(self, nxt):
        """Sets the next node."""
        self._next = nxt

    def set_adjacent(self, adj):
        """Sets the adjacent node."""
        self._adjacent = adj

    # Public methods
    def clear_seeds(self):
        """Removes all the seeds currently stored."""
        self._seeds = 0

    def increment_seeds(self):
        """Increments the number of seeds stored in the container by 1."""
        self._seeds += 1


def demo_1():
    """Example 1 from README.md.
    Expected Output:
        player 1 take another turn
        [4, 4, 0, 5, 5, 5, 1, 4, 4, 4, 4, 4, 4, 0]
        player 2 take another turn
        player1:
        store: 10
        [0, 0, 2, 7, 7, 6]
        player2:
        store: 2
        [5, 0, 1, 1, 0, 7]
        Game has not ended
    """
    game = Mancala()
    game.create_player("Lily")  # player1
    game.create_player("Lucy")  # player2
    print(game.play_game(1, 3))
    game.play_game(1, 1)
    game.play_game(2, 3)
    game.play_game(2, 4)
    game.play_game(1, 2)
    game.play_game(2, 2)
    game.play_game(1, 1)
    game.print_board()
    print(game.return_winner())


def demo_2():
    """Example 2 from README.md.
    Expected Output:
        player 1 take another turn
        player1:
        store: 12
        [0, 0, 0, 0, 0, 0]
        player2:
        store: 36
        [0, 0, 0, 0, 0, 0]
        Winner is player 2: Lucy
    """
    game = Mancala()
    game.create_player("Lily")  # player1
    game.create_player("Lucy")  # player2
    game.play_game(1, 1)
    game.play_game(1, 2)
    game.play_game(1, 3)
    game.play_game(1, 4)
    game.play_game(1, 5)
    game.play_game(1, 6)
    game.print_board()
    print(game.return_winner())


def demo_3():
    """Example 3 using pretty print.
    """
    game = Mancala()
    game.create_player("Sandman")  # player1
    game.create_player("Lucifer")  # player2
    moves = [(1, 4), (2, 4), (1, 3), (1, 1), (2, 1), (1, 2), (1, 4), (1, 5), (2, 1),
             (1, 6), (2, 2), (1, 3), (1, 6), (1, 1), (2, 6), (1, 2), (2, 5), (1, 5),
             (2, 3), (1, 6), (2, 1), (1, 1), (2, 4), (1, 2), (2, 3), (1, 4), (2, 3),
             (1, 6), (1, 5)]
    game.pretty_print_board()
    for move in moves:
        print(f"Player {move[0]} choose pit {move[1]}")
        game.play_game(*move)
        game.pretty_print_board()
    game.return_winner()


def main():
    # demo_1()  # Runs Example 1 from README.md
    # demo_2()  # Runs Example 2 from README.md
    # demo_3()  # Runs Example 3 with pretty print board

    Mancala().new_game()    # Run a complete, new game.


if __name__ == "__main__":
    main()

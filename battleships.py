import random


# Error message
class BoardOutException(Exception):
    def __init__(self, msg="You shot outside of play zone!"):
        self.msg = msg
        Exception.__init__(self, self.msg)


# Position of Ship's X & Y
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Dot):
            return self.x == other.x and self.y == other.y
        return False


class Ship:
    # Ship's stats
    def __init__(self, length, tip, direction):
        self.length = length
        self.tip = tip
        self.direction = direction
        self.lives = length

    def dots(self):
        ship_dots = []
        if self.direction == "Vertical":
            # Vertical Axis
            for i in range(self.length):
                ship_dots.append(Dot(self.tip.x, self.tip.y + i))
        else:  # Horizontal Axis
            for i in range(self.length):
                ship_dots.append(Dot(self.tip.x + i, self.tip.y))
        return ship_dots


# Field
class Board:
    def __init__(self, size, hid=True):
        self.alive_ships = 0
        self.hid = hid
        self.size = size
        self.ships = []
        self.grid = [[' '] * size for _ in range(size)]

    def add_ships(self, ship):
        for dot in ship.dots():
            if self.out(dot) or self.grid[dot.x][dot.y] != ' ':
                raise ValueError("Unable to place a ship here.")
        for dot in ship.dots():
            self.grid[dot.x][dot.y] = 'O'
            self.ships.append(ship)
        self.alive_ships += 1  # Внесены изменеине

    #
    def contour(self, ship):
        for dot in ship.dots():
            for x in range(max(0, self.size - 1), min(self.size, dot.x + 2)):
                for y in range(max(0, self.size - 1), min(self.size, dot.y + 2)):
                    if self.grid[x][y] == ' ':
                        self.grid[x][y] = "X"

    # Checks if Ships are hidden or not
    def is_hidden(self):
        self.hid = True

    def is_not_hidden(self):
        self.hid = False

    # Display a playing field
    def display(self):
        print("  | " + "   ".join(str(i) for i in range(self.size)))
        print("--+" + "----" * 1 * self.size)
        for i, row in enumerate(self.grid):
            row_str = " | ".join(cell if not self.hid or cell != 'O' else ' ' for cell in row)
            print(f"{i} | {row_str}")

    def shot(self, dot):
        if self.out(dot):
            raise ValueError("Point out of the board.")
        if not self.grid[dot.x][dot.y] != 'T':
            raise ValueError("You already shot there.")

        hit_ship = None
        for ship in self.ships:
            if dot in ship.dots():
                ship.lives -= 1
                if ship.lives == 0:
                    self.alive_ships -= 1
                    self.contour(ship)
                hit_ship = ship
                break

        if hit_ship:
            self.grid[dot.x][dot.y] = 'X'
            return True
        else:
            self.grid[dot.x][dot.y] = 'T'
            return False

    def out(self, dot):
        return not (0 <= dot.x < self.size and 0 <= dot.y < self.size)


class Player:
    def __init__(self, own_board, enemy_board):
        self.own_board = own_board
        self.enemy_board = enemy_board

    @staticmethod
    def ask():
        raise NotImplementedError("The ask method should be implemented by subclasses")

    def move(self):
        while True:
            try:
                target = self.ask()
                if self.enemy_board.shot(target):
                    return self.enemy_board.alive_ships > 0
            except ValueError as e:
                print(e)


class User(Player):
    @staticmethod
    def ask():
        while True:
            try:
                x = int(input("Enter X coordinate: "))
                y = int(input("Enter Y coordinate: "))
                shot_dot = Dot(x, y)
                return shot_dot
            except ValueError:
                print("Invalid input. Please enter valid coordinates.")


class AI(Player):
    def ask(self):
        x = random.randint(0, self.enemy_board.size - 1)
        y = random.randint(0, self.enemy_board.size - 1)
        return Dot(x, y)


class Game:
    def __init__(self):
        self.user_board = Board(10, hid=False)
        self.ai_board = Board(10, hid=True)  # True | Скрыть, False | Показать место положение кораблей у противника
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    @staticmethod
    def random_board(board):
        ship_lengths = [3, 2, 2, 1, 1, 1, 1]

        for length in ship_lengths:
            while True:
                direction = random.choice(['Vertical', 'Horizontal'])
                x = random.randint(0, board.size - 1)
                y = random.randint(0, board.size - 1)
                tip = Dot(x, y)

                try:
                    ship = Ship(length, tip, direction)
                    board.add_ships(ship)
                    break
                except ValueError:
                    continue

    def loop(self):
        while self.user_board.alive_ships > 0 and self.ai_board.alive_ships > 0:
            # Display players field
            self.user_board.display()
            self.ai_board.display()

            # Making so player and Ai can do their move. (And for some reason also breaking after losing or winning)
            user_repeat = self.user.move()
            ai_repeat = self.ai.move()
            if not user_repeat:
                self.user_board.display()
                self.ai_board.display()
                print("Congratulations! You won.")
                break
            if not ai_repeat:
                self.user_board.display()
                self.ai_board.display()
                print("Sorry, you lost.")
                break

            # Making sure if player or Ai have 0 Ships on Field
            if self.user_board.alive_ships == 0:
                break

            elif self.ai_board.alive_ships == 0:
                break

    # Start Up
    def start(self):
        self.random_board(self.user_board)
        self.random_board(self.ai_board)
        self.loop()


print("Welcome to Battleship!")
game = Game()
game.start()

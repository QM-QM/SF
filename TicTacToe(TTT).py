def TTTwelcome():
    print("_" * 36)
    print("Welcome to Tic Tac Toe (TTT), In order to play type Coordinates from 0 to 3 -\nX is Horizotnally and Y is Vertically.")
    print("_" * 36)
def TTTfield(field):
    print("XY|   0  |   1  |  2   |   3  |")
    for i, row in enumerate(field):
        inrow = f"{i} | "
        for cell in row:
            inrow += f"  {cell}  | "
        print(inrow)
        print("  |------|------|------|------|")

def TTTask():
    while True:
        c = input('Type "X" and "Y" coords: ').split()
        if len(c) != 2:
            print("Type X and Y position!")
            continue

        x, y = map(int, c)

        if not (0 <= x <= 3) or not (0 <= y <= 3):
            print("Numbers are out of playing zone.")
            continue

        return x,y

def wincond(player, field):
    win_pos = [
        # Horizontal Wins
        ((0, 0), (0, 1), (0, 2), (0, 3)),
        ((1, 0), (1, 1), (1, 2), (1, 3)),
        ((2, 0), (2, 1), (2, 2), (2, 3)),
        ((3, 0), (3, 1), (3, 2), (3, 3)),
        # Vertical Wins
        ((0, 0), (1, 0), (2, 0), (3, 0)),
        ((0, 1), (1, 1), (2, 1), (3, 1)),
        ((0, 2), (1, 2), (2, 2), (3, 2)),
        ((0, 3), (1, 3), (2, 3), (3, 3)),
        # Diagonal Wins
        ((0, 3), (1, 2), (2, 1), (3, 0)),
        ((0, 0), (1, 1), (2, 2), (3, 3))]

    for co in win_pos:
         symbols = [field[x][y] for x, y in co]
         if symbols == [player] * 4:
            return True
    return False

field = [[" "] * 4 for i in range(4)]

TTTwelcome()
TTTfield(field)

current_player = "X"

while True:
    x, y = TTTask()

    if field[x][y] == " ":
        field[x][y] = current_player
    else:
        print("This spot is already taken!")
        continue

    TTTfield(field)

    if wincond(current_player, field):
        print(f"Player {current_player} wins!")
        break

    # Switch player
    current_player = "O" if current_player == "X" else "X"
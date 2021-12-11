class Board:
    def __init__(self, s: str) -> None:
        self.values = [int(x.strip()) for row in s.split("\n") for x in row.split(" ") if len(x.strip()) > 0]
        self.used = [False for x in self.values]

    def mark(self, number: int) -> bool:
        for i in range(len(self.values)):
            if self.values[i] == number:
                self.used[i] = True
                self.lastSeen = number
                return self.check()
        return False
    
    def check(self) -> bool:
        # check rows of 5 and columns of 5
        for i in range(5):
            row = True
            column = True
            for j in range(5):
                row = row and self.used[i*5 + j]
                column = column and self.used[i + j*5]
            if row or column:
                return True
        return False

    def score(self) -> int:
        if not self.check():
            return 0
        score = 0
        for i in range(len(self.values)):
            if self.used[i] == False:
                score += self.values[i]
        return score * self.lastSeen
    
    def reset(self) -> None:
        self.used = [False for x in self.values]

with open("input.txt") as f:
    lines = f.read().split("\n\n")
    guesses = [int(x) for x in lines[0].split(',')]
    boards = []
    for i in range(1, len(lines)):
        boards.append(Board(lines[i]))

for guess in guesses:
    found = False
    for board in boards:
        if board.mark(guess):
            print(f"The winning board for Part 1 is {board.score()}")
            found = True
            break
    if found:
        break

for board in  boards:
    board.reset()

possible_boards = boards
for guess in  guesses:
    if len(possible_boards) > 1:
        next_boards = []
        for board in possible_boards:
            if board.mark(guess):
                pass
            else:
                next_boards.append(board)
        possible_boards = next_boards
    else:
        if possible_boards[0].mark(guess):
            print(f"Last possible board score for Part 2 is {possible_boards[0].score()}")
            break
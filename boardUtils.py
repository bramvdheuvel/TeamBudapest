import csv


class Board:
    def __init__(self):
        self.board = []

    def create(self, path):
        with open(path) as f:
            for row in csv.reader(f):
                int_row = []
                for value in row:
                    int_row.append(int(value))
                self.board.append(int_row)

    def __str__(self):
        return str(self.board)

    def __hash__(self):
        return hash(str(self.board))

    def __eq__(self, other):
        return str(self.board) == other


class Car:
    def __init__(self, id, index, orientation, length):
        self.id = id
        self.index = index
        self.orientation = orientation
        self.length = length

    def __eq__(self, other):
        return self.id == other

    def __str__(self):
        return str(self.id) + ' length:' + str(self.length) + ' orientation:' + self.orientation + ' row or col:' + str(self.index)

    def getmoves(self, parent):
        # checks horizontally orientated cars
        if self.orientation == 'h':
            row = parent.board[self.index]
            try:
                left = row.index(self.id)
                right = left + self.length - 1
                moves = []
                if row[left-1] == 0 and not left == 0:
                    moves.append(-1)
                if row[right + 1] == 0 and not right == len(parent.board):
                    moves.append(1)
            except:
                return moves
            return moves

        # checks vertically orientated cars
        elif self.orientation == 'v':
            col = [row[self.index] for row in parent.board]
            try:
                top = col.index(self.id)
                bottom = top + self.length - 1
                moves = []
                if col[top - 1] == 0 and not top == 0:
                    moves.append(-1)
                if col[bottom + 1] == 0 and not bottom == len(parent.board):
                    moves.append(1)
            except:
                return moves
            return moves

    # Creates a new board / node
    def move(self, number, parent):
        node = parent.board
        if self.orientation == 'h':
            row = node[self.index]

        elif self.orientation == 'v':
            col = [row[self.index] for row in node]

        # Create new board instance
        return node


# gets the cars from the board
def getcars(parent):

    # count occurances of letters
    occurances = []
    for row in parent.board:
        for item in row:
            if not item == 0:
                occurances.append(item)
    lengths = {car: occurances.count(car) for car in occurances}

    # get horizontal cars
    hor = []
    currentCar = parent.board[0][0]
    for row in parent.board:
        for item in row:
            if not item == 0 and currentCar == item:
                if item not in hor:
                    hor.append(Car(item, parent.board.index(row), 'h', lengths.get(item)))
                    lengths.pop(item)
            currentCar = item

    # get vertical cars
    ver = []
    for item in list(set(lengths)):
        for i in range(len(parent.board)-1):
            col = [row[i] for row in parent.board]
            if item in col:
                ver.append(Car(item, i, 'v', lengths.get(item)))

    # combine lists
    return hor + ver
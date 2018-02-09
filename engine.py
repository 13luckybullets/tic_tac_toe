# Creating a logical base for our app


# Function that draw game field
def get_field(num):
    field_output = [['.' for i in range(num)] for j in range(num)]
    return field_output


# Function that update game field after every move
def update_field(field, move, line, point):
    if move % 2 == 0:
        field[line][point] = 'x'
    else:
        field[line][point] = 'o'
    return field


# Check winner after player move
def check_winner(field):

    def check_line(point, line):
        counter = 0
        for j in line:
            if j == point:
                counter += 1
                if counter == 5:
                    return True
            else:
                counter = 0

    def check_cascade(field, point):
        try:
            for i in range(len(field)):
                for j in range(len(field)):
                    if field[i][j] == point and field[i + 1][j + 1] == point and field[i + 2][j + 2] == point \
                            and field[i + 3][j + 3] == point and field[i + 4][j + 4] == point:
                        return True
        except IndexError:
            pass

    # check winner in horizontal line
    for i in field:
        if check_line('x', i) or check_line('o', i):
            return True

    # check winner in vertical line
    for j in zip(*field[::-1]):
        if check_line('x', j) or check_line('o', j):
            return True

    # check winner in cascade line
    if check_cascade(field, "x") or check_cascade(field[::-1], "x") \
            or check_cascade(field, "o") or check_cascade(field[::-1], "o"):
        return True

    return False


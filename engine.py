

def get_field(num):
    field_output = [['.' for i in range(num)] for j in range(num)]
    return field_output


def update_field(field, move, line, point):
    if move % 2 == 0:
        field[line][point] = 'o'
    else:
        field[line][point] = 'x'
    return field


def check_winner(field):

    def check_line(point, line):
        counter = 0
        for j in line:
            if j == point:
                counter += 1
                if counter == 5:
                    return True

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

    if check_cascade(field, "x") or check_cascade(field[::-1], "x") \
            or check_cascade(field, "o") or check_cascade(field[::-1], "o"):
        return True

    return False



# a = get_field(20)
# work = update_field(a, 1, 0, 0)
# work = update_field(a, 3, 1, 1)
# work = update_field(a, 3, 2, 2)
# work = update_field(a, 3, 3, 3)
# work = update_field(a, 3, 4, 4)
#
# print(check_winner(work))

# a = get_field(20)
# work = update_field(a, 1, 14, 14)
# work = update_field(a, 1, 15, 15)
# work = update_field(a, 3, 16, 16)
# work = update_field(a, 3, 17, 17)
# work = update_field(a, 3, 18, 18)
#
# print(check_winner(work))
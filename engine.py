

def get_field():
    field_output = [['.' for i in range(20)] for j in range(20)]
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

    def check_cascade(check_field):
        work_lst = []
        first = 0
        second = 5
        while first != 16:
            matrx = check_field[first:second]
            for i in range(5):
                matrx[i] = matrx[i][i:]
                work_lst.append(matrx[i])
            first += 1
            second += 1

        for j in tuple(zip(*work_lst[::-1])):
            if check_line('x', j) or check_line('o', j):
                return True

    # check winner in horizontal line
    for i in field:
        if check_line('x', i) or check_line('o', i):
            return True

    # check winner in vertical line
    for j in tuple(zip(*field[::-1])): #?????????????????????????????????????????????????
        if check_line('x', j) or check_line('o', j):
            return True

    # check winner in cascade line
    if check_cascade(field) or check_cascade(field[::-1]):
        return True

    return False





# a = get_field()
# work = update_field(a, 1, 0, 0)
# work = update_field(a, 3, 1, 1)
# work = update_field(a, 3, 2, 2)
# work = update_field(a, 3, 3, 3)
# work = update_field(a, 3, 4, 4)
#
#
# print(check_winner(work))

# a = get_field()
# work = update_field(a, 1, 14, 14)
# work = update_field(a, 1, 15, 15)
# work = update_field(a, 3, 16, 16)
# work = update_field(a, 3, 17, 17)
#
#
# print(check_winner(work))
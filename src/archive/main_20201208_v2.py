import random
import itertools

class TicTacToeGame:
    def __init__(self):
        self.turn = int(input("PC first: 0, User first: 1."))  # True: O, False: X
        self.table = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    def get_now_turn(self):
        return 'O' if self.turn else 'X'

    def get_checkerboard(self):
        """
        format checkerboard and return
        """
        return '\n'.join(['\t'.join([{1: 'O', -1: 'X'}.get(j, ' ') for j in i]) for i in self.table])

    def update(self, place):
        i = (place - 1) // 3
        j = (place - 1) % 3
        if self.table[i][j] != 0:
            return False

        value = 1 if self.turn else -1  # 1 -> O, -1 -> X, 0 -> empty
        self.table[i][j] = value
        return True

    def check(self):
        """
        :return: True -> someone win, False -> Nobody win, None -> tie
        """
        # 檢查列
        for line in self.table:
            if abs(sum(line)) == 3:
                return True

        # 檢查行
        for i in zip(*self.table):
            if abs(sum(i)) == 3:
                return True

        # 檢查 1, 5, 9
        if abs(sum([self.table[i][i] for i in range(3)])) == 3:
            return True

        # 檢查 3, 5, 7
        if abs(sum([self.table[i][2 - i] for i in range(2, -1, -1)])) == 3:
            return True

        if 0 not in itertools.chain(*self.table):
            return None

        return False

    def switch_user(self):
        self.turn = not self.turn

    def computer_choice(self):
        check_value_list = [-2, 2, -1]
        for v in check_value_list:
            for i, line in enumerate(self.table):
                if sum(line) == v:
                    if 0 not in line:
                        continue

                    return i * 3 + line.index(0) + 1

            for i, line in enumerate(zip(*self.table)):
                if sum(line) == v:
                    if 0 not in line:
                        continue

                    return line.index(0) * 3 + i + 1

            line = [self.table[i][i] for i in range(3)]
            if sum(line) == v and 0 in line:
                i = line.index(0)
                return i * 3 + i + 1

            line = [self.table[i][2 - i] for i in range(3)]
            if sum(line) == v and 0 in line:
                i = line.index(0)
                return i * 3 + (2 - i) + 1

        t = itertools.chain(*self.table)
        return random.choice([i + 1 for i, j in enumerate(t) if (j == 0 and i != 4 and counter == 0)])

    def swap(self, x, y, a, b):
        self.table[a][b] = self.table[x][y]
        self.table[x][y] = 0
        
    def blue_win(self):
        for i in range(3):
            for j in range(3):
                if self.table[i][j] == -1:
                    if i - 1 >= 0 and j - 1 >= 0 and self.table[i - 1][j - 1] == 0:
                        swap(i, j, i - 1, j - 1)
                        if check() == True:
                            print('Player {} win!\n'.format(get_now_turn()))
                            return True
                        else:
                            swap(i - 1, j - 1, i, j)
                    if i - 1 >= 0 and self.table[i - 1][j] == 0:
                        swap(i, j, i - 1, j)
                        if check() == True:
                            print('Player {} win!\n'.format(get_now_turn()))
                            return True
                        else:
                            swap(i - 1, j, i, j)
                    if i - 1 >= 0 and j + 1 <= 2 and self.table[i - 1][j + 1] == 0:
                        swap(i, j, i - 1, j + 1)
                        if check() == True:
                            print('Player {} win!\n'.format(get_now_turn()))
                            return True
                        else:
                            swap(i - 1, j + 1, i, j)
                    if j + 1 <= 2 and self.table[i][j + 1] == 0:
                        swap(i, j, i, j + 1)
                        if check() == True:
                            print('Player {} win!\n'.format(get_now_turn()))
                            return True
                        else:
                            swap(i, j + 1, i, j)
                    if i + 1 <= 2 and j + 1 <= 2 and self.table[i + 1][j + 1] == 0:
                        swap(i, j, i + 1, j + 1)
                        if check() == True:
                            print('Player {} win!\n'.format(get_now_turn()))
                            return True
                        else:
                            swap(i + 1, j + 1, i, j)
                    if i + 1 <= 2 and self.table[i + 1][j] == 0:
                        swap(i, j, i + 1, j)
                        if check() == True:
                            print('Player {} win!\n'.format(get_now_turn()))
                            return True
                        else:
                            swap(i + 1, j, i, j)
                    if i + 1 <= 2 and j - 1 >= 0 and self.table[i + 1][j - 1] == 0:
                        swap(i, j, i + 1, j - 1)
                        if check() == True:
                            print('Player {} win!\n'.format(get_now_turn()))
                            return True
                        else:
                            swap(i + 1, j - 1, i, j)
                    if j - 1 >= 0 and self.table[i][j - 1] == 0:
                        swap(i, j, i, j - 1)
                        if check() == True:
                            print('Player {} win!\n'.format(get_now_turn()))
                            return True
                        else:
                            swap(i, j - 1, i, j)
        return False
    
    def blue_block(self):
        check_value_list = [2]
        for v in check_value_list:
            for i, line in enumerate(self.table):
                if sum(line) == v:
                    if 0 not in line:
                        continue
                    for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if i + _i >= 0 and i + _i <= 2 and line.index(0) + _j >= 0 and line.index(0) + _j <= 2:
                                if self.table[i + _i][line.index(0) + _j] == -1:
                                    swap(i + _i, line.index(0) + _j, i, line.index(0))
                                    return True

            for i, line in enumerate(zip(*self.table)):
                if sum(line) == v:
                    if 0 not in line:
                        continue
                    for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if line.index(0) + _i >= 0 and line.index(0) + _i <= 2 and i + _j >= 0 and i + _j <= 2:
                                if self.table[line.index(0) + _i][i + _j] == -1:
                                    swap(line.index(0) + _i, i + _j, line.index(0), i)      
                                    return True          

            line = [self.table[i][i] for i in range(3)]
            if sum(line) == v and 0 in line:
                i = line.index(0)
                for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if i + _i >= 0 and i + _i <= 2 and i + _j >= 0 and i + _j <= 2:
                                if self.table[i + _i][i + _j] == -1:
                                    swap(i + _i, i + _j, i, i)
                                    return True

            line = [self.table[i][2 - i] for i in range(3)]
            if sum(line) == v and 0 in line:
                i = line.index(0)
                for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if i + _i >= 0 and i + _i <= 2 and (2 - i) + _j >= 0 and (2 - i) + _j <= 2:
                                if self.table[i + _i][(2 - i) + _j] == -1:
                                    swap(i + _i, (2 - i) + _j, i, (2 - i))
                                    return True
        return False

    def white_win(self):
        check_value_list = [2]
        for v in check_value_list:
            for i, line in enumerate(self.table):
                count = 0
                if sum(line) == v and 0 in line:
                    for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if i + _i >= 0 and i + _i <= 2 and line.index(0) + _j >= 0 and line.index(0) + _j <= 2:
                                if self.table[i + _i][line.index(0) + _j] == 1:
                                    count += 1
                                if count == 3:
                                    return True      
            
            for i, line in enumerate(zip(*self.table)):
                count = 0
                if sum(line) == v:
                    if 0 not in line:
                        continue
                    for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if line.index(0) + _i >= 0 and line.index(0) + _i <= 2 and i + _j >= 0 and i + _j <= 2:
                                if self.table[line.index(0) + _i][i + _j] == 1:
                                    count += 1
                                if count == 3:
                                    return True 

            line = [self.table[i][i] for i in range(3)]
            if sum(line) == v and 0 in line:
                count = 0
                i = line.index(0)
                for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if i + _i >= 0 and i + _i <= 2 and i + _j >= 0 and i + _j <= 2:
                                if self.table[i + _i][i + _j] == 1:
                                    count += 1
                                if count == 3:
                                    return True 

            line = [self.table[i][2 - i] for i in range(3)]
            if sum(line) == v and 0 in line:
                count = 0
                i = line.index(0)
                for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if i + _i >= 0 and i + _i <= 2 and (2 - i) + _j >= 0 and (2 - i) + _j <= 2:
                                if self.table[i + _i][(2 - i) + _j] == 1:
                                    count += 1
                                if count == 3:
                                    return True
        return False

    def random_pc(self):
        for i in range(3):
            for j in range(3):
                if self.table[i][j] == 0:
                    for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if i + _i >= 0 and i + _i <= 2 and line.index(0) + _j >= 0 and line.index(0) + _j <= 2:
                                if self.table[i + _i][line.index(0) + _j] == -1:
                                    swap(i + _i, line.index(0) + _j, i, line.index(0))
                                if white_win() == True:
                                    swap(i, line.index(0), i + _i, line.index(0) + _j)
                                else:
                                    return
                                
def check_input(value):
    return 0 < value < 10


def user_input():
    while True:
        value = input('Place you want to put: ')
        if not value.isdigit():
            print('You should input a number\n')
            continue

        value = int(value)
        if not check_input(value):
            print('The number you input is not between 1 and 9\n')
            continue

        return value


def main(counter):
    game = TicTacToeGame()
    # not with computer -- > True
    # with computer -- > False
    print()
    

    while True:
        print('It\'s {} turn.'.format(game.get_now_turn()))
        value = user_input() if game.turn else game.computer_choice()

        if not game.turn:
            print('Computer choice to put at:', value)

        if not game.update(value):
            print('This place can not be put\n')
            continue

        result = game.check()
        print(game.get_checkerboard() + '\n')
        
        counter += 1
        if counter == 6:
            break

        if result is None:
            print('Tie')
            break

        if result:
            print('Player {} win!\n'.format(game.get_now_turn()))
            break

        game.switch_user()
        print('-' * 30)

    while True:
        if game.blue_win == True:
            break



if __name__ == '__main__':
    counter = 0
    main(counter)

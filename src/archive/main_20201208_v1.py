import random
import itertools


class TicTacToeGame:
    def __init__(self):
        self.turn = input("User first: 1, PC first: 0.")  # True: O, False: X
        print(self.turn)
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
        return random.choice([i + 1 for i, j in enumerate(t) if j == 0])


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


def main():
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
        if result is None:
            print('Tie')
            break

        if result:
            print('Player {} win!\n'.format(game.get_now_turn()))
            break

        game.switch_user()
        print('-' * 30)


if __name__ == '__main__':
    main()

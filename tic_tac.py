"""
On table:
0 - blank
1 - X
2 - 0

"""


class Game(object):
    def __init__(self, x, y):
        self.__pretty_res = ''
        self.free_list = []
        self.table = []
        self.log = []
        self.winner = 0

        self.create_table(x, y)

    def create_table(self, x, y):
        for x_pos in range(x):
            self.table.append(list())
            for y_pos in range(y):
                self.table[x_pos].append(0)

    def action(self, act_type, x_pos, y_pos):
        if self.winner != 0:
            return {'status': 1, 'desc': 'Game finished', 'winner': self.winner}
        try:

            if self.table[x_pos][y_pos] != 0:
                return {'status': 3, 'desc': 'OverWrite Error'}

            self.table[x_pos][y_pos] = act_type
        except IndexError:
            return IndexError

        # Check on X
        if self.table[0][0] == self.table[0][1] == self.table[0][2] and self.table[0][0] in [1, 2]:
            self.winner = self.table[0][0]
        if self.table[1][0] == self.table[1][1] == self.table[1][2] and self.table[1][0] in [1, 2]:
            self.winner = self.table[1][0]
        if self.table[2][0] == self.table[2][1] == self.table[2][2] and self.table[2][0] in [1, 2]:
            self.winner = self.table[2][0]

        # Check on Y
        if self.table[0][0] == self.table[1][0] == self.table[2][0] and self.table[0][0] in [1, 2]:
            self.winner = self.table[0][0]
        if self.table[0][1] == self.table[1][1] == self.table[2][1] and self.table[0][1] in [1, 2]:
            self.winner = self.table[0][1]
        if self.table[0][2] == self.table[1][2] == self.table[2][2] and self.table[0][2] in [1, 2]:
            self.winner = self.table[0][2]

        # Line on rotate
        if self.table[0][0] == self.table[1][1] == self.table[2][2] and self.table[0][0] in [1, 2]:
            self.winner = self.table[0][0]
        if self.table[0][2] == self.table[1][1] == self.table[2][0] and self.table[0][2] in [1, 2]:
            self.winner = self.table[0][2]

        # Check on draw
        new_listed = list()
        for i in self.table:
            for item in i:
                new_listed.append(item)

        if 0 not in new_listed:
            self.winner = 3

        self.log.append([[x_pos, y_pos], act_type])
        if self.winner != 0:
            return {'status': 2, 'desc': 'Last step. Win', 'winner': self.winner}
        else:
            return {'status': 0, 'desc': 'Ok'}

    def pretty_table(self, changed=True):
        self.__pretty_res = ''
        for i in self.table:
            self.__pretty_res += str(i) + '\n'
        return self.__pretty_res

    def free_step(self):
        self.free_list = []
        for y_pos in range(len(self.table)):
            for x_pos in range(len(self.table[y_pos])):
                if self.table[y_pos][x_pos] == 0:
                    self.free_list.append([y_pos, x_pos])
        return self.free_list

    def get_log(self):
        return self.log


if __name__ == '__main__':
    gg = Game(3, 3)
    status = 0
    combinations = []
    while status not in [1, 2]:

        gg.action(1, 0, 1)
    print(gg.pretty_table())
    print(gg.free_step())

import collections
import itertools
import copy

class LotoShukei:
    def __init__(self, df, count:int):
        balls = []
        df_temp = df.drop(columns='NUMBER')
        for index, row in df_temp.iterrows():
            balls.append(row.values.tolist())

        self.balls = balls
        self.count = count

    def get_range(self, min:int=0, max:int=None):
        return self.balls[min:max]

    def get_count(self, min:int=0, max:int=-1):
        list = self.get_range(min, max)
        return collections.Counter([x for row in list for x in row])

    def get_best(self, min:int=0, max:int=None, top:int=10):
        return self.__get_rank(min=min, max=max, top=top, reverse=True)

    def get_worst(self, min:int=0, max:int=None, top:int=10):
        return self.__get_rank(min=min, max=max, top=top, reverse=False)

    def __get_rank(self, reverse:bool, min:int=0, max:int=None, top:int=10):
        ball = self.get_count(min, max)
        temp = 0
        rank = 0
        same_rank = 0
        rank_list = []
        for k, v in sorted(ball.items(), reverse=reverse, key=lambda x:x[1]):
            rank += 1
            if temp != v:
                temp = v
                same_rank = rank
            if top < same_rank: break
            rank_list.append(k)

        return rank_list

    def get_max_index(self):
        return len(self.balls)

    def get_worst_4_top(self, top:int):
        all_table = self.balls
        list = [0] * self.count
        reverse = all_table[::-1]
        for row in reverse:
            for col in row:
                list[col -1] += 1
            if top+1 >= list.count(0):
                l = [i +1 for i in range(self.count) if 0 == list[i]]
                return tuple(l[:top])

    def get_best_4_top(self, limit:int):
        ball = self.get_count(min=-10)
        list = []
        for k, v in sorted(ball.items(), reverse=True, key=lambda x:x[1]):
            list.append(k)
        return list[:limit]

    def make_box_list(self, list, sc:int=1):
        sc -= 1
        if 0 > sc:
            return [list]

        temp_list =[]
        for i in list:
            copy_list = copy.copy(list)
            copy_list.remove(i)
            temp_list.append(copy_list)

        temp_list2 =[]
        for l in temp_list:
            for l2 in self.make_box_list(l, sc):
                temp_list2.append(l2)

        ret_list =[]
        for l in temp_list2:
            if not l in ret_list: ret_list.append(l)

        return ret_list

if __name__ == '__main__':
    import sqlite3
    import pandas

    conn = sqlite3.connect('LOTO.db')
    df = pandas.read_sql('SELECT * FROM LOTO6', conn)
    conn.close()

    loto_shukei = LotoShukei(df, 43)
    list = loto_shukei.make_box_list([1, 2, 3, 4, 5, 6, 7], 2)
    print(list)

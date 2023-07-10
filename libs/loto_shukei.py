import collections
import itertools

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
            if top >= list.count(0):
                return tuple([i +1 for i in range(self.count) if 0 == list[i]])

    def get_best_4_top(self, limit:int):
        ball = self.get_count(min=-10)
        list = []
        for k, v in sorted(ball.items(), reverse=True, key=lambda x:x[1]):
            list.append(k)
        return list[:limit]

if __name__ == '__main__':
    import sqlite3
    import pandas

    conn = sqlite3.connect('LOTO.db')
    df = pandas.read_sql('SELECT * FROM LOTO6', conn)
    conn.close()

    loto_shukei = LotoShukei(df, 43)
    print(loto_shukei.get_best_4_top(4))

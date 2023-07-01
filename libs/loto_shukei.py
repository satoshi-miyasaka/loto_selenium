class LotoShukei:
    def __init__(self, df, count:int):
        balls = []
        df_temp = df.drop(columns='NUMBER')
        for index, row in df_temp.iterrows():
            balls.append(tuple(row.values))

        self.balls = tuple(balls)
        self.count = count

    def get_range(self, min:int=0, max:int=-1):
        return self.balls[min:max]

    def get_count(self, min:int=0, max:int=-1, under:int=-1):
        list = [0] * self.count
        for row in self.get_range(min, max):
            for col in row:
                list[col -1] += 1

        return tuple((i +1, list[i]) for i in range(self.count) if under <= list[i])

    def get_top(self, min:int=0, max:int=-1, top:int=10):
        return self.__get_rank(min=min, max=max, top=top, reverse=True)

    def get_worst(self, min:int=0, max:int=-1, top:int=10):
        return self.__get_rank(min=min, max=max, top=top, reverse=False)

    def __get_rank(self, reverse:bool, min:int=0, max:int=-1, top:int=10):
        ball = self.get_count(min, max)
        temp = 0
        rank = 0
        same_rank = 0
        rank_list = []
        for n, m in sorted(ball, reverse=reverse, key=lambda x:x[1]):
            rank += 1
            if temp != m:
                temp = m
                same_rank = rank
            if top < same_rank: break
            rank_list.append(n)

        return tuple(rank_list)

if __name__ == '__main__':
    import sqlite3
    import pandas

    conn = sqlite3.connect('LOTO.db')
    df = pandas.read_sql('SELECT * FROM LOTO6', conn)
    conn.close()

    loto_shukei = LotoShukei(df, 43)
    # print(loto_shukei.get_count(max=10, under=3))
    print(loto_shukei.get_worst(min=-10, top=3))

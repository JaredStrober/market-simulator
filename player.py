class Player():

    def __init__(self, balance, holdings):

        self.balance = balance
        self.holdings = holdings


    def subtract_money(self, amount):
        self.balance -= amount


    def add_money(self, amount):
        self.balance += amount


patrik = Player(10_000, {'Apple': 10, 'Netflix': 4, 'Amazon': 8})

from market import market

class Security():

    def __init__(self, name, ticker, volume, price, volatility):
        self.name = name
        self.ticker = ticker
        self.volume = volume
        self.price = price
        self.volatility = volatility

        self.add_itself_to_list()


    def change_price(self):
        demand = market.demand
        sentiment = market.sentiment
        change = market.calculate_change(self.price, market.demand, market.sentiment,
                                         self.volatility)

        self.price += change
        self.price = round(self.price, 2)


    def add_itself_to_list(self):
        securities_objects.append(self)


securities_objects = []

apple = Security("Apple", "AAP", 1000, 200, 500)
netflix = Security("Netflix","NFLX", 1000, 250, 100)
amazon = Security("Amazon", "AMZN", 1000, 50, 400)
facebook = Security("Facebook", "FB", 1000, 10, 300)
berkshire = Security("Berkshire", "BRK", 1000, 1500, 1000)
tesla = Security("Tesla", "TSLA", 1000, 414, 400)
microsoft = Security("Microsoft", "MSFT", 1000, 120, 600)


#TODO nahodne generovat volatilitu jednotlivych aktiv, hra je tak zabavnejsia,
#hrac si nebude vediet zapamatat ktore aktivum je ako volatilne

#TODO adjustovat sentiment/pokles-rast ceny podla toho, ci je aktivum v demande, alebo nie

#TODO vyriesit co sa stane ak security hitne 0. zda sa, ze nulu nikdy nehitne, kvoli zaokruhlovaniu,
# takze treba urobit nejaky case, kedy firma zbankrotuje uplne. napriklad ak bude mat akcia hodnotu
# pod 0.5 dolaru, v jednom pripade z x mozeme pushnut okno, ze firma skrachovala a odstranit ju
# zo zoznamu.. !!!!UPDATE!!!: zda sa, ze 0.14 je rock bottom, menej sa nezobrazuje, asi kvoli 
# zakruhlovaniu.. UPDATE: niekedy sa to zasekne na 0.14, inokedy pokracuje aj nizsie

#TODO TIP: volatilita nemusi byt staticka, moze sa menit kazdych x iteracii. zaimplementovat ako
#@property metodu jednotlivych sekucurities

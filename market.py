import random

class Market():

    #def __init__(self, divider):
        #	# The lower this value, the more volatile a security becomes.
        #	divider = self.divider


    @property
    def old_demand(self):
    # DEPRECATED in favour of the "demand" method below.
            demand = random.choice([True, False])
            return demand


    @property
    def demand(self):
        """
        (Kinda) randomly generate the value of the demand
        variable. This functionality was handled by the now
        deprecated "old_demand" variable, but using it caused
        the value of a security to drop more often than not,
        rendering the game un-winnable.
        """

        # Adjusting this variable tips the fortune. The higher it is, 
        # more fortunate is the fate. 506 seems to be the perfect balance.
        chance = 506

        digit = random.randint(1,1000)

        if digit in range(1,chance):
                return True
        else:
                return False


    @property
    def sentiment(self):
    #Randomly generate the value of the sentiment variable. 
            sentiment = random.randint(1,10)
            return sentiment


    def calculate_change(self, price, demand, sentiment, volatility):
            """
            Calculate change in price.
            :param price: <float> Current price of a security.
            :param demand: <bool> Is commodity in demands?
            :param sentiment: <int> Strength of the sentiment (1 to 10).

            :return: <float> Degree of change.
            """

            if demand == True:
                    # Return positive value.
                    change = (price/volatility) * sentiment
                    return change
            else:
                    # Return negative value.
                    change = (price/volatility) * sentiment * -1
                    return change

market = Market()

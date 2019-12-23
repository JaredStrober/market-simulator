import sys
import time
import threading

from securities import securities_objects
from market import market
from player import patrik

from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout,
QApplication, QDialog, QMainWindow, QFrame, QGroupBox, QListWidget)


class Example(QDialog):
#class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.title = "Market simulator"
        self.top = 200
        self.left = 200
        self.width = 700
        self.height = 500

        self.initUI()

#--------------------------------------------------------------------------------------#

    def initUI(self):
        """
        Main, top-level function that calls all the other functions which have anything
        to do with constructing the UI and sets the UI parameters.
        """

        # Set the window title and geometry.
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Defining the main layout, for now it's an HBox.
        main_layout = QHBoxLayout()

        # Calling the UI constructing functions.
        self.UI_securities_grid_layout()
        self.UI_player_stats(patrik)

        # Adding the UI elements into the main layout.
        main_layout.addWidget(self.securities_groupbox)
        main_layout.addWidget(self.player_groupbox)

        # Set the main layout, show the window.
        self.setLayout(main_layout)
        self.show()

        self.run_functions()

#--------------------------------------------------------------------------------------#

    def UI_securities_grid_layout(self):
        """
        Table of securities and their prices.
        """

        # Create the securities titles QLabels.
        self.security_names_QLabels = [QLabel(security.name) for security in securities_objects]
        # Create the securities price QLabels.
        self.security_prices_QLabels = [QLabel(str(security.price)) for security in securities_objects]

        # Create the grid layout to set tickers and prices in.
        self.securities_grid = QGridLayout()

        # Set widgets into the grid layout.
        x_position = 1
        for name, price in zip(self.security_names_QLabels, self.security_prices_QLabels):
            self.securities_grid.addWidget(name, x_position, 0)
            self.securities_grid.addWidget(price, x_position, 1)
            x_position += 1

        # Create the buy button. 
        buy_button = QPushButton(f'Buy shares')
        buy_button.clicked.connect(self.popup)
        self.securities_grid.addWidget(buy_button, x_position, 0)

        # Create a groupbox.
        self.securities_groupbox = QGroupBox("Stocks")
        self.securities_groupbox.setLayout(self.securities_grid)


#--------------------------------------------------------------------------------------#

    def UI_player_stats(self, player):

        self.player_vbox = QVBoxLayout()
        self.player_grid = QGridLayout()

        # Player's money QLabel
        self.player_money = QLabel(f"Balance: {player.balance}")

        x_position = 0
        y_position = 0

        for i in player.holdings:
            self.player_grid.addWidget(QLabel(i), x_position, y_position)
            y_position += 1
            self.player_grid.addWidget(QLabel(str(player.holdings[i])), x_position, y_position)
            x_position += 1
            y_position -= 1


        self.player_vbox.addWidget(self.player_money)
        self.player_vbox.addLayout(self.player_grid)

        self.player_vbox.addWidget
        self.player_groupbox = QGroupBox("Player stats")
        self.player_groupbox.setLayout(self.player_vbox)

#--------------------------------------------------------------------------------------#

    # Updating the player's money.
    def UI_update_money(self, player):

        def update_money(player):
            while True:
                self.player_money.setText(f"Balance: {player.balance}")
                time.sleep(0.04)

        money_update_thread = threading.Thread(target=update_money, args=(player,))
        money_update_thread.start()


    def popup(self):
        self.dialog = PopupDialog()
        self.dialog.show()
#--------------------------------------------------------------------------------------#

    def update_all_prices(self, securities_objects):
        """
        Function for updating price labels of all securities.

        securities_objects (list): List containing all security objects to be updated.
        securities_objects (list): List containing QLabels of security prices.
        """

        while True:

            index = 0

            for security in securities_objects:
                demand = market.demand
                sentiment = market.sentiment
                difference = market.calculate_change(security.price, demand, sentiment, security.volatility)
                security.change_price(difference)
                self.security_prices_QLabels[index].setText(str(security.price))
                index += 1

            time.sleep(1)


    def price_update_threading(self, securities_objects):
        """
        Declare and run thread for price updating.
        """
        price_update_thread = threading.Thread(target=self.update_all_prices, args=(securities_objects,))
        price_update_thread.start()

#--------------------------------------------------------------------------------------#

    def run_functions(self):
        """
        Method for grouping and running other non-UI related functions.
        """

        # Call to the threading function that takes care of periodically updating the prices.
        self.price_update_threading(securities_objects)

        # Call to the threading function that updates the player's money.
#        self.money_update_threading(patrik)
        self.UI_update_money(patrik)

#--------------------------------------------------------------------------------------#

class PopupDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.title = "Buy stocks"
        self.top = 200
        self.left = 200
        self.width = 400
        self.height = 300

        # Set the window title and geometry.
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Setting the layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Create the list of securities.
        self.stocks_list = QListWidget()

        for i, stock in enumerate(securities_objects):
            self.stocks_list.insertItem(i, stock.name)

        self.stocks_list.clicked.connect(self.showitem)

        layout.addWidget(self.stocks_list)

    def showitem(self):
        item = self.stocks_list.currentItem()
        print(item.text())


if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

from securities import apple, netflix, netflix
from market import market
from player import patrik
import time

securities = [apple, netflix, netflix]


def main():

	for i in range(10):
		demand = market.demand
		sentiment = market.sentiment
		change = market.calculate_change(apple.price, demand, sentiment, apple.volatility)
		apple.change_price(change)
		print(apple.price)
		time.sleep(0.6)

if __name__ == "__main__":
    main()

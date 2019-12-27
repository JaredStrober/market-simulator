import sys
import time
import threading

from securities import securities_objects
from services import update_all_prices
from player import patrik

from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout,
QApplication, QDialog, QMainWindow, QFrame, QGroupBox, QListWidget, QLineEdit)

from PyQt5.QtGui import QIntValidator


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
        self.trade_button = QPushButton(f'Trade shares')
        self.trade_button.clicked.connect(self.show_TradeShares)

        # Create a VBox
        self.shares_vbox = QVBoxLayout()

        self.shares_vbox.addLayout(self.securities_grid)
        self.shares_vbox.addWidget(self.trade_button)

        # Create a groupbox.
        self.securities_groupbox = QGroupBox("Stocks")
        self.securities_groupbox.setLayout(self.shares_vbox)


#--------------------------------------------------------------------------------------#

    def UI_player_stats(self, player):

        self.player_vbox = QVBoxLayout()

        # Player's money QLabel
        self.player_money = QLabel(f"Balance: {player.balance}")

        # Portfolio button
        self.portfolio_button = QPushButton(f"Portfolio")
        self.portfolio_button.clicked.connect(self.show_portfolio)

        self.player_vbox.addWidget(self.player_money)
        self.player_vbox.addWidget(self.portfolio_button)

        self.player_groupbox = QGroupBox("Player stats")
        self.player_groupbox.setLayout(self.player_vbox)

#--------------------------------------------------------------------------------------#

    def UI_update_share_prices(self):

        def update_share_prices():

            while True:

                update_all_prices(securities_objects)

                for share, label in zip(securities_objects, self.security_prices_QLabels):
                    label.setText(str(share.price))

                time.sleep(0.5)

        share_prieces_update_thread = threading.Thread(target=update_share_prices)
        share_prieces_update_thread.start()


    # Updating the player's money.
    def UI_update_money(self, player):

        def update_money(player):
            while True:
                self.player_money.setText(f"Balance: {player.balance}")
                time.sleep(0.04)

        money_update_thread = threading.Thread(target=update_money, args=(player,))
        money_update_thread.start()

#--------------------------------------------------------------------------------------#

    def show_TradeShares(self):
        self.trade_shares_dialog = TradeShares()
        self.trade_shares_dialog.show()

    def show_portfolio(self):
        self.portolio_dialog = Portfolio()
        self.portolio_dialog.show()

#--------------------------------------------------------------------------------------#

    def run_functions(self):
        # Method for grouping and running other non-UI related functions.
        self.UI_update_share_prices()
        self.UI_update_money(patrik)

#--------------------------------------------------------------------------------------#

class TradeShares(QDialog):

    def __init__(self):
        super().__init__()

        self.title = "Trade shares"
        self.top = 200
        self.left = 200
        self.width = 400
        self.height = 300

        # Set the window title and geometry.
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Setting the layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.UI_trading_layout()


    def UI_trading_layout(self):

        # Layout contaning the below buttons layout and shares list.
        self.horizontal_layout = QHBoxLayout()

        # Layout containing line edit and buttons.
        self.vertical_layout_buttons = QVBoxLayout()

        # Create the list of securities.
        self.stocks_list = QListWidget()

        for i, stock in enumerate(securities_objects):
            self.stocks_list.insertItem(i, stock.name)

        # Create the line edit
        self.line_edit_volume = QLineEdit()
        self.line_edit_volume.setPlaceholderText("Amount")
        self.line_edit_volume.setValidator(QIntValidator(1,100_000_000))

        # Buttons
        self.buy_button = QPushButton(f"Buy")
        self.buy_button.clicked.connect(self.buy_shares)

        self.sell_button = QPushButton(f"Sell")
        self.sell_button.clicked.connect(self.sell_shares)

        self.close_button = QPushButton(f"Close")
        self.close_button.clicked.connect(self.close)

        # Status line
        self.status_line = QLabel(f"")

        # Populate the vertical layout with buttons.
        self.vertical_layout_buttons.addWidget(self.line_edit_volume)
        self.vertical_layout_buttons.addWidget(self.buy_button)
        self.vertical_layout_buttons.addWidget(self.sell_button)
        self.vertical_layout_buttons.addWidget(self.close_button)

        # Populate the horizontal layout.
        self.horizontal_layout.addWidget(self.stocks_list)
        self.horizontal_layout.addLayout(self.vertical_layout_buttons)

        # Populate the veritcal layout.
        self.main_layout.addLayout(self.horizontal_layout)
        self.main_layout.addWidget(self.status_line)


    def UI_change_status_line(self, string):

        def change_status_line(string):
            self.status_line.setText(string)
            time.sleep(2)
            self.status_line.setText(f"")

        status_line_thread = threading.Thread(target=change_status_line, args=(string,))
        status_line_thread.start()


    def buy_shares(self):

        selection = self.stocks_list.currentItem().text()
        volume = int(self.line_edit_volume.text())

        # Find the selcted share's object.
        for share in securities_objects:
            if share.name == selection:
                total_price = volume * share.price

        if patrik.check_balance(total_price) == False:
            self.UI_change_status_line(f"Not enough funds.")
        elif selection in patrik.holdings:
            patrik.holdings[selection] += volume
            self.UI_change_status_line(f"Transaction OK.")
        else:
            self.UI_change_status_line(f"Transaction OK.")
            patrik.holdings[selection] = volume


    def sell_shares(self):

        selection = self.stocks_list.currentItem().text()
        volume = int(self.line_edit_volume.text())

        # Find the selcted share's object.
        for share in securities_objects:
            if share.name == selection:
                total_price = volume * share.price

        if selection in patrik.holdings:
            if volume < patrik.holdings[selection]:
                patrik.holdings[selection] -= volume
                self.UI_change_status_line(f"Transaction OK.")
            elif volume == patrik.holdings[selection]:
                del patrik.holdings[selection]
                self.UI_change_status_line(f"Transaction OK.")
            elif volume > patrik.holdings[selection]:
                self.UI_change_status_line(f"You only own {patrik.holdings[selection]} shares, not {volume}.")
        else:
            self.UI_change_status_line(f"You don't own these shares")


class Portfolio(QDialog):

    def __init__(self):
        super().__init__()

        self.title = "Portfolio"
        self.top = 200
        self.left = 200
        self.width = 400
        self.height = 300

        # Set the window title and geometry.
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.UI_portfolio_layout()


    def UI_portfolio_layout(self):
        self.portfolio_grid = QGridLayout()
        self.setLayout(self.portfolio_grid)

        index_x = 0
        index_y = 0

        if not patrik.holdings:
            self.portfolio_grid.addWidget(QLabel("Portfolio Empty"))
        else:
            for share in patrik.holdings:
                self.portfolio_grid.addWidget(QLabel(share), index_x, index_y)
                index_y += 1
                self.portfolio_grid.addWidget(QLabel(str(patrik.holdings[share])), index_x, index_y)
                index_y = 0
                index_x += 1


        self.close_button = QPushButton(f"Close")
        self.close_button.clicked.connect(self.close)

        self.portfolio_grid.addWidget(self.close_button)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    main()


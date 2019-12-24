from securities import securities_objects

def update_all_prices(securities_objects):

        index = 0

        for share in securities_objects:
            share.change_price()
            index += 1



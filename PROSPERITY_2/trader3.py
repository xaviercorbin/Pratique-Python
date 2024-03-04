from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class WALLogEntry:
    def __init__(self, action: str, product: str, price: int, amount: int):
        self.action = action
        self.product = product
        self.price = price
        self.amount = amount

    def apply(self):
        # This method would apply the log entry to the system
        pass

class Trader:
    def __init__(self):
        self.log = []

    def write_log(self, entry: WALLogEntry):
        # In a real system, this method would write the log to a persistent storage
        # For simplicity, we're just appending to a list here
        self.log.append(entry)
        print(f"Logged: {entry.action} {entry.amount}x at {entry.price} for {entry.product}")

    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            acceptable_price = 10
            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))

            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if int(best_ask) < acceptable_price:
                    log_entry = WALLogEntry("BUY", product, best_ask, -best_ask_amount)
                    self.write_log(log_entry)
                    orders.append(Order(product, best_ask, -best_ask_amount))

            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if int(best_bid) > acceptable_price:
                    log_entry = WALLogEntry("SELL", product, best_bid, -best_bid_amount)
                    self.write_log(log_entry)
                    orders.append(Order(product, best_bid, -best_bid_amount))

            result[product] = orders

        traderData = "SAMPLE"
        conversions = 1
        return result, conversions, traderData

    # Additional functionality for recovery (not fully implemented)
    def recover(self):
        # This method would process each entry in the log to recover state
        pass

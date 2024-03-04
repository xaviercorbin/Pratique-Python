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
        # Apply the log entry to the system
        pass

class Trader:
    def __init__(self):
        self.log = []

    def write_log(self, entry: WALLogEntry):
        self.log.append(entry)
        print(f"Logged: {entry.action} {entry.amount}x at {entry.price} for {entry.product}")

    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            
            # Calculate dynamic acceptable price based on mid-price and volatility or spread
            mid_price = (max(order_depth.buy_orders.keys(), default=0) + min(order_depth.sell_orders.keys(), default=0)) / 2
            spread = min(order_depth.sell_orders.keys(), default=mid_price) - max(order_depth.buy_orders.keys(), default=mid_price)
            acceptable_price = mid_price + spread * 0.1  # Adjust this factor based on desired aggressiveness
            
            print(f"Acceptable price for {product}: {acceptable_price}")
            print("Buy Order depth : ", len(order_depth.buy_orders), ", Sell order depth : ", len(order_depth.sell_orders))

            # Volume Weighted Strategy for BUY orders
            for price, amount in sorted(order_depth.sell_orders.items()):
                if price < acceptable_price:
                    volume_weighted_price = price  # Simple example, can be more complex
                    log_entry = WALLogEntry("BUY", product, volume_weighted_price, -amount)
                    self.write_log(log_entry)
                    orders.append(Order(product, volume_weighted_price, -amount))
                    break  # Remove break to consider more levels

            # Volume Weighted Strategy for SELL orders
            for price, amount in sorted(order_depth.buy_orders.items(), reverse=True):
                if price > acceptable_price:
                    volume_weighted_price = price  # Simple example, can be more complex
                    log_entry = WALLogEntry("SELL", product, volume_weighted_price, amount)
                    self.write_log(log_entry)
                    orders.append(Order(product, volume_weighted_price, -amount))
                    break  # Remove break to consider more levels

            result[product] = orders

        traderData = "SAMPLE"
        conversions = 1
        return result, conversions, traderData

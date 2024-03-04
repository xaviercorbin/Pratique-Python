import json
import jsonpickle
from typing import Dict, List

# Definitions for types used in the classes
Time = int
Symbol = str
Product = str
Position = int
UserId = str
ObservationValue = int

class Listing:
    def __init__(self, symbol: Symbol, product: Product, denomination: Product):
        self.symbol = symbol
        self.product = product
        self.denomination = denomination

class ConversionObservation:
    def __init__(self, bidPrice: float, askPrice: float, transportFees: float, exportTariff: float, importTariff: float, sunlight: float, humidity: float):
        self.bidPrice = bidPrice
        self.askPrice = askPrice
        self.transportFees = transportFees
        self.exportTariff = exportTariff
        self.importTariff = importTariff
        self.sunlight = sunlight
        self.humidity = humidity

class Observation:
    def __init__(self, plainValueObservations: Dict[Product, ObservationValue], conversionObservations: Dict[Product, ConversionObservation]) -> None:
        self.plainValueObservations = plainValueObservations
        self.conversionObservations = conversionObservations

    def __str__(self) -> str:
        return "(plainValueObservations: " + jsonpickle.encode(self.plainValueObservations) + ", conversionObservations: " + jsonpickle.encode(self.conversionObservations) + ")"

class Order:
    def __init__(self, symbol: Symbol, price: int, quantity: int) -> None:
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

class OrderDepth:
    def __init__(self) -> None:
        self.buy_orders: Dict[int, int] = {}
        self.sell_orders: Dict[int, int] = {}

    # Calculate Weighted Average Price
    def weighted_average_price(self, orders: Dict[int, int]) -> float:
        if not orders:
            return 0.0
        total_value = sum(price * abs(quantity) for price, quantity in orders.items())
        total_quantity = sum(abs(quantity) for quantity in orders.values())
        return total_value / total_quantity if total_quantity else 0

class Trade:
    def __init__(self, symbol: Symbol, price: int, quantity: int, buyer: UserId=None, seller: UserId=None, timestamp: int=0) -> None:
        self.symbol = symbol
        self.price = price
        self.quantity = quantity
        self.buyer = buyer
        self.seller = seller
        self.timestamp = timestamp

class TradingState:
    def __init__(self,
                 traderData: str,
                 timestamp: Time,
                 listings: Dict[Symbol, Listing],
                 order_depths: Dict[Symbol, OrderDepth],
                 own_trades: Dict[Symbol, List[Trade]],
                 market_trades: Dict[Symbol, List[Trade]],
                 position: Dict[Product, Position],
                 observations: Observation):
        self.traderData = traderData
        self.timestamp = timestamp
        self.listings = listings
        self.order_depths = order_depths
        self.own_trades = own_trades
        self.market_trades = market_trades
        self.position = position
        self.observations = observations

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

class Trader:
    def __init__(self):
        self.position_limits = {
            "AMETHYSTS": 20,
            "STARFRUIT": 20
        }

    def run(self, state: TradingState):
        result: Dict[str, List[Order]] = {}

        for product in ["AMETHYSTS", "STARFRUIT"]:
            orders: List[Order] = []
            order_depth: OrderDepth = state.order_depths.get(product, OrderDepth())

            # Calculate Weighted Average Prices for buy and sell orders
            wap_buy = order_depth.weighted_average_price(order_depth.buy_orders)
            wap_sell = order_depth.weighted_average_price(order_depth.sell_orders)

            # Determine fair value as the average of WAP buy and sell if both are available
            fair_value = (wap_buy + wap_sell) / 2 if wap_buy and wap_sell else max(wap_buy, wap_sell)

            # Adjust trading decisions based on WAP strategy
            if wap_sell and wap_sell < fair_value:
                quantity = self.position_limits[product] - state.positions.get(product, 0)
                if quantity > 0:
                    orders.append(Order(product, wap_sell, quantity))

            if wap_buy and wap_buy > fair_value:
                quantity = self.position_limits[product] + state.positions.get(product, 0)
                if quantity > 0:
                    orders.append(Order(product, wap_buy, -quantity))

            result[product] = orders

        return result, 0, ""  # No conversions for this strategy
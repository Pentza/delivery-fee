from datetime import datetime
from dateutil.parser import isoparse

def minimal_value(cart_value: int) -> float:
    """
    Returns small order surcharge if cart value is under 10€ and over 0€, else return 0.0
    The surcharge is the difference between the cart value and 10€.

            Parameters:
                cart_value (int): The value of the shopping cart in cents
    
            Examples:
                cart_value = 890 (8.90€), return 1.10€
    """

    cart_value = cart_value / 100
    if cart_value >= 10 or cart_value <= 0:
        return 0.0

    return 10 - cart_value

def distance_delivery_fee(distance: int) -> int:
    """
    Returns the delivery fee based on distance to the destination.

    A delivery fee for the first 1000 meters (=1km) is 2€.
    1€ is added for every additional 500 meters.
    If the distance would be shorter than 500 meters, the minimum fee is always 1€.

            Parameters:
                distance (int): Distance to the destination in meters

            Examples:
                1499 meters => 2€ base fee + 1€ for the additional 500 m => 3€
                1500 meters => 2€ base fee + 1€ for the additional 500 m => 3€
                1501 meters => 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€
    """
    
    # Minimum fee is 1€
    fee = 1

    # If distance is under 1km, return minimum fee
    if distance < 1000:
        return fee

    # Else, add 1€ to get the first 1km 2€ fee
    distance -= 1000
    fee += 1

    # Remove one from the distance if distance mod 500 is 0.
    # Without this 1500m distance would cost you 4€ not 3€.
    if distance % 500 == 0:
        distance -= 1

    # Return the fee plus the possible additional 500m fee(s)
    return fee + distance // 500 + 1

def item_amount_fee(item_amount: int) -> float:
    """
    Returns small surcharge if cart has more than 4 items.
    Surcharge amount is 0.50€ for each item above four.

        Parameters:
            item_amount (int): the amount of items in the shopping cart

        Examples:
            Number of items is 4, no extra surcharge
            Number of items is 5, 50 cents surcharge is added
            Number of items is 10, 3€ surcharge (6 x 50 cents) is added
    """
    if item_amount - 4 <= 0:
        return 0.0
    else:
        return 0.5 * (item_amount - 4)

def maximum_fee(amount: float) -> float:
    """
    Returns 15€ if the fee amount is above it, else returns the fee.
    As the delivery fee can never be more than 15€, including possible surcharges.

            Parameters:
            amount (float): the amount of fees, including possible surcharges

        Examples:
            amount = 16.20€, returns 15€
            amount = 3.65€ returns 3.65€
    """
    if amount < 0.0:
        return 0.0
    elif amount > 15.0:
        return 15.0
    else:
        return amount

def friday_rush_hour(date_time: str) -> bool:
    """
    Returns boolean value if friday and rush hour.
    Friday rush hour is on fridays 3PM - 7PM UTC.

        Parameters:
            date_time (str): datetime string in ISO format
    """
    dt = isoparse(date_time)

    # 0 == monday, 1 == tuesday ... 4 == friday
    if dt.weekday() != 4:
        return False

    start = datetime(1, 1, 1, 15).time()
    end = datetime(1, 1, 1, 19).time()
    
    # return true if time is between 3PM (15) and 7PM (19) else false
    return start <= dt.time() <= end

def delivery_fee(cart_value: int=0, distance: int=0, item_amount: int=0, date_time: str='') -> float:
    """
    Returns total delivery fee, based on carts value, delivery distance and item amount in cart.
    There are few special cases described next.
        1. The delivery fee can never be more than 15€, including possible surcharges.
        2. The delivery is free (0€) when the cart value is equal or more than 100€.
        3. During the Friday rush (3 - 7 PM UTC),
           the delivery fee (the total fee including possible surcharges) will be multiplied by 1.1x.
           However, the fee still cannot be more than the max (15€).

        Parameters:
            cart_value  (int):  The value of the shopping cart in cents
            distance    (int):  Distance to the destination in meters
            item_amount (int):  The amount of items in the shopping cart
            date_time   (str):  Datetime string in ISO format
    """

    if cart_value / 100 >= 100:
        return 0.0


    total_delivery_fee = (
        minimal_value(cart_value) +
        distance_delivery_fee(distance) +
        item_amount_fee(item_amount)
        )

    if friday_rush_hour(date_time):
        total_delivery_fee *= 1.1

    total_delivery_fee = maximum_fee(total_delivery_fee)
    
    return total_delivery_fee

    

    

    
    


import unittest
from random import random
from ..delivery_fee import (
    minimal_value,
    distance_delivery_fee, 
    item_amount_fee, maximum_fee, 
    friday_rush_hour,
    delivery_fee
)
from datetime import datetime


class TestSurcharge(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_minimal_value_returns_zero_with_negative_value(self):
        self.assertEqual(0.0, minimal_value(-2054))

    def test_minimal_value_returns_zero_with_value_over_10(self):
        self.assertEqual(0.0, minimal_value(2054))

    def test_minimal_value_returns_correct_surcharge(self):
        self.assertAlmostEqual(0.0, minimal_value(0))
        self.assertAlmostEqual(9.9, minimal_value(10))
        self.assertAlmostEqual(0.1, minimal_value(990))
        self.assertAlmostEqual(4.5, minimal_value(550))

    def test_delivery_fee_returns_one_with_less_than_500_meters(self):
        self.assertEqual(1, distance_delivery_fee(-20))
        self.assertEqual(1, distance_delivery_fee(0))
        self.assertEqual(1, distance_delivery_fee(499))
    
    def test_delivery_fee_returns_2_with_500_or_over_and_less_or_equal_to_1000(self):
        self.assertEqual(1, distance_delivery_fee(500))
        self.assertEqual(1, distance_delivery_fee(501))
        self.assertEqual(2, distance_delivery_fee(1000))

    def test_delivery_fee_returns_correct_amounts_for_over_1000(self):
        self.assertEqual(3, distance_delivery_fee(1001))
        self.assertEqual(3, distance_delivery_fee(1499))
        self.assertEqual(3, distance_delivery_fee(1500))

        self.assertEqual(4, distance_delivery_fee(1501))
        self.assertEqual(4, distance_delivery_fee(1999))
        self.assertEqual(4, distance_delivery_fee(2000))

        self.assertEqual(5, distance_delivery_fee(2001))
        self.assertEqual(5, distance_delivery_fee(2499))
        self.assertEqual(5, distance_delivery_fee(2500))

    def test_item_amount_fee_with_less_than_5_items(self):
        for i in range(-1, 5):
            self.assertEqual(0.0, item_amount_fee(i))

    def test_item_amount_fee_with__5_or_more_items(self):
        self.assertEqual(0.50, item_amount_fee(5))
        self.assertEqual(1.50, item_amount_fee(7))
        self.assertEqual(3, item_amount_fee(10))

    def test_maximum_fee_returns_0_with_negative_value(self):
        self.assertEqual(0.0, maximum_fee(-1))

    def test_maximum_fee_returns_value_with_value_between_0_and_15(self):
        self.assertEqual(0.0, maximum_fee(0))
        for _ in range(15):
            rand = random() * 15
            self.assertEqual(rand, maximum_fee(rand))
        self.assertEqual(15.0, maximum_fee(15.0))

    def test_maximum_fee_returns_15_with_value_above_15(self):
        self.assertEqual(15.0, maximum_fee(15.01))
        self.assertEqual(15.0, maximum_fee(27.9))

    def test_friday_rush_hour_with_non_friday(self):
        dt = datetime(2022, 1, 1, 16, 0, 0) # Jan 1st 2022 = saturday
        self.assertFalse(friday_rush_hour(dt.isoformat()))

    def test_friday_rush_hour_with_friday_but_wrong_time(self):
        dt = datetime(2021, 12, 31, 19, 0, 1) # Dec 31st 2021 = friday
        self.assertFalse(friday_rush_hour(dt.isoformat()))
        dt.replace(hour=14, minute=59, second=59)
        self.assertFalse(friday_rush_hour(dt.isoformat()))

    def test_friday_rush_hour_with_friday_and_correct_time(self):
        dt = datetime(2021, 12, 31, 15, 0, 0)
        self.assertTrue(friday_rush_hour(dt.isoformat()))
        dt.replace(hour=17, minute=31, second=11)
        self.assertTrue(friday_rush_hour(dt.isoformat()))
        dt.replace(hour=19, minute=0, second=0)
        self.assertTrue(friday_rush_hour(dt.isoformat()))

    def test_delivery_fee_returns_0_with_cart_value_over_100(self):
        cart_value_in_cents = 10000 # 100€
        self.assertAlmostEqual(0.0, delivery_fee(cart_value=cart_value_in_cents))
        cart_value_in_cents = 10001 # 100.01€
        self.assertAlmostEqual(0.0, delivery_fee(cart_value=cart_value_in_cents))

    def test_delivery_fee_returns_correct_amount_with_test_input(self):
        cart_value_in_cents = 790
        delivery_distance = 2235
        number_of_items = 4
        time = '2021-10-12T13:00:00Z'
        self.assertAlmostEqual(
            7.10, 
            delivery_fee(
                cart_value=cart_value_in_cents,
                distance=delivery_distance,
                item_amount=number_of_items,
                date_time=time
                )
            )

    def test_delivery_fee_returns_correct_amount_with_test_input_and_its_friday(self):
        cart_value_in_cents = 790
        delivery_distance = 2235
        number_of_items = 4
        time = '2021-12-31T16:00:00Z'
        self.assertAlmostEqual(
            7.10 * 1.1, 
            delivery_fee(
                cart_value=cart_value_in_cents,
                distance=delivery_distance,
                item_amount=number_of_items,
                date_time=time
                )
            )






    




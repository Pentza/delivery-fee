from flask import Flask, request
from .delivery_fee import delivery_fee

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_world():
    data = request.get_json()
    if not data:
        return "<p>Hello, World!</p>"

    fee = delivery_fee(
        data['cart_value'],
        data['delivery_distance'],
        data['number_of_items'],
        data['time']
    )

    return str(fee)

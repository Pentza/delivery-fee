from flask import Flask, request
from dateutil.parser import isoparse
from .delivery_fee import delivery_fee

app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_delivery_fee():
    data = request.get_json(silent=True)

    if not data:
        return {'code': 400, 'message': 'Bad request'}, 400

    for key in (['cart_value', 'delivery_distance', 'number_of_items', 'time']):
        if key not in data:
            return {'code': 400, 'message': f'payload missing {key}'}, 400

    try:
        isoparse(data['time'])
    except ValueError:
        return {'code': 400, 'message': 'malformatted time'}, 400

    fee = delivery_fee(
        data['cart_value'],
        data['delivery_distance'],
        data['number_of_items'],
        data['time']
    )

    return {'delivery_fee': fee}, 200

@app.errorhandler(404)
def page_not_found():
    return 'This page does not exist', 404

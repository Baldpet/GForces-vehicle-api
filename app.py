import os
import uuid
import datetime
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo



app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config["MONGO_DBNAME"] = 'GForces'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)


@app.route('/api/create', methods=['POST'])
def create():
    try:
        order = mongo.db.orders
        order_date = datetime.datetime.now()
        order_number = uuid.uuid4().hex
        order.insert_one({
            'order_number': order_number,
            'order_date': order_date,
        })

        context = {
            'order_number': order_number
        }

        return context
    except:
        return Response(status=500)


@app.route('/api/update/<order_number>', methods=['POST'])
def update(order_number):
    try:
        if 'vehicle_manufacturer' in request.args:
            vehicle_manufacturer = request.args['vehicle_manufacturer']
        else:
            vehicle_manufacturer = None
        if 'model' in request.args:
            model = request.args['model']
        else:
            model = None
        if 'total_price' in request.args:
            total_price = request.args['total_price']
        else:
            total_price = None

        order = mongo.db.orders

        order.update_one({'order_number': order_number},
                        {'$set': {'vehicle_manufacturer': vehicle_manufacturer,
                                'model': model,
                                'total_price': total_price
                                }
                        })

        return Response(status=200)
    except:
        return Response(status=500)




if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')), debug=True)

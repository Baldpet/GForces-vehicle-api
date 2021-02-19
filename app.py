import os
import uuid
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from flask_apscheduler import APScheduler
from bson.objectid import ObjectId


class config(object):
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(config())
app.secret_key = os.urandom(24)

app.config["MONGO_DBNAME"] = 'GForces'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@scheduler.task('cron', id='do_job', hour='1')
def job():
    order = mongo.db.orders
    orders = order.find({})
    for item in orders:
        date = item.get('order_date')
        three_days = datetime.now() - timedelta(days=3)
        if date < three_days:
            order_id = ObjectId(item.get('_id'))
            order.delete_one({'_id': order_id})


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
        order = mongo.db.orders

        if 'vehicle_manufacturer' in request.args:
            vehicle_manufacturer = request.args['vehicle_manufacturer']
            order.update_one({'order_number': order_number},
                             {'$set': {'vehicle_manufacturer': vehicle_manufacturer}})
        if 'model' in request.args:
            model = request.args['model']
            order.update_one({'order_number': order_number},
                             {'$set': {'model': model}})
        if 'total_price' in request.args:
            total_price = request.args['total_price']
            order.update_one({'order_number': order_number},
                             {'$set': {'total_price': total_price}})

        return Response(status=200)
    except:
        return Response(status=500)


@app.route('/api/view/<order_number>', methods=['GET'])
def view(order_number):
    try:
        order = mongo.db.orders

        order_info = order.find_one({'order_number': order_number}, {
            '_id': False,
            'order_number': True,
            'model': True,
            'vehicle_manufacturer': True,
            'total_price': True
        })

        return order_info
    except:
        return Response(status=500)


@app.route('/api/view_all', methods=['GET'])
def view_all():
    order = mongo.db.orders

    all_orders_cur = order.find({}, {
        '_id': False,
        'order_number': True,
        'model': True,
        'vehicle_manufacturer': True,
        'total_price': True
    })

    all_orders = []
    for order in all_orders_cur:
        all_orders.append(order)

    return jsonify(all_orders)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')), debug=True)

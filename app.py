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






if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')), debug=True)

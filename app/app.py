#!/usr/bin/env python3
import os
import datetime

import pandas as pd
from flask import Flask, jsonify, request, render_template, make_response, Response
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'iVNbrpodsdYpfgge2jshQaU4dXQH9zVj'
mongo = MongoClient(os.environ['MONGO_MLAB_URI'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    data = request.json
    if _has_registed_before(data):
        return jsonify({'status': 'error', 'data': data, 'error': '您已经报名过了，请不要重复提交'})
    
    data['timestamp'] = datetime.datetime.utcnow()
    registration_id = mongo.stock_trader.registration.insert_one(data).inserted_id

    data['_id'] = str(registration_id)

    return jsonify({'status': 'success', 'data': data})


@app.route("/download_csv")
def download_csv():
    
    registrations = list(mongo.stock_trader.registration.find())
    df = pd.DataFrame(registrations)
    csv = df.to_csv(encoding='utf-8')

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=registrations.csv"})


def _has_registed_before(data):

    from_db = list(mongo.stock_trader.registration.find({
        'name': data['name'],
        'city': data['city'],
        'occupation': data['occupation'],
        'phone': data['phone'],
        'wechat': data['wechat'],
        'referrer': data['referrer'],
        'location': data['location']
    }))

    if from_db:
        return True
    
    return False


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

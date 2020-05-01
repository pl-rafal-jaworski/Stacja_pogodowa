import flask
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from datetime import datetime
import time
import json

# from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///database.db')
print(db_connect)
app = Flask(__name__)
api = Api(app)


def getEmojiAndDesc(temp):
    if temp < 5:
        ret = 'Zimno'
        emoji = "❄️"
    elif 5 <= temp < 15:
        ret = "Chłodno"
        emoji = "☀️"
    elif 15 <= temp < 23:
        ret = 'Ciepło'
        emoji = "🌞"
    elif 23 <= temp < 28:
        ret = "Gorąco"
        emoji = "⛱️"
    else:
        ret = "Upalnie"
        emoji = "🔥"

    return [ret, emoji]


@app.route('/', methods=['GET'])
class NewestTemp(Resource):
    def get(self):
        temp = 'N/A'

        conn = db_connect.connect()
        query = conn.execute('SELECT "wartosc" FROM "temp" ORDER BY id DESC LIMIT 1')

        response = flask.jsonify({'temp': i[0] for i in query.cursor.fetchall()})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


class NewestPressure(Resource):
    def get(self):
        temp = 'N/A'

        conn = db_connect.connect()
        query = conn.execute('SELECT "wartosc" FROM "cisnienie" ORDER BY id DESC LIMIT 1')

        response = flask.jsonify({'cisnienie': i[0] for i in query.cursor.fetchall()})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


class NewestPM(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute('SELECT "wartosc" FROM "pm25" ORDER BY id DESC LIMIT 1')

        response = flask.jsonify({'pm': i[0] for i in query.cursor.fetchall()})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


class NewestTimestamp(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute('SELECT "updateTime" FROM "timestamp" ORDER BY id DESC LIMIT 1')

        db_receive = {i[0] for i in query.cursor.fetchall()}
        db_rec = list(db_receive)

        timestamp = int(db_rec[0])
        timestamp = datetime.fromtimestamp(timestamp)
        timestamp = timestamp.strftime("%H:%M:%S %d/%m/%Y")

        response = flask.jsonify({'timestamp': timestamp})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


class NewestTempDesc(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute('SELECT "wartosc" FROM "temp" ORDER BY id DESC LIMIT 1')
        db_receive = {i[0] for i in query.cursor.fetchall()}
        db_rec = list(db_receive)

        temp = db_rec[0]
        ret, emoji = getEmojiAndDesc(temp)

        ret.encode('unicode-escape')

        response = flask.jsonify({'desc': ret, 'emoji': emoji})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


class PastData(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT temp, cisnienie, pm, timestamp FROM 'historyczne' ORDER BY id DESC LIMIT 5")

        db_receive = query.cursor.fetchall()
        db_rec = list(db_receive)

        ret = []

        for i in range(0, 5):
            temp = db_rec[i][0]
            desc, emoji = getEmojiAndDesc(temp)

            timestamp = int(db_rec[i][3])
            timestamp = datetime.fromtimestamp(timestamp)
            timestamp = timestamp.strftime("%H:%M:%S %d/%m/%Y")

            ret += [{"temp": db_rec[i][0], "cisnienie": db_rec[i][1], "pm": db_rec[i][2], "timestamp": timestamp, "emoji": emoji, "description": desc}]

        response = flask.jsonify(ret)
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


api.add_resource(NewestTemp, '/NewestTemp')
api.add_resource(NewestPressure, '/NewestPressure')
api.add_resource(NewestPM, '/NewestPM')
api.add_resource(NewestTimestamp, '/NewestTimestamp')
api.add_resource(NewestTempDesc, '/NewestTempDesc')
api.add_resource(PastData, '/PastData')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port='5002')

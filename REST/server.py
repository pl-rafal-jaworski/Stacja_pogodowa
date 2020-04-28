import flask
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

# from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///database.db')
print(db_connect)
app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
class NewestTemp(Resource):
    def get(self):
        temp = 'N/A'

        conn = db_connect.connect()
        query = conn.execute('SELECT "wartosc" FROM "temp" ORDER BY id DESC LIMIT 1')

        response = flask.jsonify({'temp': i[0] for i in query.cursor.fetchall()})
        response.headers.add('Access-Control-Allow-Origin', '*')
        print(response)

        return response


class NewestPressure(Resource):
    def get(self):
        temp = 'N/A'

        conn = db_connect.connect()
        query = conn.execute('SELECT "wartosc" FROM "cisnienie" ORDER BY id DESC LIMIT 1')

        response = flask.jsonify({'cisnienie': i[0] for i in query.cursor.fetchall()})
        response.headers.add('Access-Control-Allow-Origin', '*')
        print(response)

        return response



class NewestPM(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute('SELECT "wartosc" FROM "pm25" ORDER BY id DESC LIMIT 1')

        response = flask.jsonify({'pm': i[0] for i in query.cursor.fetchall()})
        response.headers.add('Access-Control-Allow-Origin', '*')
        print(response)

        return response


class NewestTimestamp(Resource):
    def get(self):
        temp = 'N/A'

        conn = db_connect.connect()
        query = conn.execute('SELECT "updateTime" FROM "timestamp" ORDER BY id DESC LIMIT 1')

        response = flask.jsonify({'timestamp': i[0] for i in query.cursor.fetchall()})
        response.headers.add('Access-Control-Allow-Origin', '*')
        print(response)

        return response


api.add_resource(NewestTemp, '/NewestTemp')
api.add_resource(NewestPressure, '/NewestPressure')
api.add_resource(NewestPM, '/NewestPM')
api.add_resource(NewestTimestamp, '/NewestTimestamp')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port='5002')

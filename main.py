import flask
import requests
import datetime
import logging
from flask import Flask
from flask import Response

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class GCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime())
    g_code_file = db.Column(db.String(256))
    g_code_name = db.Column(db.String(256))

    def __init__(self, timestamp, g_code_file, g_code_name):
        self.timestamp = timestamp
        self.g_code_file = g_code_file
        self.g_code_name = g_code_name

@app.route('/gcode', methods=['POST'])
def svg_to_gcode():
    request_json=flask.request.json
    g_code_file=request_json['g_code_file']
    g_code_name=request_json['g_code_name']
    timestamp_data=request_json['time_stamp']

    if ".gcode" not in g_code_file:
        logging.error("Wrong file extension")
        return Response("Wrong file extension", status=400)

    try:
        query = GCode(
        g_code_file=g_code_file,
        g_code_name=g_code_name,
        timestamp=datetime.datetime.utcnow()
    )
        db.session.add(query)
        db.session.commit()
        return Response(status=200)

    except KeyError as e:
        logging.error("Missing critical key")
        return Response("Missing critical key/value", status=400)

@app.route('/retrieve_gcode/<id>')
def retrieve_gcode(id):
    result = GCode.query.get(id)
    if not result:
        return Response("entry does not exist", status=400)
    return from_sql(result)

if __name__ == '__main__':
    app.run()

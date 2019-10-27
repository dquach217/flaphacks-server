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

    def __init__(self, timestamp, svg_file, svg_name):
        self.timestamp = timestamp
        self.svg_file = g_code_file
        self.svg_name = g_code_name

@app.route('/gcode', methods=['POST'])
def svg_to_gcode():
    request_json=flask.request.json
    g_code_file=request_json['g_code_file']
    g_code_name=request_json['g_code_name']
    timestamp_data=request_json['time_stamp']

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


if __name__ == '__main__':
    app.run()

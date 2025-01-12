import os
from flask import Flask, request, jsonify
from flask.json.provider import DefaultJSONProvider
from db import db, LapTime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DB_URL']
db.init_app(app)

with app.app_context():
    db.create_all()


class CustomJsonProvider(DefaultJSONProvider):
    @staticmethod
    def default(obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        else:
            return DefaultJSONProvider.default(obj)


app.json_provider_class = CustomJsonProvider
app.json = CustomJsonProvider(app)


@app.route("/")
def hello():
    return "hello"


@app.route("/laptime", methods=['POST'])
def post_laptime():
    time = LapTime(
        **request.json
    )
    db.session.add(time)
    db.session.commit()
    return "OK"


@app.route("/laptimes", methods=['GET'])
def get_laptimes():
    times = db.session.execute(db.select(LapTime)).scalars().all()
    return jsonify(times)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

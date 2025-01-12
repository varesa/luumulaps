import os
from flask import Flask, request, jsonify
from db import db, LapTime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DB_URL']
db.init_app(app)


@app.route("/")
def hello():
    return "hello"


@app.route("/laptime", methods=['GET', 'POST'])
def laptime():
    if request.method == 'POST':
        time = LapTime(
            **request.json
        )
        db.session.add(time)
        db.session.commit()
    else:
        times = db.session.execute(db.select(LapTime)).scalars()
        return jsonify(times)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0')

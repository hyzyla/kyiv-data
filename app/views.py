from flask import jsonify

from app.main import app


@app.route("/")
def read_root():
    return jsonify({'response': 'ok'})

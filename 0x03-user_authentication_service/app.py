"""
Script to config a bsic flask app
"""
from flask import Flask
from flask import jsonify


app = Flask(__name__)

@app.route("/", methods=['GET'])

def task():
    """
    A simple GET route that returns a JSON message
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    app.run(debug=True)
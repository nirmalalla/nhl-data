from flask import Flask, jsonify
from data_analysis.hart_trophy import hartTrophyData
from data_analysis.art_ross_trophy import artRossTrophyData
from data_analysis.norris_trophy import norrisTrophyData
from data_analysis.rocket_richard_trophy import rocketRichardTrophyData
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/api/hart", methods=["GET"])
def get_hart():
    data = hartTrophyData()
    return jsonify(data)

@app.route("/api/art_ross", methods=["GET"])
def get_art_ross():
    data = artRossTrophyData()
    return jsonify(data)

@app.route("/api/norris", methods=["GET"])
def get_norris():
    data = norrisTrophyData()
    return jsonify(data)

@app.route("/api/rocket_richard", methods=["GEt"])
def get_rocket_richard():
    data = rocketRichardTrophyData()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
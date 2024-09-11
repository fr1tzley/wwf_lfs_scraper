# your_python_script.py

import base64
from datetime import datetime
import io
import json
import sys
from flask import Flask, render_template, request
import flask
import pandas as pd
from flask_cors import CORS, cross_origin
from sql_query import query_overall
from mapping import get_lon_lat
from graphing import draw_graph
import matplotlib

sys.path.insert(0, '..')

from webscraper import full_query
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

@app.route("/hw")
def index():
    return "Hello World!"

@app.route('/graph', methods=['POST'])
@cross_origin()
def process_graph():
    data = request.get_json()
    start_date = datetime.strptime(data.get("startDate"), '%Y-%m-%d')
    end_date = datetime.strptime(data.get("endDate"), '%Y-%m-%d')
    graph_type = data.get("graph_type")
    keys = data.get("keys")
    step = data.get("step")
    df = query_overall(data, start_date, end_date)

    fig = draw_graph(df, start_date, end_date, graph_type, keys, step)

    image_stream = io.BytesIO()
    fig.savefig(image_stream, format='png')
    plt.close(fig)
    image_stream.seek(0)
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    return json.dumps({"result": encoded_image})

@app.route('/download_data', methods=['POST'])
@cross_origin()

def process_download_data():
    df = pd.read_csv("test\lonlat_Jan-16-2024.csv")

    data = request.get_json()
    print(data["startDate"])
    start_date = datetime.strptime(data.get("startDate"), '%Y-%m-%d')
    end_date = datetime.strptime(data.get("endDate"), '%Y-%m-%d')

    res = query_overall(data, start_date, end_date)
    if len(res) >= 0:
        res = res.to_json(orient="records")
    else:
        res = []
    return res

@app.route('/map', methods=['POST'])
@cross_origin()
def process_map():
    data = request.get_json()
    start_date = datetime.strptime(data.get("startDate"), '%Y-%m-%d')
    end_date = datetime.strptime(data.get("endDate"), '%Y-%m-%d')

    df = query_overall(data, start_date, end_date)
    res = get_lon_lat(df)
    if len(res) > 0:
        res = res.to_json(orient="index")
    else:
        res = []
    return json.dumps({"result": res})

@app.route('/add_data', methods=['POST'])
@cross_origin()
def add_data():
    data = request.get_json()
    rows = json.loads(data["content"])
    
    #for r in rows:
    #    r.update(full_query(r["Article"], r["Date"]))

    return json.dumps({"result": rows})


if __name__ == '__main__':
    app.run(debug=False)
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import psycopg2
import os
import pandas as pd
import io
import functools
import json
from retry import retry

# instantiate the app
app = Flask(__name__, static_folder="./dist/static", template_folder="./dist/static")
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
# Insecure, but just for this project
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Get postgres connection vars
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'benford')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'benford')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'benford')
POSTGRES_HOST = "l7_postgres"

@retry(tries=3, delay=10)
def make_connection():
    conn = psycopg2.connect(
        "dbname={db} user={user} password={password} host={host}".format(
            db=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST
        )
    )
    cursor = conn.cursor()
    return conn, cursor


conn, cursor = make_connection()
print("Connected to {postgres}".format(postgres=POSTGRES_HOST))


def make_histograms(df):
    result = {}
    for column in df.columns:
        reduced = functools.reduce(lambda v, e: v + str(e), df[column].values, '')
        histogram = {
            digit: reduced.count(str(digit)) for digit in range(1, 10) 
        }
        total = functools.reduce(lambda v, e: v + e, histogram.values(), 0)
        for digit in histogram.keys():
            if total == 0:
                histogram[digit] = 0
            else:
                histogram[digit] /= total
        result[column] = histogram
    return result


def parse_file(contents, delimiter='\t'):
    return pd.read_csv(io.StringIO(contents), delimiter=delimiter)


@app.route('/api/files/', methods=["GET"])
def files():
    sql = "SELECT filename, metadata FROM benford;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = {row[0]: row[1] for row in rows}
    return jsonify(results)


def get_file(filename):
    sql = "SELECT contents FROM benford WHERE filename=%s;"
    cursor.execute(sql, [filename])
    result = cursor.fetchone()
    return result[0].tobytes()


@app.route("/api/reparse/", methods=["POST"])
def reparse():
    data = request.get_json()
    if 'filename' not in data or 'delimiter' not in data:
        raise Exception("Bad post")
    if data['delimiter'] == 'tab':
        delimiter = '\t'
    elif data['delimiter'] == 'comma':
        delimiter = ','
    contents = get_file(data['filename'])
    df = parse_file(contents.decode('utf-8'), delimiter=delimiter)
    histogram = make_histograms(df)
    metadata = {
        'delimiter': delimiter,
        'histogram': histogram
    }
    sql = "UPDATE benford SET metadata=%s WHERE filename=%s"
    cursor.execute(sql, [json.dumps(metadata), data['filename']])
    conn.commit()
    return jsonify(metadata)


@app.route("/api/upload/", methods=["POST"])
def upload():
    if not request.files or 'file' not in request.files:
        raise Exception("Bad Request")
    blob = request.files["file"]
    try:
        filename = blob.filename
        contents = blob.stream.read()
        try:
            df = parse_file(contents.decode('utf-8'))
            histogram = make_histograms(df)
            metadata = {
                'delimiter': 'tab',
                'histogram': histogram
            }
        except:
            raise Exception("Parsing error")
        binary = psycopg2.Binary(contents)
        sql = "INSERT INTO benford (filename, contents, metadata) VALUES (%s, %s, %s);"
        cursor.execute(sql, [filename, binary, json.dumps(metadata)])
        conn.commit()
    except:
        raise Exception("DB Error")
    return jsonify(metadata)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


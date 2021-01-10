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
            digit: reduced.count(str(digit)) for digit in range(10) 
        }
        total = functools.reduce(lambda v, e: v + e, histogram.values(), 0)
        for digit in histogram.keys():
            if total == 0:
                histogram[digit] = 0
            else:
                histogram[digit] /= total
        print("COLUMN", column)
        result[column] = histogram
    return result


def parse_file(contents, delimiter='\t'):
    return pd.read_csv(io.StringIO(contents), delimiter=delimiter)


@app.route("/api/upload/", methods=["POST"])
def upload():
    if not request.files or 'file' not in request.files:
        raise Exception("Bad Request")
    blob = request.files["file"]
    try:
        filename = blob.filename
        contents = blob.stream.read()
        print(type(contents))
        try:
            df = parse_file(contents.decode('utf-8'))
            histogram = make_histograms(df)
        except:
            raise Exception("Parsing error")
        binary = psycopg2.Binary(contents).getquoted()
        sql = "INSERT INTO benford (filename, contents, metadata) VALUES (%s, %s, %s)"
        cursor.execute(sql, [filename, binary, json.dumps(histogram)])
        conn.commit()
    except:
        raise Exception("DB Error")
    return jsonify(histogram)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


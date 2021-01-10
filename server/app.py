from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import psycopg2
import os
import pandas as pd
import io
import functools

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
conn = psycopg2.connect(
    "dbname={db} user={user} password={password} host={host}".format(
        db=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST
    )
)
cursor = conn.cursor()

def make_histograms(df):
    result = {}
    for column in df.columns:
        reduced = functools.reduce(lambda v, e: v + str(e), df[column].values, '')
        histogram = {
            digit: reduced.count(str(digit)) for digit in range(10) 
        }
        total = functools.reduce(lambda v, e: v + e, histogram.values(), 0)
        for digit in histogram.keys():
            histogram[digit] /= total
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
        try:
            filetype, data = parse_file(contents)
        except:
            raise Exception("Parsing error")
        binary = psycopg2.Binary(contents).getquoted()
        sql = "INSERT INTO benford (filename, contents) VALUES (%s, %s)"
        cursor.execute(sql, [filename, binary])
        conn.commit()
    except:
        raise Exception("DB Error")
    return "OK"


@app.route('/', methods=['GET'])
def index():
    print("Hello world")
    return render_template("index.html")


from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import psycopg2
import os

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

@app.route("/api/upload/", methods=["POST"])
def upload():
    if not request.files or 'file' not in request.files:
        raise Exception("Bad Request")
    blob = request.files["file"]
    try:
        filename = blob.filename
        binary = psycopg2.Binary(blob.stream.read()).getquoted()
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


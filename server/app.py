from flask import Flask, render_template

# instantiate the app
app = Flask(__name__, static_folder="./dist/static", template_folder="./dist/static")
app.config.from_object(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


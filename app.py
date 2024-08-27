from flask import Flask, request
import db

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/honeydews/<id>.json")
def show(id):
    return db.honeydews_find_by_id(id)


@app.route("/honeydews.json")
def index():
    return db.honeydews_all()


@app.route("/honeydews.json", methods=["POST"])
def create():
    name = request.form.get("name")
    description = request.form.get("description")
    priority = request.form.get("priority")
    return db.honeydews_create(name, description, priority)

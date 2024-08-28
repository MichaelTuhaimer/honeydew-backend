from flask import Flask, request
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/honeydews/<id>.json")
def showhoneydews(id):
    return db.honeydews_find_by_id(id)
@app.route("/honeydews.json")
def indexhoneydews():
    return db.honeydews_all()
@app.route("/honeydews.json", methods=["POST"])
def createhoneydews():
    name = request.form.get("name")
    completed = request.form.get("completed")
    deadline = request.form.get("deadline")
    description = request.form.get("description")
    priority = request.form.get("priority")
    category_id = request.form.get("category_id")
    user_id = request.form.get("user_id")
    return db.honeydews_create(name, completed, deadline, description, priority, category_id, user_id)
@app.route("/honeydews/<id>.json", methods=["PATCH"])
def updatehoneydews(id):
    name = request.form.get("name")
    completed = request.form.get("completed")
    deadline = request.form.get("deadline")
    description = request.form.get("description")
    priority = request.form.get("priority")
    category_id = request.form.get("category_id")
    user_id = request.form.get("user_id")
    return db.honeydews_update_by_id(id, name, completed, deadline, description, priority, category_id, user_id)
@app.route("/honeydews/<id>.json", methods=["DELETE"])
def destroyhoneydews(id):
    return db.honeydews_destroy_by_id(id)


@app.route("/categories/<id>.json")
def showcategories(id):
    return db.categories_find_by_id(id)
@app.route("/categories.json")
def indexcategories():
    return db.categories_all()
@app.route("/categories.json", methods=["POST"])
def createcategories():
    name = request.form.get("name",)
    return db.categories_create(name)
@app.route("/categories/<id>.json", methods=["PATCH"])
def updatecategories(id):
    name = request.form.get("name")
    return db.categories_update_by_id(id, name)
@app.route("/categories/<id>.json", methods=["DELETE"])
def destroycategories(id):
    return db.categories_destroy_by_id(id)
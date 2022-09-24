from ast import For
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:mukhtar@localhost:5432/hayley'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Fruit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

# db.create_all()
# db.session.commit()

@app.route("/")
def index():
    return "Hello Hayley"

@app.route("/new-fruit", methods=["POST"])
def new_fruit():
    name = request.get_json()['name']
    description = request.get_json()['description']
    fruit = Fruit(name=name, description=description)
    db.session.add(fruit)
    db.session.commit()
    return jsonify("New Fruit created")

@app.route("/fruits", methods=["GET"])
def get_fruits():
    all_fruits = []
    fruits = Fruit.query.all()
    for fruit in fruits:
        all_fruits.append({
            "name": fruit.name,
            "description": fruit.description
        })
    return jsonify(all_fruits)

@app.route("/update-fruit/<int:id>", methods=["PATCH"])
def update_fruit(id):
    fruit = Fruit.query.get(id)
    name = request.get_json()['name']
    description = request.get_json()['description']
    fruit.name = name
    fruit.description = description
    db.session.commit()
    return jsonify("Fruit Updated Successfully")
    
@app.route("/delete-fruit/<int:id>", methods=["DELETE"])
def delete_fruit(id):
    fruit = Fruit.query.get(id)
    db.session.delete(fruit)
    db.session.commit()
    return jsonify("Fruit Deleted Successfully")
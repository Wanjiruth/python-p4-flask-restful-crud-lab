# app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from datetime import datetime
from models import db, Plant

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route("/")
def index():
    return "<h1>Plant Management App</h1>"

class PlantsResource(Resource):
    def get(self):
        plants = Plant.query.all()
        return [plant.to_dict() for plant in plants], 200

    def post(self):
        data = request.get_json()
        try:
            new_plant = Plant(
                name=data['name'],
                image=data['image'],
                price=data['price']
            )
            db.session.add(new_plant)
            db.session.commit()
            return new_plant.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 400

class PlantResource(Resource):
    def get(self, id):
        plant = db.session.get(Plant, id)
        if plant:
            return plant.to_dict(), 200
        return {"error": "Plant not found"}, 404

    def patch(self, id):
        plant = db.session.get(Plant, id)
        if plant:
            data = request.get_json()
            plant.is_in_stock = data.get('is_in_stock', plant.is_in_stock)
            db.session.commit()
            return plant.to_dict(), 200
        return {"error": "Plant not found"}, 404

    def delete(self, id):
        plant = db.session.get(Plant, id)
        if plant:
            db.session.delete(plant)
            db.session.commit()
            return '', 204
        return {"error": "Plant not found"}, 404

api.add_resource(PlantsResource, '/plants')
api.add_resource(PlantResource, '/plants/<int:id>')

if __name__ == "__main__":
    app.run(port=5555, debug=True)

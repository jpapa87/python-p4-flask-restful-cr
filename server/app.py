#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Retrieving Records with Flask-RESTful - GET
class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }
        response = make_response(
            response_dict, 200
        )
        return response
api.add_resource( Home , "/")

# Retrieving Records with Flask-RESTful - GET
class Newsletters(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]
        response = make_response(response_dict_list , 200)
        return response

# Creating Records with Flask-RESTful - POST
    def post(self):
        new_record = Newsletter(
            title = request.form["title"],
            body = request.form["body"],
        )
        db.session.add(new_record)
        db.session.commit()
        response_dict = new_record.to_dict()
        response = make_response(response_dict, 201,)
        return response

api.add_resource( Newsletters , "/newsletters")

# Building Another Resource and Retrieving a Single Record
# building a route to get a single record back from the database
# A GET route already exists under newsletters/.
# Retrieving a single record means that we need some sort of identifier.
# This means that we need to build a new Resource for this endpoint, and that it should include the id in the URL.
class Newsletter_ById(Resource):
    def get(self, id):
        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()
        response = make_response(response_dict, 200)
        return response
api.add_resource(Newsletter_ById, "/newsletters/<int:id>")
        


if __name__ == '__main__':
    app.run(port=5555, debug=True)

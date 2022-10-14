from flask import Flask, request
from flask_restful import Resource, Api
from models import Advertise, advertise_schema, db

app = Flask(__name__)
api = Api(app)


class AdvertiseResource(Resource):
    def get(self):
        advertises = Advertise.query.all()
        return advertise_schema.dump(advertises)

    def post(self):
        new_ad = Advertise(
            title=request.json['title'],
            description=request.json['description'],
            created_at=request.json['created_at'],
            author=request.json['author'],
        )
        db.session.add(new_ad)
        db.session.commit()
        return advertise_schema.dump(new_ad)
    
    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(AdvertiseResource, '/adverts')

if __name__ == '__main__':
    app.run(debug=True)

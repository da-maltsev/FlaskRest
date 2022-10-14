import os
from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

db.init_app(app)
ma = Marshmallow(app)


class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now())
    author = db.Column(db.String)

    def __repr__(self):
        return '<Post %s>' % self.title


class AdvertisementSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "created_at", "author")
        model = Advertisement


advertisement_schema = AdvertisementSchema()
advertisement_schemas = AdvertisementSchema(many=True)


class AdvertisementListResource(Resource):
    def get(self):
        advertisements = Advertisement.query.all()
        return advertisement_schemas.dump(advertisements)

    def post(self):
        new_ad = Advertisement(
            title=request.json['title'],
            description=request.json['description'],
            created_at=datetime.strptime(request.json['created_at'], '%d/%m/%y %H:%M:%S'),
            author=request.json['author'],
        )
        db.session.add(new_ad)
        db.session.commit()
        return advertisement_schema.dump(new_ad)


class AdvertisementResource(Resource):
    def get(self, ad_id):
        ad = Advertisement.query.get_or_404(ad_id)
        return advertisement_schema.dump(ad)

    def patch(self, ad_id):
        ad = Advertisement.query.get_or_404(ad_id)
        r = request.json

        if 'title' in r:
            ad.title = r['title']
        if 'description' in r:
            ad.description = r['description']
        if 'created_at' in r:
            ad.created_at = datetime.strptime(r['created_at'], '%d/%m/%y %H:%M:%S')
        if 'author' in r:
            ad.description = r['author']

        db.session.commit()
        return advertisement_schema.dump(ad)

    def delete(self, ad_id):
        ad = Advertisement.query.get_or_404(ad_id)
        db.session.delete(ad)
        db.session.commit()
        return '', 204


api.add_resource(AdvertisementListResource, '/ad')
api.add_resource(AdvertisementResource, '/ad/<int:ad_id>')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
